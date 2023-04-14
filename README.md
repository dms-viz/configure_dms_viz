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
- Pandas
- Snakemake

We recommend using the `conda` package manager to set up a virtual environment and install the necessary tools. If you don't already have `conda`, you can download it from the [official website](https://docs.conda.io/en/latest/miniconda.html).

Create a new conda environment and install the required packages:

```bash
conda create -n dms_viz_env python=3.10.5
conda activate dms_viz_env
conda install -c conda-forge snakemake pandas
```

These commands will create a new conda environment called `dms_viz_env` with all the requirements needed to use this tool.

## Installation

Currently, the best way to use `configure_dms_viz` is by cloning the repository and using the script directly:

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

- `--input` <input_csv>: Path to a CSV file with site- and mutation-level data to visualize on a protein structure. [See details below](#input-data-format) for required columns and format.
- `--name` <experiment_name>: Name of the experiment/selection for the tool. For example, the antibody name or serum ID. This property is necessary for combining multiple experiments into a single file.
- `--sitemap` <sitemap_csv>: Path to a CSV file containing a map between reference sites in the experiment and sequential sites. [See details below](#input-data-format) for required columns and format.
- `--metric` <metric_column>: Name of the column that contains the value to visualize on the protein structure. This tells the tool which column you want to visualize on a protein strucutre.
- `--output` <output_json>: Path to save the \*.json file containing the data for the visualization tool.

**Optional configuration arguments**

- `--structure` <pdb_structure>: Either an RSCB PDB ID if using a structure that can be fetched directly from the PDB (i.e. `"6xr8"`). Or, a path to a locally downloaded PDB file (i.e. `./pdb/my_custom_structure.pdb`).
- `--metricName` <metric_name>: The name that should show up for your metric in the plot. This let's you customize the names of your columns in your visualization. For example, if your metric column is called `escape_mean` you can rename it to `Escape` for the visualization.
- `--joinData` <join_data_csv>: A CSV file with data to join to the visualization data. This data can then be used in the visualization tooltips or filters. [See details below](#input-data-format) for formatting requirements.
- `--tooltipCols` <column_names>: A dictionary that establishes the columns that you want to show up in the tooltip in the visualization (i.e. `"{'times_seen': '# Obsv', 'effect': 'Func Eff.'}"`).
- `--filterCols` <column_names>: A dictionary that establishes the columns that you want to use as filters in the visualization (i.e. `"{'effect': 'Functional Effect', 'times_seen': 'Times Seen'}"`).
- `--includedChains` <chain_names>: A space-delimited string of chain names that correspond to the chains in your PDB structure that correspond to the reference sites in your data (i.e., `'C F M G J P'`). This is only necesary if your PDB structure contains chains that you do not have site- and mutation-level measurements for.
- `--excludedChains` <chain_names>: A space-delimited string of chain names that should not be shown on the protein structure (i.e., `'B L R'`).
- `--alphabet` <mutation_string>: A string with no spaces containing all the amino acids in your experiment and their desired order (i.e. `"RKHDEQNSTYWFAILMVGPC-*"`).
- `--colors` <color_list>: A list of colors for representing different epitopes.

## Input Data Format

The main inputs for `configure_dms_viz` include the following example files located in the [tests directory](tests/sars2/):

1. An [**input CSV**](tests/sars2/escape/): Example CSV files containing site- and mutation-level data to visualize on a protein structure can be found in the `tests/sars2/escape` directory. The CSV must contain the following columns in addition to the specified _`metric_column`_:
   - `site` or `reference_site`: These will be the sites that show up on the x-axis of the visualization
   - `wildtype`: The wildtype amino acid at a given reference site
   - `mutant`: The mutant amino acid for a given measurement
   - `epitope`: If there are multiple measurements for the same site (i.e. multiple epitopes), a unique string deliniating these
2. A [**Sitemap**](tests/sars2/site_numbering_map): An example sitemap, which is a CSV file containing a map between reference sites on the protein and their sequential order, can be found at `tests/sars2/site_numbering_map`.
   - `reference_site`: This must correspond to the `site` or `reference_site` column in your `input csv`.
   - `sequential_site`: This is the sequential order of the reference sites and must be a numeric column.
   - `protein_site`: **Optional**, this column is only necessary if the `reference_site` sites are different from the sites in your PDB strucutre.
3. [**Join Data**](tests/sars2/muteffects_observed.csv): An example dataframe that you could join with your data, if desired, is provided at `tests/sars2/muteffects_observed.csv`. The CSV is joined to your `input CSV` by the `site`, `wildtype`, and `mutant` columns.

Make sure your input data follows the same format as the provided examples to ensure compatibility with the `configure_dms_viz` tool.

## Output Data Format

The output is a single JSON file per experiment that can be uploaded to [dms-viz](https://dms-viz.github.io/) for visualizing. You can combine these into a single JSON file if you want to visualize mulitple experiments in the same session.

## Examples

To see a detailed example, look in the provided `Snakefile`. You can run this example pipeline using the following command from within the `configure_dms_viz` directory:

```bash
snakemake --cores 1
```

The output should be located in the [tests](tests/sars2/) directory in a folder called `output`. You can upload the example output into [`dms-viz`](https://dms-viz.github.io/).

## Troubleshooting

If you have any questions formating your data or run into any issues with this tool, post a git issue in this repo.
