# Mapping the neutralization profile of antibodies and sera against HIV envelope

In this study, [Radford et al.](https://www.sciencedirect.com/science/article/pii/S1931312823002184?via%3Dihub) mapped mutations to HIV envelope (Env) that affect neutralization by polyclonal human serum using a pseudotyping-based deep mutational scanning platform (Radford et al., 2023).

This visualization shows the escape profiles from a several sera and monoclonal antibodies from the paper. The total mutation escape at each site is displayed in the main plot. The regions on the protein with high total escape show the antiody binding footprints for a given epitope. Cetain serum samples – like IDC508 – target distinct epitopes on Env. You can toggle between these epitopes using the legend in the sidebar.

The `configure-dms-viz` command used to generate these visualizations is:

```bash
configure-dms-viz format
  --input tests/HIV-Envelope-BF520-DMS/input/IDC508_avg.csv
  --sitemap tests/HIV-Envelope-BF520-DMS/sitemap/sitemap.csv
  --output tests/HIV-Envelope-BF520-DMS/output/IDC508.json
  --name "IDC508"
  --metric "escape_mean"
  --metric-name "Escape"
  --condition "epitope"
  --condition-name "Epitope"
  --join-data tests/HIV-Envelope-BF520-DMS/join-data/functional_effects.csv
  --structure "6UDJ"
  --included-chains "C F M G J P"
  --excluded-chains "B L R A Q K"
  --tooltip-cols "{'times_seen': '# Obsv', 'effect': 'Func Eff.'}"
  --filter-cols "{'effect': 'Functional Effect', 'times_seen': 'Times Seen'}"
  --title "IDC508"
```

For more information about the experiment, check out the [manuscript](https://www.sciencedirect.com/science/article/pii/S1931312823002184?via=ihub):
> Mapping the neutralizing specificity of human anti-HIV serum by deep mutational scanning
>
> **Caelan E. Radford**, Philipp Schommers, Lutz Gieselmann, Katharine H. D. Crawford, Bernadeta Dadonaite, Timothy C. Yu, Adam S. Dingens, Julie Overbaugh, Florian Klein, **Jesse D. Bloom**

For more information on the analysis, check out the [GitHub repo](https://github.com/dms-vep/HIV_Envelope_BF520_DMS_CD4bs_sera).