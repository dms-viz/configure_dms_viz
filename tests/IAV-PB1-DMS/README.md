# Deep mutational scanning reveals the functional constraints and evolutionary potential of the influenza A virus PB1 protein

**Authors:** **Yuan Li**, Sarah Arcos, Kimberly R. Sabsay, Aartjan J.W. te Velthuis, **Adam S. Lauring**
**Manuscript**: https://www.biorxiv.org/content/10.1101/2023.08.27.554986v1.full

In this study, the authors preformed a deep-mutational scan of the influenza (IAV) A virus PB1 protein to assess the replicative fitness of mutations. Specifically, they used the A/WSN/1933(H1N1) (abbreviated WSN33) strain of influenza.

The structure used for this visualization is [7NHX](https://www.rcsb.org/structure/7NHX), which is a cryo-EM structure of the 1918 H1N1 Viral influenza polymerase heterotrimer - full transcriptase (Class1). The IAV PB1 subunit is `chain B` of the full assembly.

A small amount of post-processing was performed on the raw data from the manuscript to conform to the data requirements detailed in the [documentation](https://dms-viz.github.io/dms-viz-docs/) of `dms-viz`:

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
