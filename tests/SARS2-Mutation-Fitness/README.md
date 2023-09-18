# Fitness effects of SARS-CoV-2 amino-acid mutations estimated from observed versus expected mutation counts

**Authors:** **Jesse D. Bloom**, **Richard A. Neher**
**Manuscript**: https://www.biorxiv.org/content/10.1101/2023.01.30.526314v2
**Code and Data**: https://github.com/jbloomlab/SARS2-mut-fitness

In this study, the authors estimated the fitness effects of mutations to all SARS-CoV-2 proteins by [analyzing mutations in millions human SARS-CoV-2 sequences](https://usher-wiki.readthedocs.io/), and quantifying how the observed counts of each mutation compares to the expected counts from the underlying neutral mutation rate.

These data could be used to help guide the design of small molecule drugs targeting SARS-CoV-2 proteins that aren't suitable for standard deep mutational scanning experiments.

Some processing of the raw scores was done to conform to the data format [described in the documentation](https://dms-viz.github.io/dms-viz-docs/). Most of this processing was to map the sites in the data to the sites in avaliable protein structures. The details of this analysis can be found [here](https://github.com/jbloomlab/SARS2-mut-fitness/blob/main/scripts/format-data-for-dms-viz.py).

Some of the structures used in the visualization are hosted on the RCSB PDB, however, several are locally stored in [`tests/SARS2-Mutation-Fitness/structures/`](/tests/SARS2-Mutation-Fitness/structures/). Details for each structure are available in the [`experiments.csv`](/tests/SARS2-Mutation-Fitness/experiments.csv) file.
