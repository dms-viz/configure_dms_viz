"""Test the command line tool by running this script. To run the script, type `poetry run python tests/test_cli.py.`"""

import os
import json
import pandas as pd
import subprocess


def create_viz_json(
    input_df,
    sitemap_df,
    output_path,
    **kwargs,
):
    """
    Creates a visualization JSON file for a given experiment/dataset.

    Parameters
    ----------
    input_df : str
        Path to the input dataframe CSV (--input).
    sitemap_df : str
        Path to the sitemap dataframe CSV (--sitemap).
    output_path : str
        Path to the output path JSON (--output).

    Returns
    -------
    None
        Executes a subprocess command and does not return any value.
    """

    command = f"""
    configure-dms-viz \
        --input "{input_df}" \
        --sitemap "{sitemap_df}" \
        --output "{output_path}" \
    """

    for key, value in kwargs.items():
        command += f' --{key} "{value}"'

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
    # Test Datsets
    test_datasets = [
        "SARS2-Omicron-BA1-DMS",
        "IAV-PB1-DMS",
        "SARS2-Mutation-Fitness",
        "HIV-Envelope-BF520-DMS",
    ]
    # Test the command line tool for each dataset
    for dataset in test_datasets:
        print("Testing:", dataset, "\n")
        # Read in the datasets.csv
        datasets = pd.read_csv(f"tests/{dataset}/datasets.csv")
        # Create a visualization JSON for each dataset
        viz_jsons = []
        for row in datasets.itertuples():
            # Get the arguments for the command line tool
            arguments = {
                key.replace("_", "-"): value
                for key, value in row._asdict().items()
                if key not in ["input", "sitemap", "Index"]
            }
            output_path = f"tests/{dataset}/output/{row.name}.json"
            # Create the visualization JSON
            create_viz_json(row.input, row.sitemap, output_path, **arguments)
            viz_jsons.append(output_path)
            # Join the visualization JSONs into a single JSON
            combine_jsons(
                viz_jsons, os.path.join(f"tests/{dataset}/output/", f"{dataset}.json")
            )
