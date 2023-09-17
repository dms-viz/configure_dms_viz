# Testing `configure-dms-viz`

The command line interface (CLI) of `configure-dms-viz` is tested using four example datasets from different projects and labs that cover 100% of its flags and features. The testing framework used is `pytest`.

These four examples are:

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

## Run Tests

This section will contain details on how to run the tests.
