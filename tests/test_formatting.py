"""Explicit unit tests for the formatting commands of configure-dms-viz."""

import pandas as pd
import pytest
from configure_dms_viz.configure_dms_viz import (
    format_mutation_data,
    format_sitemap_data,
    join_additional_data,
)


@pytest.fixture
def dummy_data():
    mut_metric_df = pd.read_csv("tests/dummy-data/dummy.csv")
    sitemap_df = pd.read_csv("tests/dummy-data/dummymap.csv")
    join_data_df = pd.read_csv("tests/dummy-data/dummyjoin.csv")
    included_chains = "E"
    return sitemap_df, mut_metric_df, join_data_df, included_chains


def test_format_mutation_data(dummy_data):
    """Test input data formatting"""

    # Load the dummy dataset
    _, mut_metric_df, _, _ = dummy_data

    # Define the parameters for the function call
    metric_col = "mut_escape"
    condition_col = "condition"
    alphabet = "RKHDEQNSTYWFAILMVGPC-*"

    # Call the function
    formatted_data = format_mutation_data(
        mut_metric_df, metric_col, condition_col, alphabet
    )

    # Assert the 'site' column is renamed to 'reference_site'
    assert "reference_site" in formatted_data.columns

    # Assert the necessary columns are present
    necessary_columns = {"reference_site", "wildtype", "mutant", metric_col}
    if condition_col is not None:
        necessary_columns.add(condition_col)
    assert set(formatted_data.columns).issuperset(necessary_columns)

    # Assert there are no NaN values in the metric column
    assert not formatted_data[metric_col].isna().any()


def test_format_sitemap_data(dummy_data):
    """Test sitemap formatting"""
    sitemap_df, mut_metric_df, _, included_chains = dummy_data

    # Define the parameters for the function call
    metric_col = "mut_escape"
    condition_col = "condition"
    alphabet = "RKHDEQNSTYWFAILMVGPC-*"

    # Call the function
    formatted_data = format_mutation_data(
        mut_metric_df, metric_col, condition_col, alphabet
    )

    # Format the sitemap data
    formatted_df = format_sitemap_data(sitemap_df, formatted_data, included_chains)

    # Assert that all necessary columns are present
    for column in ["reference_site", "sequential_site", "protein_site", "chains"]:
        assert column in formatted_df.columns

    # Check that reference sites match between sitemap and mutation dataframes
    assert set(formatted_data.reference_site).issubset(set(formatted_df.reference_site))

    # Assert that sequential sites are numeric
    assert pd.api.types.is_numeric_dtype(formatted_df["sequential_site"])

    # Check that protein sites are filled in if missing
    if "protein_site" not in sitemap_df.columns:
        assert all(formatted_df["protein_site"] == formatted_df["reference_site"])


def test_join_additional_data(dummy_data):
    """Test joining additional dataframes to the main dataframe"""
    _, mut_metric_df, join_data_df, _ = dummy_data

    # Define the parameters for the function call
    metric_col = "mut_escape"
    condition_col = "condition"
    alphabet = "RKHDEQNSTYWFAILMVGPC-*"

    # Call the function
    formatted_data = format_mutation_data(
        mut_metric_df, metric_col, condition_col, alphabet
    )

    # Prepare the list of dataframes to join
    join_data = [join_data_df]

    # Call the function
    joined_df = join_additional_data(formatted_data, join_data)

    # Assert the merged dataframe contains the expected columns from the join dataframe
    for column in ["reference_site", "wildtype", "mutant"]:
        assert column in joined_df.columns

    # Assert additional column was properly added
    assert (
        "additional_col" in joined_df.columns
    ), "Expected column 'additional_info' not found in the joined dataframe."

    # Assert no duplicate measurements per mutation
    assert not joined_df.duplicated(
        subset=["reference_site", "wildtype", "mutant"]
    ).any(), "Duplicate measurements found after join."


if __name__ == "__main__":
    pytest.main([__file__])
