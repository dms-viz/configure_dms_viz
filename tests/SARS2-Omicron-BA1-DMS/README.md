# A pseudovirus system enables deep mutational scanning of the full SARS-CoV-2 spike

In this study, the authors describe a system that uses pseudovirus to perform deep mutational scanning on viral glycoproteins. They used this system to map escape from monocolonal antibodies against the full SARS-CoV-2 Spike protein.

The visualization above shows the total mutation-escape for each antibody on the Omicron BA1 Spike structure.

The `configure-dms-viz` command used to generate this visualization is:

```bash
configure-dms-viz
  --input tests/SARS2-Omicron-BA1-DMS/input/LyCoV-1404_avg.csv
  --sitemap tests/SARS2-Omicron-BA1-DMS/sitemap/sitemap.csv
  --output tests/SARS2-Omicron-BA1-DMS/output/LyCoV-1404_avg.json
  --name "LyCoV-1404"
  --metric "escape_mean"
  --metric-name "Escape"
  --structure "6xr8"
  --included-chains "polymer"
  --join-data tests/SARS2-Omicron-BA1-DMS/join-data/muteffects_observed.csv
  --tooltip-cols "{'times_seen': '# Obsv', 'effect': 'Func Eff.'}"
  --filter-cols "{'effect': 'Functional Effect', 'times_seen': 'Times Seen'}"
  --title "LyCoV-1404"
```

For more information about the study, check out the [manuscript](https://www.sciencedirect.com/science/article/pii/S0092867423001034):
> A pseudovirus system enables deep mutational scanning of the full SARS-CoV-2 spike
>
> **Bernadeta Dadonaite**, **Katharine H D Crawford**, **Caelan E Radford**, Ariana G Farrell, Timothy C Yu, William W Hannon, Panpan Zhou, Raiees Andrabi, Dennis R Burton, Lihong Liu, David D. Ho, Richard A. Neher, **Jesse D Bloom**

To view the analysis pipeline and raw data, checkout the [GitHub repository](https://github.com/dms-vep/SARS-CoV-2_Omicron_BA.1_spike_DMS_mAbs).