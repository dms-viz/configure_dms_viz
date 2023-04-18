#!/usr/bin/env python
import os
import json
import click
import pandas as pd
from pandas.api.types import is_numeric_dtype


# Check that the mutation data is in the correct format
def format_mutation_data(mut_metric_df, metric_col, alphabet):
    """Check that the mutation data is in the correct format.

    This data should be a pandas.DataFrame with the following columns:
    - reference_site: The site number in the reference sequence
    - wildtype: The wildtype amino acid at the site
    - mutant: The mutant amino acid at the site
    - metric_col: The metric to visualize
    - epitope: The epitope the mutation is in

    Parameters
    ----------
    mut_metric_df: pandas.DataFrame
        A dataframe containig site- and mutation-level data for visualization.
    metric_col: str
        The name of the column the contains the metric for visualization.
    alphabet: list
        A list of the amino acid names correspoinding to the mutagenized residues.

    Returns
    -------
    pandas.DataFrame
        The mutation dataframe with the site column renamed to reference_site if necessary.
    """

    # Ensure that the site column is called 'reference_site' and rename if necessary
    if "reference_site" not in set(mut_metric_df.columns):
        if "site" in set(mut_metric_df.columns):
            mut_metric_df = mut_metric_df.rename(columns={"site": "reference_site"})
        else:
            raise ValueError(
                "The mutation dataframe is missing either the site or reference_site column designating reference sites."
            )

    # Check that the rest of the necessary columns are present in the mut_metric dataframe
    missing_mutation_columns = {
        "reference_site",
        "wildtype",
        "mutant",
        metric_col,
        "epitope",
    } - set(mut_metric_df.columns)
    if missing_mutation_columns:
        raise ValueError(
            f"The following columns do not exist in the mutation dataframe: {list(missing_mutation_columns)}"
        )

    # Check that all mutant and wildtype residue names are in the provided alphabet
    mut_metric_alphabet = set(
        mut_metric_df.mutant.to_list() + mut_metric_df.wildtype.to_list()
    )
    missing_amino_acids = mut_metric_alphabet - {aa for aa in alphabet}
    if missing_amino_acids:
        raise ValueError(
            f"Some of the wildtype or mutant amino acid names are not in the provided alphabet, i.e., {missing_amino_acids}"
        )

    return mut_metric_df


# Check that the sitemap data is in the correct format
def format_sitemap_data(sitemap_df, mut_metric_df, included_chains):
    """Check that the sitemap data is in the correct format.

    This data should be a pandas.DataFrame with the following columns:
    - reference_site: The site number in the reference sequence that
        corresponds to the reference site in the mutation dataframe
    - sequential_site: The order of the site in the protein sequence and
        on the x-axis of the visualization
    - protein_site: [Optional] The site number in the protein structure if
        different from the reference site

    Parameters
    ----------
    mut_metric_df: pandas.DataFrame
        A dataframe containig site- and mutation-level data for visualization.
    sitemap_df: pandas.DataFrame
        A dataframe mapping sequential sites to reference sites to protein sites.
    included_chains: list
        A list of the protien chains to include in the visualization.

    Returns
    -------
    pandas.DataFrame
    """

    # Check that required columns are present in the sitemap data
    missing_sitemap_columns = {"sequential_site", "reference_site"} - set(
        sitemap_df.columns
    )
    if missing_sitemap_columns:
        raise ValueError(
            f"The following columns do not exist in the sitemap: {list(missing_sitemap_columns)}"
        )

    # Check that the reference sites are the same between the sitemap and mut_metric dataframe
    missing_reference_sites = set(mut_metric_df.reference_site.tolist()) - set(
        sitemap_df.reference_site.tolist()
    )
    if missing_reference_sites:
        raise ValueError(
            f"There are reference sites in the mutation dataframe missing from your sitemap e.g. {list(missing_reference_sites)[0:10]}..."
        )

    # Check if the sequential sites are a numeric type as they need to be for ordering the x-axis
    if not is_numeric_dtype(sitemap_df["sequential_site"]):
        # Try to coerce the sequential sites into a numeric type
        try:
            sitemap_df["sequential_site"] = pd.to_numeric(sitemap_df["sequential_site"])
        except ValueError:
            raise ValueError(
                "The sequential_site column of the sitemap is not numeric and cannot be coerced into a numeric type."
            )

    # If the protein site isn't specified, assume that it's the same as the reference site
    if "protein_site" not in sitemap_df.columns:
        click.secho(
            message="'protein_site' column is not present in the sitemap. Assuming that the reference sites correspond to protein sites.",
            fg="yellow",
        )
        sitemap_df["protein_site"] = sitemap_df["reference_site"].apply(
            lambda y: y if str(y).isnumeric() else ""
        )
    else:
        # Make sure that the provided protein column has no invalid values
        if (
            not sitemap_df["protein_site"]
            .apply(lambda y: y == "" or str(y).isnumeric())
            .all()
        ):
            raise ValueError(
                "The protein_site column of the sitemap contains invalid values that cannot be coerced into a numeric form."
            )

    # Add the included chains to the sitemap dataframe if there are any
    sitemap_df["chains"] = sitemap_df["protein_site"].apply(
        lambda y: included_chains if str(y).isnumeric() else ""
    )

    return sitemap_df


# Join the additional dataframes to the main dataframe
def join_additional_data(mut_metric_df, join_data):
    """Join additional dataframes to the main mutation dataframe.

    The additional dataframes should have the following columns:
    - reference_site: The site number in the reference sequence that
        corresponds to the reference site in the mutation dataframe
    - wildtype: The wildtype amino acid at the site
    - mutant: The mutant amino acid at the site

    *Note that there currently this data should apply to all site and should
    be identical between epitopes or conditions. Otherwise, there will be an
    errror about duplicate data.*

    Parameters
    ----------
    mut_metric_df: pandas.DataFrame
        A dataframe containig site- and mutation-level data for visualization.
    join_data: list of pandas.DataFrame
        A list of dataframes to join to the main mutation dataframe.

    Returns
    -------
    pandas.DataFrame
        The updated mut_metric_df with the joined dataframes.

    """
    for df in join_data:
        # Check that the neccessary columns are present, first the reference_sites
        if "reference_site" not in set(df.columns):
            if "site" in set(df.columns):
                df.rename({"site": "reference_site"})
            else:
                raise ValueError(
                    "One of the join dataframes is missing either the site or reference_site column designating reference sites."
                )
        # Now check for the other necessary columns
        missing_join_columns = {"reference_site", "wildtype", "mutant"} - set(
            df.columns
        )
        if missing_join_columns:
            raise ValueError(
                f"The following columns do not exist in the join dataframe: {missing_join_columns}"
            )

        # Before merging, make sure that there aren't more than one measurement per merge condition
        if df[["reference_site", "wildtype", "mutant"]].duplicated().any():
            raise ValueError(
                "Duplicates measurements per mutation were found in join dataframe, merge cannot be performed"
            )

        # Before merging, remove any columns present in both dataframes
        duplicate_columns = [
            col
            for col in df.columns
            if col
            in (set(mut_metric_df.columns) - {"reference_site", "wildtype", "mutant"})
        ]
        if duplicate_columns:
            df = df.drop(duplicate_columns, axis=1)
            click.secho(
                message=f"Warning: duplicate column names exist between mutation dataframe and join dataframe. Dropping {duplicate_columns}.",
                fg="red",
            )

        # Merge this dataframe with the main dataframe
        mut_metric_df = mut_metric_df.merge(
            df, on=["reference_site", "wildtype", "mutant"], how="left"
        )

        return mut_metric_df


# Check the filter columns are in the main dataframe and formatted correctly
def check_filter_columns(mut_metric_df, filter_cols):
    """Check the filter columns are in the main dataframe and formatted correctly.

    Parameters
    ----------
    mut_metric_df: pandas.DataFrame
        A dataframe containig site- and mutation-level data for visualization.
    filter_cols: dict
        A dictionary of column names and values to filter the dataframe by.

    Returns
    -------
    list of str
        The names of the filter columns to add to the dataframe.
    """
    # Get the current names of the columns
    filter_column_names = [col for col in filter_cols.keys()]

    # Make sure the filter columns are actually in the dataframe at this point
    missing_filter_columns = set(filter_column_names) - set(mut_metric_df.columns)
    if missing_filter_columns:
        raise ValueError(
            f"The filter column(s): {missing_filter_columns} are not present in the data."
        )

    # Make sure that filter columns are numeric
    for col in filter_column_names:
        try:
            pd.to_numeric(mut_metric_df[col])
        except ValueError:
            raise ValueError(
                f"The column {col} contains values that cannot be coerced into numbers."
            )

    # Make sure that the filter columns don't have spaces in them
    for col in filter_column_names:
        if " " in col:
            raise ValueError(f"There is a space in {col}. Please remove this.")

    return filter_column_names


# Check the tooltip columns are in the main dataframe and formatted correctly
def check_tooltip_columns(mut_metric_df, tooltip_cols):
    """Check the tooltip columns are in the main dataframe and formatted correctly

    Parameters
    ----------
    mut_metric_df: pandas.DataFrame
        A dataframe containig site- and mutation-level data for visualization.
    tooltip_cols: dict
        A dictionary of column names and values use as tooltips in the visualization.

    Returns
    -------
    list of str
        The names of the tooltip columns to add to the dataframe.
    """
    # Get the current names of the columns
    tooltip_column_names = [col for col in tooltip_cols.keys()]

    # Make sure the tooltip columns are actually in the dataframe at this point
    missing_tooltip_columns = set(tooltip_column_names) - set(mut_metric_df.columns)
    if missing_tooltip_columns:
        raise ValueError(
            f"The tooltip column(s): {missing_tooltip_columns} are not present in the data."
        )

    return tooltip_column_names


def make_experiment_dictionary(
    mut_metric_df,
    metric_col,
    sitemap_df,
    structure,
    join_data=None,
    filter_cols=None,
    tooltip_cols=None,
    metric_name=None,
    included_chains="polymer",
    excluded_chains="none",
    alphabet="RKHDEQNSTYWFAILMVGPC-*",
    colors=["#0072B2", "#CC79A7", "#4C3549", "#009E73"],
):
    """Take site-level and mutation-level measurements and format into
    a dictionary that can be used to create a JSON file for the visualization.

    Prameters
    ---------
    mut_metric_df: pandas.DataFrame
        A dataframe containig site- and mutation-level data for visualization.
    metric_col: str
        The name of the column the contains the metric for visualization.
    sitemap_df: pandas.DataFrame
        A dataframe mapping sequential sites to reference sites to protein sites.
    structure: str
        An RCSB PDB ID (i.e. 6UDJ) or the path to a file with a *.pdb extension.
    metric_name: str or None
        Rename the metric column to this name if desired. This name shows up in the plot.
    join_data: list or None
        A list of pandas.dataFrames to join to the main dataframe by mutation/epitope.
    filter_cols: dict or None
        A dictionary of column names and formatted names to designate as filters.
    tooltip_cols: dict or None
        A dictionary of column names and formatted names to designate as tooltips.
    included_chains: str or None
        If not mapping data to every chain, a space separated list of chain names (i.e. "C F M G J P").
    excluded_chains: str or None
        A space separated string of chains that should not be shown on the protein structure (i.e. "B L R").
    alphabet: str
        The amino acid labels in the order the should be displayed on the heatmap.
    colors: list
        A list of colors that will be used for each epitope in the experiment.

    Returns
    -------
    dict
        A dictionary containing a single dataset for visualization to convert into a JSON file.
    """

    # Check that the necessary columns are present in the mut_metric dataframe and format
    mut_metric_df = format_mutation_data(mut_metric_df, metric_col, alphabet)

    # Check that the necessary columns are present in the sitemap dataframe and format
    sitemap_df = format_sitemap_data(sitemap_df, mut_metric_df, included_chains)

    # Keep track of the required columns to cut down on the final total data size
    cols_to_keep = ["reference_site", "wildtype", "mutant", metric_col, "epitope"]

    # Join the additional data to the main dataframe if there is any
    if join_data:
        mut_metric_df = join_additional_data(mut_metric_df, join_data)

    # Add the filter columns to the required columns
    if filter_cols:
        cols_to_keep += check_filter_columns(mut_metric_df, filter_cols)

    # Add the tooltip columns to required columns
    if tooltip_cols:
        cols_to_keep += check_filter_columns(mut_metric_df, tooltip_cols)

    # Subset the mutation dataframe down to the required columns
    mut_metric_df = mut_metric_df[list(set(cols_to_keep))]

    # Determine whether the structure is a PDB ID or a local file
    _, ext = os.path.splitext(structure)

    if ext == ".pdb":
        # PDB is local, load it in as a string
        with open(structure, "r") as f:
            pdb = f.read()
    else:
        pdb = structure

    # Get a list of the epitopes and map these to the colors
    epitopes = list(set(mut_metric_df.epitope))
    if len(epitopes) > len(colors):
        raise ValueError(
            f"There are {len(epitopes)} epitopes, but only {len(colors)} color(s) specified. Please specify more colors."
        )
    epitope_colors = {epitope: colors[i] for i, epitope in enumerate(epitopes)}

    # Rename the metric column to the metric name
    if metric_name:
        mut_metric_df = mut_metric_df.rename(columns={metric_col: metric_name})
        metric_col = metric_name

    # Make a dictionary holding the experiment data
    experiment_dict = {
        "mut_metric_df": json.loads(mut_metric_df.to_json(orient="records")),
        "metric_col": metric_col,
        "sitemap": sitemap_df.set_index("reference_site").to_dict(orient="index"),
        "alphabet": [aa for aa in alphabet],
        "pdb": pdb,
        "dataChains": included_chains.split(" "),
        "excludeChains": excluded_chains.split(" "),
        "epitopes": epitopes,
        "epitope_colors": epitope_colors,
        "filter_cols": filter_cols,
        "tooltip_cols": tooltip_cols,
    }

    return experiment_dict


# Custom classes for click parameters
class ListParamType(click.ParamType):
    name = "list"

    def convert(self, value, param, ctx):
        try:
            if isinstance(value, list):
                return value
            elif isinstance(value, str):
                return list(map(str, value.split(",")))
        except ValueError:
            self.fail(f"{value} is not a valid list", param, ctx)


class DictParamType(click.ParamType):
    name = "dict"

    def convert(self, value, param, ctx):
        try:
            return json.loads(value.replace("'", '"'))
        except ValueError:
            self.fail(f"{value} is not a valid dictionary", param, ctx)


# Command line interface for creating a JSON file for visualizing protein data
@click.command("configure-dms-viz")
@click.option(
    "--input",
    type=click.Path(exists=True),
    required=True,
    help="Path to a csv with site- and mutation-level data to visualize on a protein structure.",
)
@click.option(
    "--sitemap",
    type=click.Path(exists=True),
    required=True,
    help="Path to a csv with a mapping of sequential sites to reference sites to protein sites.",
)
@click.option(
    "--metric",
    type=str,
    required=True,
    help="The name of the column the contains the metric for visualization.",
)
@click.option(
    "--structure",
    type=str,
    required=True,
    help="An RCSB PDB ID (i.e. 6UDJ) or the path to a file with a *.pdb extension.",
)
@click.option(
    "--name",
    type=str,
    required=True,
    help="The name of the experiment. This will be used when concatenating multiple experiments.",
)
@click.option(
    "--output",
    type=click.Path(),
    required=True,
    help="Path to save the *.json file containing the data for the visualization tool.",
)
@click.option(
    "--metric-name",
    type=str,
    required=False,
    default=None,
    help="Optionally, the name that should show up for your metric in the plot.",
)
@click.option(
    "--filter-cols",
    type=DictParamType(),
    required=False,
    default=None,
    help="Optionally, a space separated list of columns to use as filters in the visualization. Example: \"{'effect': 'Functional Effect', 'times_seen': 'Times Seen'}\"",
)
@click.option(
    "--tooltip-cols",
    type=DictParamType(),
    required=False,
    default=None,
    help="Optionally, a space separated list of columns to use as tooltips in the visualization. Example: \"{'times_seen': '# Obsv', 'effect': 'Func Eff.'}\"",
)
@click.option(
    "--join-data",
    type=ListParamType(),
    required=False,
    default=None,
    help='Optionally, a csv file with additional data to join to the mutation data. Example: "path/to/join_data.csv, path/to/join_data2.csv"',
)
@click.option(
    "--included-chains",
    type=str,
    required=False,
    default="polymer",
    help='Optionally, a space separated list of chains to include in the visualization. Example: "A B C"',
)
@click.option(
    "--excluded-chains",
    type=str,
    required=False,
    default="none",
    help='A space separated list of chains to exclude from the visualization. Example: "A B C"',
)
@click.option(
    "--alphabet",
    type=str,
    required=False,
    default="RKHDEQNSTYWFAILMVGPC-*",
    help="A string of amino acids to use as the alphabet for the visualization. The order is the order in which the amino acids will be displayed on the heatmap.",
)
@click.option(
    "--colors",
    type=ListParamType(),
    required=False,
    default=["#0072B2", "#CC79A7", "#4C3549", "#009E73"],
    help='A list of colors to use for the epitopes in the visualization. Example: "#0072B2, #CC79A7, #4C3549, #009E73"',
)
def cli(
    input,
    sitemap,
    metric,
    structure,
    name,
    output,
    metric_name,
    filter_cols,
    tooltip_cols,
    join_data,
    included_chains,
    excluded_chains,
    alphabet,
    colors,
):
    """Command line interface for creating a JSON file for visualizing protein data

    Args:
        input (str): Path to a csv with site- and mutation-level data to visualize on a protein structure.
        sitemap (str): Path to a csv with a mapping of sequential sites to reference sites to protein sites.
        metric (str): The name of the column the contains the metric for visualization.
        structure (str): An RCSB PDB ID (i.e. 6UDJ) or the path to a file with a *.pdb extension.
        name (str): The name of the experiment. This will be used when concatenating multiple experiments.
        output (str): Path to save the *.json file containing the data for the visualization tool.
        metric_name (str, optional): Optionally, the name that should show up for your metric in the plot. Defaults to None.
        filter_cols (dict, optional): Optionally, a space separated list of columns to use as filters in the visualization. Defaults to None.
        tooltip_cols (dict, optional): Optionally, a space separated list of columns to use as tooltips in the visualization. Defaults to None.
        join_data (list, optional): Optionally, a csv file with additional data to join to the mutation data. Defaults to None.
        included_chains (str, optional): Optionally, a space separated list of chains to include in the visualization. Defaults to "polymer".
        excluded_chains (str, optional): A space separated list of chains to exclude from the visualization. Defaults to "none".
        alphabet (str, optional): A string of amino acids to use as the alphabet for the visualization. The order is the order in which the amino acids will be displayed on the heatmap. Defaults to "RKHDEQNSTYWFAILMVGPC-*".
        colors (list, optional): A list of colors to use for the epitopes in the visualization. Defaults to ["#0072B2", "#CC79A7", "#4C3549", "#009E73"].
    """

    # Read in the main mutation data
    mut_metric_df = pd.read_csv(input)

    # Split the list of join data files and read them in as a list
    if join_data:
        join_data_dfs = [pd.read_csv(file) for file in join_data]
    # Read in the sitemap data
    sitemap_df = pd.read_csv(sitemap)

    # Create the dictionary to save as a json
    experiment_dict = make_experiment_dictionary(
        mut_metric_df,
        metric,
        sitemap_df,
        structure,
        join_data_dfs,
        filter_cols,
        tooltip_cols,
        metric_name,
        included_chains,
        excluded_chains,
        alphabet,
        colors,
    )

    # Write the dictionary to a json file
    with open(output, "w") as f:
        json.dump({name: experiment_dict}, f)


if __name__ == "__main__":
    cli()
