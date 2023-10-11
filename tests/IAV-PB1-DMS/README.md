# Deep mutational scanning reveals the functional constraints and evolutionary potential of the influenza A virus PB1 protein

[Li et. al.](https://www.biorxiv.org/content/10.1101/2023.08.27.554986v1.full) measured the effects of thousands of mutations to the PB1 subunit of the RdRP on the replicative fitness of the lab-adapted influenza strain A/WSN/1933(H1N1) (Li et. al., 2023). 

The visualization above shows the mean mutation-fitness at each site in the PB1 subunit. Sites that tolerate the most mutational change will be closet to a fitness score of 0. The structure used for this visualization is [7NHX](https://www.rcsb.org/structure/7NHX), which is a cryo-EM structure of the 1918 H1N1 Viral influenza polymerase heterotrimer - full transcriptase (Class1). The IAV PB1 subunit is `chain B` of the full assembly.

The `configure-dms-viz` command used to generate this visualization is:

```bash
configure-dms-viz
  --input tests/IAV-PB1-DMS/input/pb1_fitness.csv
  --sitemap tests/IAV-PB1-DMS/sitemap/sitemap.csv
  --output tests/IAV-PB1-DMS/sitemap/pb1.json
  --name "IAV PB1"
  --metric "fitness"
  --metric-name "Replicative Fitness"
  --structure "7NHX"
  --included-chains "B"
  --title "IAV PB1 Deep Mutational Scan"
  --description "Deep mutational scan of influenza virus A/WSN/1933(H1N1) PB1 RdRp subunit"
```

For more information about the study, check out the [manuscript](https://www.biorxiv.org/content/10.1101/2023.08.27.554986v1.full):
> Deep mutational scanning reveals the functional constraints and evolutionary potential of the influenza A virus PB1 protein
>
> **Yuan Li**, Sarah Arcos, Kimberly R. Sabsay, Aartjan J.W. te Velthuis, **Adam S. Lauring**

A small amount of pre-processing was performed on the raw data from the manuscript to conform to the data requirements detailed in the [documentation](https://dms-viz.github.io/dms-viz-docs/) of `dms-viz`:

```python
# Import and format the data from the supplement
fitness_df = pd.read_csv("../data/supplemental-data.csv")
# Drop the amplicon column
fitness_df.drop('amplicon', axis=1, inplace=True)
# Replace the three letter code with one letter code
fitness_df['wildtype'] = fitness_df['wildtype'].replace(AA_DICT)
fitness_df['substitution'] = fitness_df['substitution'].replace(AA_DICT)
# Rename the columns
fitness_df.rename(columns={'substitution': 'mutant'}, inplace=True)
# Save the output data
fitness_df.to_csv("../data/fitness.csv", index=False)
```

To summarize, the columns were renamed according to the `dms-viz` naming scheme and the three-letter amino acid code was converted to the one-letter code.
