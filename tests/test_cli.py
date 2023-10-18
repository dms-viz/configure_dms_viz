"""Test the command line tool with pytest on a set of datasets."""

import os
import json
import pandas as pd
import subprocess
import pytest


def create_viz_json(input_df, sitemap_df, output_path, **kwargs):
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
    configure-dms-viz format \
        --input "{input_df}" \
        --sitemap "{sitemap_df}" \
        --output "{output_path}" \
    """
    for key, value in kwargs.items():
        command += f' --{key} "{value}"'
    subprocess.run(command, shell=True, check=True)


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
        Executes a subprocess command and does not return any value.
    """
    command = f"""
    configure-dms-viz join \
        --input "{', '.join(input_files)}" \
        --output "{output_file}" \
    """
    subprocess.run(command, shell=True, check=True)


@pytest.fixture(scope="module")
def test_datasets():
    return [
        "SARS2-Omicron-BA1-DMS",
        "IAV-PB1-DMS",
        "SARS2-Mutation-Fitness",
        "HIV-Envelope-BF520-DMS",
        "SARS2-RBD-REGN-DMS",
    ]


def test_create_viz_json(test_datasets):
    for dataset in test_datasets:
        datasets = pd.read_csv(f"tests/{dataset}/datasets.csv")
        viz_jsons = []
        for row in datasets.itertuples():
            arguments = {
                key.replace("_", "-"): value
                for key, value in row._asdict().items()
                if key not in ["input", "sitemap", "Index"]
            }
            output_path = f"tests/{dataset}/output/{row.name}.json"
            try:
                create_viz_json(row.input, row.sitemap, output_path, **arguments)
                viz_jsons.append(output_path)
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Command failed with error: {e}")

        try:
            combine_jsons(
                viz_jsons, os.path.join(f"tests/{dataset}/output/", f"{dataset}.json")
            )
        except Exception as e:
            pytest.fail(f"Combining JSON files failed with error: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
