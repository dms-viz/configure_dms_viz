# Fitness effects of mutations to SARS-CoV-2 protein

In this study, the authors estimated the fitness effects of mutations to all SARS-CoV-2 proteins by [analyzing mutations in millions human SARS-CoV-2 sequences](https://usher-wiki.readthedocs.io/), and quantifying how the observed counts of each mutation compares to the expected counts from the underlying neutral mutation rate. These mutation-fitness estimates are useful for purposes such as attempting to design antiviral drugs that target functionally constrained sites where resistance is unlikely to emerge. The visualization above shows the average mutation-fitness for each site in every SARS-CoV-2 protein.

The `configure-dms-viz` command used to generate this visualization is:

```bash
configure-dms-viz
  --input tests/SARS2-Mutation-Fitness/input/S_fitness.csv
  --sitemap tests/SARS2-Mutation-Fitness/sitemap/S_sitemap.csv
  --output tests/SARS2-Mutation-Fitness/sitemap/S.json
  --name "S"
  --metric "fitness"
  --metric-name "Fitness"
  --structure "6VYB"
  --included-chains "polymer"
  --tooltip-cols "{'expected_count': 'Expected Count'}"
  --filter-cols "{'expected_count': 'Expected Count'}"
  --filter-limits "{'expected_count': [0, 100]}"
  --title "S"
  --alphabet "RKHDEQNSTYWFAILMVGPC*"
  --exclude-amino-acids "*"
  --description "The Spike Glycoprotein. The Structure is has one RBD in the up position. [Structure: 6VYB]"
```

For more information about the study, check out the [manuscript](https://www.biorxiv.org/content/10.1101/2023.01.30.526314v2):
> Fitness effects of mutations to SARS-CoV-2 protein
>
> **Jesse D. Bloom**, **Richard A. Neher**

To view the analysis pipeline and raw data, checkout the [GitHub repository](https://github.com/jbloomlab/SARS2-mut-fitness).

Some processing of the raw scores was done to conform to the data format [described in the documentation](https://dms-viz.github.io/dms-viz-docs/). Most of this processing was to map the sites in the data to the sites in avaliable protein structures. The details of this analysis can be found [here](https://github.com/jbloomlab/SARS2-mut-fitness/blob/main/scripts/format-data-for-dms-viz.py).

Some of the structures used in the visualization are hosted on the RCSB PDB, however, several are locally stored in [`tests/SARS2-Mutation-Fitness/structures/`](/tests/SARS2-Mutation-Fitness/structures/). Details for each structure are available in the [`experiments.csv`](/tests/SARS2-Mutation-Fitness/experiments.csv) file.