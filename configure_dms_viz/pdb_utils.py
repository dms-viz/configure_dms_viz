import os
import requests
import warnings
import Bio.PDB
import pandas as pd
from Bio.SeqUtils import seq1
from io import StringIO


def get_structure(pdb_input):
    """
    Fetch a PDB structure from the RCSB PDB web service or load it from a local file.

    This function takes a string as input, which should either be a 4-character PDB ID or
    a path to a local PDB file. The function fetches the structure with the specified PDB ID
    from the RCSB PDB web service, or reads the structure from the specified local PDB file,
    and returns a Bio.PDB structure object.

    Parameters
    ----------
    pdb_input : str
        A string that is either a 4-character PDB ID or a path to a local .pdb file.

    Returns
    -------
    structure : Bio.PDB.Structure.Structure
        A Bio.PDB structure object.

    Raises
    ------
    ValueError
        If the pdb_input is neither a valid PDB ID nor a local PDB file path.
        If there was an error reading the local PDB file or parsing the PDB content.
        If there was an error downloading the PDB file from the RCSB PDB web service.

    """

    # Check if the input is a local file path
    if os.path.isfile(pdb_input) and pdb_input.endswith(".pdb"):
        try:
            # Ignore warnings about discontinuous chains
            with warnings.catch_warnings():
                warnings.simplefilter(
                    "ignore", category=Bio.PDB.PDBExceptions.PDBConstructionWarning
                )
                structure = Bio.PDB.PDBParser().get_structure(pdb_input[:-4], pdb_input)
        except Exception as e:
            raise ValueError(f"Error reading PDB file {pdb_input}: {e}") from e
    elif len(pdb_input) == 4 and pdb_input.isalnum():  # Check for a valid PDB ID format
        # Try to fetch the structure from RCSB PDB
        response = requests.get(f"https://files.rcsb.org/download/{pdb_input}.cif")
        if response.status_code == 200:
            try:
                pdb_file_content = StringIO(response.text)
                # Ignore warnings about discontinuous chains
                with warnings.catch_warnings():
                    warnings.simplefilter(
                        "ignore", category=Bio.PDB.PDBExceptions.PDBConstructionWarning
                    )
                    structure = Bio.PDB.MMCIFParser().get_structure(
                        pdb_input, pdb_file_content
                    )
            except Exception as e:
                raise ValueError(
                    f"Error parsing PDB content for {pdb_input}: {e}"
                ) from e
        else:
            raise ValueError(
                f"Failed to download {pdb_input} from the RCSB database. Status code: {response.status_code}"
            )
    else:
        raise ValueError(
            f"Invalid input: {pdb_input}. Please provide a valid PDB ID or a local PDB file path."
        )

    return structure


def check_chains(structure, chains):
    """
    Check that the user supplied data chains are in the structure.

    Parameters
    ----------
    structure : Bio.PDB.Structure.Structure
        A Bio.PDB structure object.

    chains : list
        A list of chain IDs.

    Raises
    ------
    ValueError
        If the chains are not in the structure.
    """
    # Check that the chains are in the structure
    missing_chains = set(chains) - {chain.id for chain in structure[0]}
    if missing_chains:
        raise ValueError(
            f"Data chain(s): {missing_chains} are not present in the PDB structure."
        )


def check_wildtype_residues(structure, mut_metric_df, sitemap_df, excluded_chains):
    """
    Checks the percentage of wildtype residues in the DataFrame that match those in a provided PDB structure.

    The function first merges the input dataframes on 'reference_site' and then checks each protein site for
    matching wildtype residues. A site is considered a match if all chains in that site have a matching wildtype
    residue in the structure. It also counts the number of sites that are not present in the structure. The
    function returns the proportion of matching and missing sites in the input data.

    Parameters
    ----------
    structure : Bio.PDB.Structure
        The structure obtained from a PDB file parsed by Bio.PDB.
    mut_metric_df : pandas.DataFrame
        DataFrame containing mutation metric data. Expected to have 'reference_site' and 'wildtype' columns.
    sitemap_df : pandas.DataFrame
        DataFrame containing site map data. Expected to have 'reference_site', 'protein_site', 'chains' columns.
    excluded_chains: str or None
        A str of the chains that shouldn't be included in the visualization separated by a str or None.


    Returns
    -------
    total_matching_residues : float
        The proportion of protein sites in the mut_metric_df where all chains have a matching wildtype residue in
        the structure.
    total_missing_sites : float
        The proportion of protein sites in the mut_metric_df that are not present in the structure.

    Raises
    ------
    KeyError
        If a specified protein site or chain is not found in the structure.
    """

    # Join the protein sites and chains with the wiltype residues in the mut_metric_df by the reference sites
    wildtype_df = (
        pd.merge(mut_metric_df, sitemap_df, on="reference_site", how="left")[
            ["protein_site", "chains", "wildtype"]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # If there was no list of chains given, infer the 'polymer' chains
    standard_residues = [res for res in Bio.PDB.Polypeptide.protein_letters_3to1.keys()]
    if "polymer" in wildtype_df.chains.to_list():
        polymer_chains = []
        for chain in structure[0]:
            chain_is_polymer = False
            for residue in chain:
                # Check if the residue is a standard protein/nucleic acid residue
                if residue.get_resname() in standard_residues:
                    chain_is_polymer = True
                    break
            if chain_is_polymer:
                polymer_chains.append(chain.id)
        if excluded_chains:
            polymer_chains = list(set(polymer_chains) - set(excluded_chains.split(" ")))

    # Iterate through each row and check if the wildtype residue matches the pdb residue
    total_sites = 0
    matching_residues = 0
    missing_sites = 0
    for _, site, chains, wildtype in wildtype_df.itertuples():
        if chains == "polymer":
            chains = polymer_chains
        else:
            chains = chains.split(" ")
        total_sites += 1
        matches_wildtype_at_site = []
        site_not_in_structure = []
        for chain in chains:
            try:
                residue = structure[0][chain][int(site)]
                if seq1(residue.resname) == wildtype.upper():
                    matches_wildtype_at_site.append(True)
                else:
                    matches_wildtype_at_site.append(False)
                site_not_in_structure.append(False)
            except KeyError:
                site_not_in_structure.append(True)
        if matches_wildtype_at_site and all(matches_wildtype_at_site):
            matching_residues += 1
        if site_not_in_structure and all(site_not_in_structure):
            missing_sites += 1

    # Calculate the matching and missing sites
    total_matching_residues = matching_residues / total_sites
    total_missing_sites = missing_sites / total_sites

    return (total_matching_residues, total_missing_sites)
