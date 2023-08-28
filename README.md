# `configure_dms_viz`

![License](https://img.shields.io/github/license/matsengrp/multidms)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

---

`configure_dms_viz` is a python utility created by the [Bloom Lab](https://research.fredhutch.org/bloom/en.html?gad=1&gclid=CjwKCAjw_aemBhBLEiwAT98FMrUu0b-uBYBHLlkGqcFPG2hLq7HMGbYTnmcHATXLYrHMckohVI-ClhoCkxgQAvD_BwE) that configures your data for the web-based visualization tool [dms-viz](https://dms-viz.github.io/).

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

## Installation

Before using `configure_dms_viz`, ensure that you have the following software installed:

- python >=3.10
- pip

You can use the python package manager `pip` to install `configure_dms_viz` like so:

```bash
pip install configure-dms-viz
```

You can check that the installation worked by running:

```bash
configure-dms-viz --help
```

## Usage

To use `configure_dms_viz`, execute the `configure-dms-viz` command with the required and optional arguments as needed:

```bash
configure-dms-viz \
    --name <experiment_name> \
    --input <input_csv> \
    --sitemap <sitemap_csv> \
    --metric <metric_column> \
    --structure <pdb_structure> \
    --output <output_json> \
    [optional_arguments]
```

### Arguments

**Required arguments**

- `--input` <string>: Path to a CSV file with site- and mutation-level data to visualize on a protein structure. [See details below](#input-data-format) for required columns and format.
- `--name` <string>: Name of the experiment/selection for the tool. For example, the antibody name or serum ID. This property is necessary for combining multiple experiments into a single file.
- `--sitemap` <string>: Path to a CSV file containing a map between reference sites in the experiment and sequential sites. [See details below](#input-data-format) for required columns and format.
- `--metric` <string>: Name of the column that contains the value to visualize on the protein structure. This tells the tool which column you want to visualize on a protein strucutre.
- `--structure` <string>: Either an RSCB PDB ID if using a structure that can be fetched directly from the PDB (i.e. `"6xr8"`). Or, a path to a locally downloaded PDB file (i.e. `./pdb/my_custom_structure.pdb`).
- `--output` <string>: Path to save the \*.json file containing the data for the visualization tool.

**Optional configuration arguments**

- `--condition` <string>: If there are multiple measurements per mutation, the name of the column that contains that condition distinguishing these measurements.
- `--metric-name` <string>: The name that will show up for your metric in the plot. This let's you customize the names of your columns in your visualization. For example, if your metric column is called `escape_mean` you can rename it to `Escape` for the visualization.
- `--conditon_name` <string>: The name that will show up for your condition column in the title of the plot legend. For example, if your condition column is 'epitope', you might rename it to be capilized as 'Epitope' in the legend title.
- `--join-data` <list>: A comma separated list of CSV file with data to join to the visualization data. This data can then be used in the visualization tooltips or filters. [See details below](#input-data-format) for formatting requirements.
- `--tooltip-cols` <dict>: A dictionary that establishes the columns that you want to show up in the tooltip in the visualization (i.e. `"{'times_seen': '# Obsv', 'effect': 'Func Eff.'}"`).
- `--filter-cols` <dict>: A dictionary that establishes the columns that you want to use as filters in the visualization (i.e. `"{'effect': 'Functional Effect', 'times_seen': 'Times Seen'}"`).
- `--included-chains` <string>: A space-delimited string of chain names that correspond to the chains in your PDB structure that correspond to the reference sites in your data (i.e., `'C F M G J P'`). This is only necesary if your PDB structure contains chains that you do not have site- and mutation-level measurements for.
- `--excluded-chains` <string>: A space-delimited string of chain names that should not be shown on the protein structure (i.e., `'B L R'`).
- `--alphabet` <string>: A string with no spaces containing all the amino acids in your experiment and their desired order (i.e. `"RKHDEQNSTYWFAILMVGPC-*"`).
- `--colors` <list>: A comma separated list of HEX format colors for representing different conditions, i.e. `"#0072B2, #CC79A7, #4C3549, #009E73"`.
- `--negative-colors` <list>: A comma separated list of HEX format colors for representing the negative end of the scale for different conditions, i.e. `"#0072B2, #CC79A7, #4C3549, #009E73"`. If not provided, the inverse of each color is automatically calculated.
- `--check-pdb` <bool>: Whether to perform checks on the provided pdb structure including checking if the 'included chains' are present, what % of data sites are missing, and what % of wildtype residues in the data match at corresponding sites in the structure.
- `--exclude-amino-acids` <list>: A comma separated list of amino acids that shouldn't be used to calculate the summary statistics (i.e. "\*, -")
- `--description` <string>: A short description of the dataset that will show up in the tool if the user clicks a button for more information.
- `--title` <string>: A short title to appear above the plot.

## Input Data Format

The main inputs for `configure_dms_viz` include the following example files located in the [tests directory](tests/sars2/):

1. An [**input CSV**](tests/sars2/escape/): Example CSV files containing site- and mutation-level data to visualize on a protein structure can be found in the `tests/sars2/escape` directory. The CSV must contain the following columns in addition to the specified _`metric_column`_:
   - `site` or `reference_site`: These will be the sites that show up on the x-axis of the visualization.
   - `wildtype`: The wildtype amino acid at a given reference site.
   - `mutant`: The mutant amino acid for a given measurement.
   - `condition`: _Optionally_, if there are multiple measurements for the same site (i.e. multiple epitopes), a unique string deliniating these measurements.
2. A [**Sitemap**](tests/sars2/site_numbering_map.csv): An example sitemap, which is a CSV file containing a map between reference sites on the protein and their sequential order, can be found at `tests/sars2/site_numbering_map`.
   - `reference_site`: This must correspond to the `site` or `reference_site` column in your `input csv`.
   - `sequential_site`: This is the sequential order of the reference sites and must be a numeric column.
   - `protein_site`: **Optional**, this column is only necessary if the `reference_site` sites are different from the sites in your PDB strucutre.
3. Optional [**Join Data**](tests/sars2/muteffects_observed.csv): An example dataframe that you could join with your data, if desired, is provided at `tests/sars2/muteffects_observed.csv`. The CSV is joined to your input CSV by the `site`, `wildtype`, and `mutant` columns.

Make sure your input data follows the same format as the provided examples to ensure compatibility with the `configure_dms_viz` tool.

## Output Data Format

The output is a single JSON file per experiment that can be uploaded to [dms-viz](https://dms-viz.github.io/) for visualizing. You can combine these into a single JSON file if you want to visualize mulitple experiments in the same session.

## Examples

An example dataset is included within the [`tests`](tests/sars2/) directory of the repo. After installing the tool, you can run the following example:

```bash
configure-dms-viz \
   --name LyCoV-1404 \
   --input tests/sars2/escape/LyCoV-1404_avg.csv \
   --sitemap tests/sars2/site_numbering_map.csv \
   --metric escape_mean \
   --structure 6xr8 \
   --output LyCoV-1404.json \
   --metric-name Escape \
   --join-data tests/sars2/muteffects_observed.csv \
   --filter-cols "{'effect': 'Functional Effect', 'times_seen': 'Times Seen'}" \
   --tooltip-cols "{'times_seen': '# Obsv', 'effect': 'Func Eff.'}"
```

To an example of what this would look like applied over multiple datasets, look in the provided [`Snakefile`](./Snakefile). You can run this example pipeline using the following command from within the `configure_dms_viz` directory:

```bash
snakemake --cores 1
```

The output will be located in the [tests](tests/sars2/) directory in a folder called `output`. You can upload the example output into [`dms-viz`](https://dms-viz.github.io/).

## Troubleshooting

If you have any questions formating your data or run into any issues with this tool, post a git issue in this repo.
