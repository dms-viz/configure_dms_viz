# `configure_dms_viz`

`configure_dms_viz` is a python utility for configuring an input file for the visualization tool [dms-viz](https://dms-viz.github.io/).

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Input Data Format](#input-data-format)
- [Output Data Format](#output-data-format)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Introduction

`configure_dms_viz` is a command-line tool designed to create a JSON file for the web-based visualization tool [`dms-viz`](https://dms-viz.github.io/). You can use [`dms-viz`](https://dms-viz.github.io/) to visualize site-level mutation data in the context of a 3D protein structure. With `configure_dms_viz`, users can generate a compatible JSON file that can be uploaded to the [`dms-viz`](https://dms-viz.github.io/) website for interactive analysis of their protein mutation data.

## Prerequisites

Before using `configure_dms_viz`, ensure that you have the following software installed:

- Python version 3.10.5 or higher
- Snakemake
- Pandas

We recommend using the `conda` package manager to set up a virtual environment and install the necessary tools. If you don't already have `conda`, you can download it from the [official website](https://docs.conda.io/en/latest/miniconda.html).

Create a new conda environment and install the required packages:

```bash
conda create -n dms_viz_env python=3.10.5
conda activate dms_viz_env
conda install -c conda-forge snakemake pandas
```

These commands will create a new conda environment called `dms_viz_env` with all the requirements need to use this tool.

## Installation

Currently, the best way to use `configure_dms_viz` is by cloning the repository:

```bash
git clone https://github.com/yourusername/configure_dms_viz.git
cd configure_dms_viz
```

In the future, we plan to make this tool available as a package that can be installed via pip or conda.

## Usage

To use `configure_dms_viz`, execute the `configure-dms-viz.py` script with the required and optional arguments as needed:

```bash
python configure-dms-viz.py \
    --input <input_csv> \
    --name <experiment_name> \
    --sitemap <sitemap_csv> \
    --metric <metric_column> \
    --output <output_json> \
    [optional_arguments]
```

### Arguments

**Required arguments**

- `--input` <input_csv>: Path to a CSV file with site- and mutation-level data to visualize on a protein structure.
- `--name` <experiment_name>: Name of the experiment/selection for the tool.
- `--sitemap` <sitemap_csv>: Path to a CSV file containing a map between reference sites in the experiment and sequential sites.
- `--metric` <metric_column>: Name of the column that contains the value to visualize on the protein structure.
- `--output` <output_json>: Path to save the \*.json file containing the data for the visualization tool.

**Optional configuration arguments**

- `--structure` <pdb_id>: An RSCB PDB ID if using a structure that can be fetched directly from the PDB.
- `--metricName` <metric_name>: The name that should show up for your metric in the plot.
- `--joinData` <join_data_csv>: A CSV file with functional scores to join to the visualization data. Column with the scores should be called 'effect'.
- `--tooltipCols` <column_names>: A list of column names to use as filters in the visualization.
- `--filterCols` <column_names>: A list of column names to use as filters in the visualization.
- `--includedChains` <chain_names>: If not mapping data to every chain, a space-separated list of chain names (i.e., 'C F M G J P').
- `--excludedChains` <chain_names>: A space-separated string of chains that should not be shown on the protein structure (i.e., 'B L R').
- `--alphabet` <mutation_string>: A string with no spaces containing all the mutations in your experiment and their desired order.
- `--colors` <color_list>: A list of colors for representing different epitopes.

## Input Data Format

The main inputs for `configure_dms_viz` include the following example files located in the [tests directory](tests/sars2/):

1. An [**input CSV**](tests/sars2/escape/): Example CSV files containing site- and mutation-level data to visualize on a protein structure can be found in the `tests/sars2/escape` directory.
2. A [**Sitemap**](tests/sars2/site_numbering_map): An example sitemap, which is a CSV file containing a map between reference sites in the experiment and sequential sites, can be found at `tests/sars2/site_numbering_map`.
3. [**Join Data**](tests/sars2/muteffects_observed.csv): An example dataframe that you could join with your data, if desired, is provided at `tests/sars2/muteffects_observed.csv`.

Make sure your input data follows the same format as the provided examples to ensure compatibility with the `configure_dms_viz` tool.

## Output Data Format

The output is a single JSON file per experiment that can be uploaded to [dms-viz](https://dms-viz.github.io/) for visualizing.

## Examples

To see a detailed example, look in the provided `Snakefile`. You can run this example pipeline using the following command from within the `configure_dms_viz` directory:

```bash
snakemake --cores 1
```

The output should be located in the [tests](tests/sars2/) directory in a folder called `output`. You can upload the example output into [`dms-viz`](https://dms-viz.github.io/).

## Troubleshooting

If you have any questions formating your data or run into any issues with this tool, post a git issue in this repo.
