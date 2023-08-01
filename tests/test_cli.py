import json
import pandas as pd
from os.path import join
import subprocess


def create_viz_json(
    escape_df,
    sitemap_df,
    functional_score_df,
    output_path,
    experiment_name,
    experiments,
):
    """
    Creates a visualization JSON file for a given experiment.

    Parameters
    ----------
    escape_df : str
        Path to the escape dataframe CSV.
    sitemap_df : str
        Path to the sitemap dataframe CSV.
    functional_score_df : str
        Path to the functional score dataframe CSV.
    output_path : str
        Path where the output JSON should be saved.
    experiment_name : str
        Name of the experiment.
    experiments : pd.DataFrame
        DataFrame containing experiments data.

    Returns
    -------
    None
        Executes a subprocess command and does not return any value.
    """
    structure = experiments.loc[
        experiments["selection"] == experiment_name, "pdb"
    ].item()
    include_chains = experiments.loc[
        experiments["selection"] == experiment_name, "dataChains"
    ].item()
    exclude_chains = experiments.loc[
        experiments["selection"] == experiment_name, "excludedChains"
    ].item()
    filter_cols = {"effect": "Functional Effect", "times_seen": "Times Seen"}
    tooltip_cols = {"times_seen": "# Obsv", "effect": "Func Eff."}
    metric = "escape_mean"
    metric_name = "Escape"
    condition = "epitope"
    condition_name = "Epitope"

    command = f""" 
    configure-dms-viz \
        --input {escape_df} \
        --name {experiment_name} \
        --sitemap {sitemap_df} \
        --metric {metric} \
        --structure {structure} \
        --metric-name {metric_name} \
        --output {output_path} \
        --condition {condition} \
        --condition-name {condition_name} \
        --join-data {functional_score_df} \
        --included-chains "{include_chains}" \
        --excluded-chains "{exclude_chains}" \
        --filter-cols "{filter_cols}" \
        --tooltip-cols "{tooltip_cols}" \
        --title "{experiment_name}" \
    """

    subprocess.run(command, shell=True)


def combine_jsons(input_files, output_file):
    """
    Combines multiple JSON files into a single file.

    Parameters
    ----------
    input_files : list of str
        List of paths to the input JSON files.
    output_file : str
        Path where the combined JSON should be saved.

    Returns
    -------
    None
        Writes combined data to a JSON file.
    """
    combined_data = {}
    for input_file in input_files:
        with open(input_file) as f:
            data = json.load(f)
            combined_data.update(data)
    with open(output_file, "w") as f:
        json.dump(combined_data, f)


if __name__ == "__main__":
    virus = "sars2"
    virus_dir = f"{virus}"
    output_dir = f"{virus}/output"
    data_dir = f"{virus}/escape"

    experiments = pd.read_csv(join(virus_dir, "experiments.csv"))
    sitemap_df_path = join(virus_dir, "site_numbering_map.csv")
    functional_score_df_path = join(virus_dir, "muteffects_observed.csv")

    json_files = []
    for experiment_name in experiments.selection.unique():
        escape_df_path = join(data_dir, f"{experiment_name}_avg.csv")
        output_json_path = join(output_dir, f"{experiment_name}.json")
        json_files.append(output_json_path)

        create_viz_json(
            escape_df_path,
            sitemap_df_path,
            functional_score_df_path,
            output_json_path,
            experiment_name,
            experiments,
        )

    combine_jsons(json_files, join(output_dir, f"{virus}.json"))
