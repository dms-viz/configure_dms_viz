# VAMPseq mutational scan of the PTEN tumor suppressor

The `configure-dms-viz` command used to generate this visualization is:

```bash
configure-dms-viz format \
  --input tests/PTEN-VAMPseq/input/PTEN-VAMPseq.csv \
  --output tests/PTEN-VAMPseq/output/PTEN-VAMPseq.json \
  --name "PTEN-VAPseq" \
  --metric "score" \
  --metric-name "Score" \
  --heatmap-limits "-2, 1, 4" \
  --structure "1D5R" 
```
