""" Example workflow for creating a JSON file for https://dms-viz.github.io/ """

# Import modules
import json
import pandas as pd
from os.path import join

# Name of the virus in the tests directory
virus = "sars2"

# Paths to data directories
virus_dir = f"tests/{virus}"
output_dir = f"tests/{virus}/output"
data_dir = f"tests/{virus}/escape"

# Read in data for each virus
experiments = pd.read_csv(join(virus_dir, f"experiments.csv"))


# Target rule
rule all:
    input:
        join(output_dir, f"{virus}.json"),


# Create JSON files for each experiment
rule create_viz_json:
    input:
        escape_df=join(data_dir, "{experiment}_avg.csv"),
        sitemap_df=join(virus_dir, "site_numbering_map.csv"),
        functional_score_df=join(virus_dir, "muteffects_observed.csv"),
    output:
        join(output_dir, "{experiment}.json"),
    params:
        name=lambda wildcards: wildcards.experiment,
        structure=lambda wildcards: experiments.loc[
            experiments["selection"] == wildcards.experiment, "pdb"
        ].item(),
        include_chains=lambda wildcards: experiments.loc[
            experiments["selection"] == wildcards.experiment, "dataChains"
        ].item(),
        exclude_chains=lambda wildcards: experiments.loc[
            experiments["selection"] == wildcards.experiment, "excludedChains"
        ].item(),
        filter_cols={"effect": "Functional Effect", "times_seen": "Times Seen"},
        tooltip_cols={"times_seen": "# Obsv", "effect": "Func Eff."},
        metric="escape_mean",
        metric_name="Escape",
        condition="epitope",
        condition_name="Epitope",
    shell:
        """ 
        configure-dms-viz \
            --input {input.escape_df} \
            --name {params.name} \
            --sitemap {input.sitemap_df} \
            --metric {params.metric} \
            --structure {params.structure} \
            --metric-name {params.metric_name} \
            --output {output} \
            --condition {params.condition} \
            --condition-name {params.condition_name} \
            --join-data {input.functional_score_df} \
            --included-chains "{params.include_chains}" \
            --excluded-chains "{params.exclude_chains}" \
            --filter-cols "{params.filter_cols}" \
            --tooltip-cols "{params.tooltip_cols}" \
            --title "{params.name}" \
        """


# Combine JSON files into one
rule combine_jsons:
    input:
        input_files=expand(
            join(output_dir, "{experiment}.json"),
            experiment=experiments.selection.unique(),
        ),
    output:
        output_file=join(output_dir, f"{virus}.json"),
    run:
        combined_data = {}
        for input_file in input.input_files:
            with open(input_file) as f:
                data = json.load(f)
                combined_data.update(data)
        with open(output.output_file, "w") as f:
            json.dump(combined_data, f)
