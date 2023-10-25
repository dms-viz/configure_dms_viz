# Escape from the antibodies in the Regeneron cocktail targeting the SARS-CoV-2 RBD

`dms-viz` is an interactive tool designed to visualize mutation-level data on an associated protein structure. This example visualization is showing how mutations to the SARS-CoV-2 receptor binding domain (RBD) escape antibody binding by two (previously) clinically approved monoclonal antibodies – REGN10933 and REGN10987. The protein structure is the RBD bound by the Fab fragments of both antibodies [PDB 6XDG](https://www.rcsb.org/structure/6XDG).

The total mutation escape at each site is shown in the summary plot and on the structure. It's clear that regions of the protein with high total escape represent the antibody binding footprints for their corresponding antibody selection.

To use the visualization, you can *zoom* in and out of regions of your data by *brushing* (click and drag) over the area plot. You can select sites to see in the heatmap by *clicking* on points in the line/point plot. You can *mouseover* sites on the line/point and mutations on the heatmap to see details in a pop-up tooltip. Finally, you can select which sites to highlight on the protein structure by *brushing* (click and drag) over points and *clicking* on points in the line/point plot. To deselect sites, you can either *double-click* on the line/point plot or hold down the *option key* (⌥) and *brush* over the sites that you want to deselect.

In this visualization, there are two seperate condition – each representing an antibody in the cocktail. If there are more than on condition in the data, an interactive legend will appear in the Chart Options section of the sidebar. You can select an condition to visualize on the protein structure by *clicking* on a condition in the legend. You can remove or add conditions to the line/point plot by holding down the *option key* (⌥) while *clicking*.

The protein structure is interactive. You can reorient and zoom into the protein structure by *clicking* and *dragging* it around the window. You can also reset the protein structure to its original orientation by *pressing* the `R` button on your keyboard.

For more details on how to use `dms-viz` with your own data, [check out the documentation](https://dms-viz.github.io/dms-viz-docs/).

The `configure-dms-viz` command used to generate this visualization is:

```bash
configure-dms-viz format
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
