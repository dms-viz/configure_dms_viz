import os
import requests
import warnings
import Bio.PDB
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
            raise ValueError(f"Error reading PDB file {pdb_input}: {e}")
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
                raise ValueError(f"Error parsing PDB content for {pdb_input}: {e}")
        else:
            raise ValueError(
                f"Failed to download {pdb_input} from the RCSB database. Status code: {response.status_code}"
            )
    else:
        raise ValueError(
            f"Invalid input: {pdb_input}. Please provide a valid PDB ID or a local PDB file path."
        )

    return structure
