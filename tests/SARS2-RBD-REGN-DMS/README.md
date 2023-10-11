# Prospective mapping of viral mutations that escape antibodies used to treat COVID-19

This visualization is showing how mutations to the SARS-CoV-2 receptor binding domain (RBD) escape antibody binding by two (previously) clinically approach monoclonal antibodies – REGN10933 and REGN10987. The protein structure is the RBD bound by the Fab fragments of both antibodies [PDB 6XDG](https://www.rcsb.org/structure/6XDG).

The total mutation escape at each site is shown in the summary plot and on the structure. It's clear that regions of the protein with high total escape represent the antibody binding footprints for their corresponding antibody selection. Use the legend to toggle between the antibody selections being shown on the plot and on the protein.

The `configure-dms-viz` command used to generate this visualization is:

```bash
configure-dms-viz 
  --input "input/REGN_escape.csv" 
  --sitemap "sitemap/sitemap.csv" 
  --output "REGN_cocktail.json" 
  --name "REGN mAb Cocktail" 
  --metric "mut_escape" 
  --metric-name "Escape" 
  --structure "6XDG" 
  --condition "condition" 
  --condition-name "Antibody" 
  --included-chains "E" 
  --colors "#a10e0e,#220ea1" 
  --title "Escape from the Regeneron anti-RBD antibody cocktail"
```

For more information about the study, check out the [manuscript](https://science.sciencemag.org/content/early/2021/01/22/science.abf9302):
> Prospective mapping of viral mutations that escape antibodies used to treat COVID-19
>
> **Tyler N. Starr**, **Allison J. Greaney**, Amin Addetia, William W. Hannon, Manish C. Choudhary, Adam S. Dingens, Jonathan Z. Li, **Jesse D. Bloom**

To view the analysis pipeline and raw data, checkout the [GitHub repository](https://github.com/jbloomlab/SARS-CoV-2-RBD_MAP_clinical_Abs/blob/main/).
