#!/usr/bin/env python
import argparse
import json
import pandas as pd


def format_input_for_json(mut_metric_df,
                          metric_col,
                          sitemap_df,
                          mut_effect_df=None,
                          filter_cols=None,
                          structure=None,
                          included_chains="polymer",
                          excluded_chains="none",
                          alphabet="RKHDEQNSTYWFAILMVGPC-*",
                          colors=['#0072B2', '#CC79A7', '#4C3549', '#009E73']
                          ):
    """
    Take site-level and mutation-level measurements and format into 
    a JSON file for interactive visualization with `dms-viz`. 

    Prameters
    ---------
    mut_metric_df: pandas.DataFrame
        A dataframe containig site- and mutation-level data for visualization. 
    metric_col: str
        The name of the column the contains the metric for visualization.
    sitemap_df: pandas.DataFrame
        A dataframe mapping data sites to reference sites to protein sites. 
    structure: str or None 
        An RCSB PDB ID (i.e. 6UDJ) if not using a custom strucutre.
    included_chains: str or None
        If not mapping data to every chain, a space separated list of chain names (i.e. "C F M G J P").
    excluded_chains: str or None
        A space separated string of chains that should not be shown on the protein structure (i.e. "B L R").
    mut_effect_df: pandas.dataFrame or None
        A dataframe of functional effects to join to the main dataframe by mutation. 
    filter_cols: list or None
        A list of column names to designate as filters in the visualization. 
    alphabet: str
        The amino acid labels in the order the should be displayed on the heatmap. 
    colors: list
        A list of colors that will be used for each epitope in the experiment.

    Returns
    -------
    dict
        A dictionary containing the data for visualization to convert into a JSON file.
    """

    # Check that there are reference sites in the mutation data
    if not mut_metric_df.columns.isin(['site', 'reference_site']).any():
        raise ValueError(
            "The mutation dataframe is missing either the site or reference_site column.")

    # Check that required columns are present in the mutation data
    missing_mutation_columns = {'epitope', 'site', 'wildtype',
                                'mutant', 'mutation', metric_col} - set(mut_metric_df.columns)
    if missing_mutation_columns:
        raise ValueError(
            f"The following columns do not exist in the mutation metric data: {list(missing_mutation_columns)}")

    # Check that required columns are present in the sitemap data
    missing_sitemap_columns = {'sequential_site',
                               'reference_site'} - set(sitemap_df.columns)
    if missing_sitemap_columns:
        raise ValueError(
            f"The following columns do not exist in the sitemap: {list(missing_sitemap_columns)}")

    # If the protein site isn't specified, assume that it's the same as the reference site
    if 'protein_site' not in sitemap_df.columns:
        sitemap_df['protein_site'] = sitemap_df['reference_site'].apply(
            lambda y: y if y.isnumeric() else "")
    else:
        # Make sure that the provided column has no invalid values
        if not sitemap_df['protein_site'].apply(lambda y: y == "" or y.isnumeric()).all():
            raise ValueError(
                "The protein_site column of the sitemap contains invalid values.")

    # Add the included chains to the sitemap data if there are any
    sitemap_df['chains'] = sitemap_df['protein_site'].apply(
        lambda y: included_chains if y.isnumeric() else "")

    # Get a list of the epitopes and map these to the colors
    epitopes = list(set(mut_metric_df.epitope))
    if len(epitopes) > len(colors):
        raise ValueError(
            f"There are {len(epitopes)} epitopes, but only {len(colors)} color(s) specified. Please specify more colors.")
    epitope_colors = {epitope: colors[i] for i, epitope in enumerate(epitopes)}

    # Join optional columns to the mutation metric data
    if mut_effect_df is not None:
        # Check that the necessary columns are present
        missing_effect_columns = {
            'wildtype', 'reference_site', 'mutant', 'effect'} - set(mut_effect_df.columns)
        if missing_effect_columns:
            raise ValueError(
                f"The following columns do not exist in the functional data: {list(missing_effect_columns)}")
        # Join to the main metric data
        mut_effect_df['mutation'] = mut_effect_df.apply(
            lambda row: row.wildtype + row.reference_site + row.mutant, axis=1)
        mut_metric_df = pd.merge(mut_metric_df, mut_effect_df[[
                                 'mutation', 'effect']].drop_duplicates(), on='mutation')
        mut_metric_df = mut_metric_df.rename(columns={"effect": "func_effect"})

    # If there are columns to filter by, make sure that these are present in the data and numeric
    if filter_cols:
        missing_filter_columns = set(filter_cols) - set(mut_metric_df.columns)
        if missing_filter_columns:
            raise ValueError(
                f"The filter column(s): {missing_filter_columns} are not present in the data.")

    # Make a dictionary holding the experiment data
    experiment_dict = {
        'mut_escape_df': json.loads(mut_metric_df.to_json(orient='records')),
        'sitemap': sitemap_df.set_index('reference_site').to_dict(orient='index'),
        'alphabet': [aa for aa in alphabet],
        'pdb': structure,
        'dataChains': included_chains.split(" "),
        'excludeChains': excluded_chains.split(" "),
        'epitopes': epitopes,
        'epitope_colors': epitope_colors,
        'filter_cols': filter_cols
    }

    return experiment_dict


if __name__ == "__main__":

    # Command line interface
    parser = argparse.ArgumentParser(
        description="""Create a JSON file from protein site- and mutation-level data for 
        visualizing with https://dms-viz.github.io/.
        
        e.g., python create-viz-json.py -i mut_escape.csv -o output.json 
        """
    )

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
        "--output",
        type=str,
        required=True,
        help="Path to save the *.json file containing the data for the visualization tool.",
    )
    parser.add_argument(
        "--funcScores",
        type=str,
        required=False,
        help="Optionally, a csv with functional scores to join to the visualization data. Column with the scores should be called 'effect'.",
    )
    parser.add_argument(
        "--filterCols",
        type=str,
        required=False,
        help="Optionally, a list of column names to use as filters in the visualization.",
    )
    parser.add_argument(
        "--structure",
        type=str,
        required=False,
        help="Optionally, an RSCB PDB ID if using a structure that can be fetched directly from the PDB.",
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

    args = parser.parse_args()

    # Create the dictionary to save as a json
    output_dict = format_input_for_json(pd.read_csv(args.input),
                                        args.metric,
                                        pd.read_csv(args.sitemap),
                                        pd.read_csv(
                                            args.funcScores) if args.funcScores else None,
                                        args.filterCols.split(
                                            ",") if args.filterCols else None,
                                        args.structure if args.structure else None,
                                        args.includedChains if args.includedChains else "polymer",
                                        args.excludedChains if args.excludedChains else "none",
                                        alphabet="RKHDEQNSTYWFAILMVGPC-*",
                                        colors=['#0072B2', '#CC79A7',
                                                '#4C3549', '#009E73']
                                        )

    # Write the dictionary to a json file
    with open(args.output, 'w') as f:
        json.dump({args.name: output_dict}, f)
