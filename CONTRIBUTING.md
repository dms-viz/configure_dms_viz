# CONTRIBUTING to configure_dms_viz

Hello and thank you for your interest in contributing to `configure_dms_viz`! Here's how you can help.

## Getting Started:

### 1. Set Up Your Environment:

We use [`Poetry`](https://python-poetry.org/) for dependency management and packaging. If you don't have it installed, get it [here](https://python-poetry.org/docs/#installation).

### 2. Fork the Repository:

Before you start making changes, fork the repository to your own GitHub account.

### 3. Clone Your Fork:

Clone your forked repository to your local machine.

```bash
git clone https://github.com/dms-viz/configure_dms_viz.git
cd configure_dms_viz
```

### 4. Install Dependencies:

With `Poetry`, setting up the project environment and installing dependencies is easy:

```bash
poetry install
```

## Contributing Guidelines:

### 1. Work on a New Branch:

Don't work directly on the main branch. Create a new branch for your feature or bug fix.

```bash
git checkout -b your-new-feature-or-fix
```

### 2. Document Your Changes:

Make sure to comment your code appropriately. If you're introducing a new feature or making significant changes, update the README.md file as necessary.

### 3. Commit Your Changes:

Make granular commits with meaningful commit messages. This makes it easier to review your contributions.

### 4. Push to Your Fork:

Push the changes to your forked repository.

```bash
git push origin your-new-feature-or-fix
```

### 5. Testing your code

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

### 6. Create a Pull Request:

Once you're done with your changes and you think it's ready for review, create a pull request from your forked repository to the original repository.

## Code Formatting

The code is formatted using `Black`, which will be installed as a development dependence by `Poetry`. Linting is handled by `Ruff`, which will also be installed by `Poetry`.
