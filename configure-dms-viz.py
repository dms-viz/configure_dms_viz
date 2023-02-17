#!/usr/bin/env python
import os
import json
import argparse
import pandas as pd
from pandas.api.types import is_numeric_dtype


def format_input_for_json(mut_metric_df,
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
                          colors=['#0072B2', '#CC79A7', '#4C3549', '#009E73']
                          ):
    """ Take site-level and mutation-level measurements and format into 
    a JSON file for interactive visualization with https://dms-viz.github.io. 

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

    # Ensure that the site column is called 'reference_site'
    if "reference_site" not in set(mut_metric_df.columns):
        if "site" in set(mut_metric_df.columns):
            mut_metric_df = mut_metric_df.rename(
                columns={"site": "reference_site"})
        else:
            raise ValueError(
                "The mutation dataframe is missing either the site or reference_site column designating reference sites.")

    # Check that the rest of the necessary columns are present in the mut_metric dataframe
    missing_mutation_columns = {"reference_site", "wildtype",
                                "mutant", metric_col, "epitope"} - set(mut_metric_df.columns)
    if missing_mutation_columns:
        raise ValueError(
            f"The following columns do not exist in the mutation dataframe: {list(missing_mutation_columns)}")

    # Check that required columns are present in the sitemap data
    missing_sitemap_columns = {'sequential_site',
                               'reference_site'} - set(sitemap_df.columns)
    if missing_sitemap_columns:
        raise ValueError(
            f"The following columns do not exist in the sitemap: {list(missing_sitemap_columns)}")

    # Check that the reference sites are the same between the sitemap and mut_metric dataframe
    missing_reference_sites = set(
        mut_metric_df.reference_site.tolist()) - set(sitemap_df.reference_site.tolist())
    if missing_reference_sites:
        raise ValueError(
            f"There are sites in mutation dataframe missing from your sitemap e.g. {list(missing_reference_sites)[0:10]}...")

    # Check if the sequential sites are a numeric type column
    if not is_numeric_dtype(sitemap_df['sequential_site']):
        # Try to coerce the sequential sites into a numeric type
        try:
            sitemap_df['sequential_site'] = pd.to_numeric(
                sitemap_df['sequential_site'])
        except ValueError:
            raise ValueError(
                "The sequential_site column of the sitemap is not numeric and cannot be coerced into a numeric type.")

    # If the protein site isn't specified, assume that it's the same as the reference site
    if 'protein_site' not in sitemap_df.columns:
        print("'protein_site' column is not present in the sitemap. Assuming that the reference sites correspond to protein sites.")
        sitemap_df['protein_site'] = sitemap_df['reference_site'].apply(
            lambda y: y if str(y).isnumeric() else "")
    else:
        # Make sure that the provided column has no invalid values
        if not sitemap_df['protein_site'].apply(lambda y: y == "" or str(y).isnumeric()).all():
            raise ValueError(
                "The protein_site column of the sitemap contains invalid values that cannot be coerced into a numeric form.")

    # Make sure the sequential sites are numeric
    sitemap_df['sequential_site'] = pd.to_numeric(
        sitemap_df['sequential_site'])

    # If there are additional pieces of data to add, add them
    if join_data:
        for df in join_data:
            # Check that the neccessary columns are present, first the reference_sites
            if not "reference_site" in set(df.columns):
                if "site" in set(df.columns):
                    df.rename({"site": "reference_site"})
                else:
                    raise ValueError(
                        "One of the join dataframes is missing either the site or reference_site column designating reference sites.")
            # Now check for the other necessary columns
            missing_join_columns = {"reference_site",
                                    "wildtype", "mutant"} - set(df.columns)
            if missing_join_columns:
                raise ValueError(
                    f"The following columns do not exist in the join dataframe: {missing_join_columns}")
            # Before merging, make sure that there aren't more than one measurement per merge condition
            if df[['reference_site', 'wildtype', 'mutant']].duplicated().any():
                raise ValueError(
                    "Duplicates measurements per mutation were found in join dataframe, merge cannot be performed")
            # Before merging, remove any columns present in both dataframes
            duplicate_columns = [col for col in df.columns if col in (
                set(mut_metric_df.columns) - {"reference_site", "wildtype", "mutant"})]
            if duplicate_columns:
                df = df.drop(duplicate_columns, axis=1)
                print(
                    f"Warning: duplicate column names exist between mutation dataframe and join dataframe. Dropping {duplicate_columns}.")

            # Merge this dataframe with the main dataframe
            mut_metric_df = mut_metric_df.merge(
                df, on=['reference_site', 'wildtype', 'mutant'], how='left')

    # Only keep the required columns to cut down on total data size
    cols_to_keep = ["reference_site", "wildtype",
                    "mutant", metric_col, "epitope"]

    # Add filter columns to required columns
    if filter_cols:
        # Get the current names of the columns
        filter_column_names = [col for col in filter_cols.keys()]
        # Make sure the filter columns are actually in the dataframe at this point
        missing_filter_columns = set(
            filter_column_names) - set(mut_metric_df.columns)
        if missing_filter_columns:
            raise ValueError(
                f"The filter column(s): {missing_filter_columns} are not present in the data.")
        # Make sure that filter columns are numeric
        for col in filter_column_names:
            try:
                pd.to_numeric(mut_metric_df[col])
            except ValueError:
                raise ValueError(
                    f"The column {col} contains values that cannot be coerced into numbers.")
        # Make sure that the filter columns don't have spaces in them
        for col in filter_column_names:
            if " " in col:
                raise ValueError(
                    f"There is a space in {col}. Please remove this.")

        cols_to_keep += filter_column_names

    # Add tooltip columns to required columns
    if tooltip_cols:
        # Make sure the filter columns are actually in the dataframe at this point
        missing_tooltip_columns = set(
            tooltip_cols) - set(mut_metric_df.columns)
        if missing_tooltip_columns:
            raise ValueError(
                f"The tooltip column(s): {missing_tooltip_columns} are not present in the data.")
        cols_to_keep += tooltip_cols

    # Subset the mutation dataframe
    mut_metric_df = mut_metric_df[cols_to_keep]

    # Check that all mutant and wildtype residue names are in the provided alphabet
    mut_metric_alphabet = set(
        mut_metric_df.mutant.to_list() + mut_metric_df.wildtype.to_list())
    missing_amino_acids = mut_metric_alphabet - {aa for aa in alphabet}
    if missing_amino_acids:
        raise ValueError(
            f"Some of the wildtype or mutant amino acid names are not in the provided alphabet, i.e., {missing_amino_acids}")

    # Process some information about the protein structure
    _, ext = os.path.splitext(structure)

    if ext == '.pdb':
        # PDB is local, load it in as a string
        with open(structure, 'r') as f:
            pdb = f.read()
    else:
        pdb = structure

    # Add the included chains to the sitemap data if there are any
    sitemap_df['chains'] = sitemap_df['protein_site'].apply(
        lambda y: included_chains if str(y).isnumeric() else "")

    # Get a list of the epitopes and map these to the colors
    epitopes = list(set(mut_metric_df.epitope))
    if len(epitopes) > len(colors):
        raise ValueError(
            f"There are {len(epitopes)} epitopes, but only {len(colors)} color(s) specified. Please specify more colors.")
    epitope_colors = {epitope: colors[i] for i, epitope in enumerate(epitopes)}

    # Rename the metric column to the metric name
    if metric_name:
        mut_metric_df = mut_metric_df.rename(columns={metric_col: metric_name})
        metric_col = metric_name

    # Make a dictionary holding the experiment data
    dataset_dict = {
        'mut_metric_df': json.loads(mut_metric_df.to_json(orient='records')),
        'metric_col': metric_col,
        'sitemap': sitemap_df.set_index('reference_site').to_dict(orient='index'),
        'alphabet': [aa for aa in alphabet],
        'pdb': pdb,
        'dataChains': included_chains.split(" "),
        'excludeChains': excluded_chains.split(" "),
        'epitopes': epitopes,
        'epitope_colors': epitope_colors,
        'filter_cols': filter_cols
    }

    return dataset_dict


if __name__ == "__main__":

    # Command line interface
    parser = argparse.ArgumentParser(
        description="""Create a JSON file from protein site- and mutation-level data for 
        visualizing with https://dms-viz.github.io/. 
        
        e.g., python create-viz-json.py --input data.csv \
                                        --name "My Experiment" \
                                        --sitemap sitemap.csv \
                                        --metric "fitness" \
                                        --output data.json
        """
    )

    # Required arguments - input data, name, sitemap, metric, and structure
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to a csv with site- and mutation-level data to visualize on a protein structure.",
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Name of the experiment/selection for the tool.",
    )
    parser.add_argument(
        "--sitemap",
        type=str,
        required=True,
        help="Path to a csv containing a map between reference sites in the experiment and sequential sites.",
    )
    parser.add_argument(
        "--metric",
        type=str,
        required=True,
        help="Name of the column that contains the value to visualize on the protein structure.",
    )
    parser.add_argument(
        "--structure",
        type=str,
        required=False,
        help="Optionally, an RSCB PDB ID if using a structure that can be fetched directly from the PDB.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to save the *.json file containing the data for the visualization tool.",
    )
    # Optional configuration arguments
    parser.add_argument(
        "--metricName",
        type=str,
        required=False,
        help="Optionally, the name that should show up for your metric in the plot.",
    )
    parser.add_argument(
        "--joinData",
        type=str,
        required=False,
        help="Optionally, a csv with functional scores to join to the visualization data. Column with the scores should be called 'effect'.",
    )
    parser.add_argument(
        "--tooltipCols",
        type=str,
        required=False,
        help="Optionally, a list of column names to use as filters in the visualization.",
    )
    parser.add_argument(
        "--filterCols",
        type=str,
        required=False,
        help="Optionally, a list of column names to use as filters in the visualization.",
    )
    parser.add_argument(
        "--includedChains",
        type=str,
        required=False,
        help="Optionally, if not mapping data to every chain, a space separated list of chain names (i.e. 'C F M G J P').",
    )
    parser.add_argument(
        "--excludedChains",
        type=str,
        required=False,
        help="Optionally, a space separated string of chains that should not be shown on the protein structure (i.e. 'B L R').",
    )
    parser.add_argument(
        "--alphabet",
        type=str,
        required=False,
        help="Optionally, a string with no spaces containing all the mutations in your experiment and their desired order.",
    )
    parser.add_argument(
        "--colors",
        type=str,
        required=False,
        help="Optionally, a list of colors for representing different epitopes.",
    )

    args = parser.parse_args()

    # Read in the main mutation data
    mut_metric_df = pd.read_csv(args.input)
    # Split the list of join data files and read them in as a list
    if args.joinData:
        join_data_dfs = [pd.read_csv(join_data_file)
                         for join_data_file in args.joinData.split(",")]
    # Read in the sitemap data
    sitemap_df = pd.read_csv(args.sitemap)
    # Get the filter columns and parse dict from JSON
    if args.filterCols:
        filter_cols = json.loads(args.filterCols.replace("'", "\""))
    # Get the tooltip columns and parse dict from JSON
    if args.tooltipCols:
        tooltip_cols = json.loads(args.tooltipCols.replace("'", "\""))

    # Create the dictionary to save as a json
    output_dict = format_input_for_json(mut_metric_df,
                                        args.metric,
                                        sitemap_df,
                                        args.structure,
                                        join_data_dfs if args.joinData else None,
                                        filter_cols if args.filterCols else None,
                                        tooltip_cols if args.tooltipCols else None,
                                        args.metricName if args.metricName else None,
                                        args.includedChains if args.includedChains else "polymer",
                                        args.excludedChains if args.excludedChains else "none",
                                        args.alphabet if args.alphabet else "RKHDEQNSTYWFAILMVGPC-*",
                                        args.colors if args.colors else ['#0072B2', '#CC79A7',
                                                                         '#4C3549', '#009E73']
                                        )

    # Write the dictionary to a json file
    with open(args.output, 'w') as f:
        json.dump({args.name: output_dict}, f)
