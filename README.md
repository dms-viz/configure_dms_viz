# `configure_dms_viz`

![License](https://img.shields.io/github/license/matsengrp/multidms)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

---

## Overview

`configure_dms_viz` is a python command line utility that formats your data for the visualization tool [`dms-viz`](https://dms-viz.github.io/). [`dms-viz`](https://dms-viz.github.io/) is a tool that helps you take quantitative data associated with mutations to a protein and analyze that data using intuitive visual summaries and an interactive 3D protein structure. Visualizations created with dms-viz are **flexible**, **customizable**, and **shareable**.

For more information on getting started with `dms-viz`, check out the [documentation](https://dms-viz.github.io/dms-viz-docs/).

## Prerequisites

To use `configure-dms-viz`, you must ensure that you have the correct version of `Python` (`>= 3.9`) installed on your operating system. You can check this by running:

```bash
python --version
```

The version number displayed should `>= 3.9.x`.

## Installation

`configure-dms-viz` is distributed on [PyPI](https://pypi.org/), allowing you to install `configure-dms-viz` using `pip`. To install the latest version of `configure-dms-viz`, run the following command:

```bash
pip install configure-dms-viz
```

`configure-dms-viz` should now be installed. You can double-check that the installation worked by running the following command:

```bash
configure-dms-viz --help
```

You should see a help message printed to the terminal.

## Basic Usage

`configure_dms_viz` takes input data consisting of a quantitative metric associated with mutations to a protein sequence and returns a `.json` specification file that is uploaded to [`dms-viz`](https://dms-viz.github.io/) to create an interactive visualization. Below is a simple tutorial on `configure-dms-viz`; however, for a detailed guide to the `configure-dms-viz` API, check out the [documentation](https://dms-viz.github.io/dms-viz-docs/preparing-data/command-line-api/).

`configure-dms-viz` has two commands, `format` and `join`. To format a single dataset for `dms-viz`, you execute the `configure-dms-viz format` command with the required and optional arguments as needed:

```bash
configure-dms-viz format \
    --name <experiment_name> \
    --input <input_csv> \
    --metric <metric_column> \
    --structure <pdb_structure> \
    --output <output_json> \
    [optional_arguments]
```

The information that is required to make a visualization file for **`dms-viz`** is as follows:

1. `--name`: The name of your dataset as you'd like it to appear in the visualization.
2. `--input`: The file path to your input data.
3. `--metric`: The name of the column that contains the metric you want to visualize.
4. `--structure`: The protein structure that you want to use as a 3D model.
5. `--output`: The file path of the output `.json` file.

The remaining arguments are _optional_ and configure the protein, appearance, and data included in your final visualization.

Now, let's use `configure-dms-viz` with a minimal example. The example data is included in this GitHub repository under `tests/`. If you want to follow along, clone the repository and run the following command from the root of the directory.

### Input

```bash
configure-dms-viz format \
   --name "REGN mAb Cocktail" \
   --input tests/SARS2-RBD-REGN-DMS/input/REGN_escape.csv \
   --metric "mut_escape" \
   --metric-name "Escape" \
   --sitemap tests/SARS2-RBD-REGN-DMS/sitemap/sitemap.csv \
   --structure "6XDG" \
   --included-chains "E" \
   --condition "condition" \
   --condition-name "Antibody" \
   --output ./REGN_escape.json
```

First, we've specified that we want the _name_ of the dataset as it appears in `dms-viz` to be `REGN mAb Cocktail` (named after the Regeneron Antibody cocktail therapuetic for SARS-CoV-2). This isn't so crucial when there is only a single dataset; however, when combining multiple datasets with the `join` command, it's necessary to have unique and descriptive names.

Next, we've pointed to the [input data](https://github.com/dms-viz/configure_dms_viz/blob/main/tests/SARS2-RBD-REGN-DMS/input/REGN_escape.csv) containing quantitative scores that measure the degree of antibody escape from the `REGN mAb Cocktail`. For details on the specific requirements for input data, check out the [Data Requirements](https://dms-viz.github.io/dms-viz-docs/preparing-data/data-requirements/) guide in the documentation. In addition to specifying the input data, we told `configure-dms-viz` which column contains the escape scores (`mut_escape`) and what to call that column in the plots (`Escape`).

Then, we've specified a [sitemap](https://github.com/dms-viz/configure_dms_viz/blob/main/tests/SARS2-RBD-REGN-DMS/sitemap/sitemap.csv). This is optional information that describes how the sites in your input data correspond to your 3D protein structure. If you do not provide a sitemap, the sites in the input data are assumed to correspond one-to-one with the sites in the protein structure.

After that, we specified a protein structure. In this case, we're fetching `6XDG` from the [RSCB PDB](https://www.rcsb.org/) and only showing our data on chain `E` of that structure.

Finally, in this particular dataset, we have multiple 'conditions' for each mutation; this means there are multiple measurements (`mut_escape`) for each mutation/position (corresponding to escape from different antibodies). We need to specify the column that contains these `condition`s. In `dms-viz`, an interactive legend will let you toggle between conditions.

The result of this command should be a message printed to the terminal providing some basic information from the `configure-dms-viz format` command that looks like this:

**Output**

```md
Formatting data for visualization using the 'mut_escape' column from 'tests/SARS2-RBD-REGN-DMS/input/REGN_escape.csv'...

Using sitemap from 'tests/SARS2-RBD-REGN-DMS/sitemap/sitemap.csv'.

'protein_site' column is not present in the sitemap. Assuming that the reference sites correspond to protein sites.

About 95.98% of the wildtype residues in the data match the corresponding residues in the structure.
About 4.02% of the data sites are missing from the structure.

Success! The visualization JSON was written to './REGN_escape.json'
```

That's how you use `configure-dms-viz` to format a single dataset! You can also combine multiple datasets into a single `.json` specification file using the `configure-dms-viz join` command. For more details on combining datasets to jointly visualize with `dms-viz`, check out the [API](https://dms-viz.github.io/dms-viz-docs/preparing-data/command-line-api/#configure-dms-viz-join).

## Developing

`configure-dms-viz` was developed using `Python` (>=3.9) and the [`click`](https://click.palletsprojects.com/en/8.1.x/) library.

To contribute to `configure-dms-viz`, follow the instructions [here](https://dms-viz.github.io/dms-viz-docs/project-info/contributing-guide/#contributing-to-configure-dms-viz) for setting up a development environment.

### Testing

[`pytest`](https://docs.pytest.org/en/8.0.x/) is the testing framework for `configure-dms-viz`.

The command line interface (CLI) of `configure-dms-viz` is tested using four example datasets from different projects and labs that cover 100% of its flags and features. These four examples are:

1. [Deep mutational scanning of the SARS-CoV-2 Spike protein](/tests/SARS2-Omicron-BA1-DMS/README.md)
   Authors: **Bernadeta Dadonaite**, **Katharine H D Crawford**, **Caelan E Radford**, Ariana G Farrell, Timothy C Yu, William W Hannon, Panpan Zhou, Raiees Andrabi, Dennis R Burton, Lihong Liu, David D. Ho, Richard A. Neher, **Jesse D Bloom**
   Manuscript: https://www.sciencedirect.com/science/article/pii/S0092867423001034?via%3Dihub

2. [Deep mutational scanning of the HIV BF520 strain Envelope protein](/tests/HIV-Envelope-BF520-DMS/README.md)
   Authors: **Caelan E. Radford**, Philipp Schommers, Lutz Gieselmann, Katharine H. D. Crawford, Bernadeta Dadonaite, Timothy C. Yu, Adam S. Dingens, Julie Overbaugh, Florian Klein, **Jesse D. Bloom**
   Manuscript: https://www.sciencedirect.com/science/article/pii/S1931312823002184?via%3Dihub

3. [Phylogenetic fitness estimates of every SARS-CoV-2 protein](/tests/SARS2-Mutation-Fitness/README.md)
   Authors: **Jesse D. Bloom**, **Richard A. Neher**
   Manuscript: https://www.biorxiv.org/content/10.1101/2023.01.30.526314v2

4. [Deep mutational scanning of the Influenza PB1 polymerse subunit](/tests/IAV-PB1-DMS/README.md)
   Authors: **Yuan Li**, Sarah Arcos, Kimberly R. Sabsay, Aartjan J.W. te Velthuis, **Adam S. Lauring**
   Manuscript: https://www.biorxiv.org/content/10.1101/2023.08.27.554986v1.full

In addition to these test datasets, there are specific tests using dummy data for the key formatting functions. To run the tests, execute the following command from the root of the directory:

```
poetry run pytest
```
