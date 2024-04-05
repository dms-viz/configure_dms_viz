"""Explicit unit tests for the PDB utils of configure-dms-viz."""

import pytest
import pandas as pd

from configure_dms_viz.pdb_utils import (
    get_structure,
    check_chains,
    check_wildtype_residues,
)
from configure_dms_viz.configure_dms_viz import (
    format_mutation_data,
    format_sitemap_data,
)


@pytest.fixture
def dummy_data():
    # Get a local structure
    structure = get_structure("tests/dummy-data/dummypdb.pdb")
    mut_metric_df = pd.read_csv("tests/dummy-data/dummy.csv")
    sitemap_df = pd.read_csv("tests/dummy-data/dummymap.csv")
    included_chains = "E"
    return structure, sitemap_df, mut_metric_df, included_chains


def test_check_chains_with_valid_chains(dummy_data):
    """Test that check_chains does not raise an error when the chains are present."""
    structure, _, _, included_chains = dummy_data
    try:
        check_chains(structure, [included_chains])
        assert True  # If no exception is raised, the test passes
    except ValueError:
        pytest.fail("check_chains raised ValueError unexpectedly!")


def test_check_chains_with_invalid_chains(dummy_data):
    """Test that check_chains raises an error when the chains are not present."""
    structure, _, _, _ = dummy_data
    with pytest.raises(ValueError) as excinfo:
        check_chains(structure, ["Z"])
    assert "are not present in the PDB structure" in str(excinfo.value)


def test_check_wildtype_residues_with_all_matches(dummy_data):
    """Test that check_wildtype_residues correctly identifies all matching wildtype residues."""
    structure, sitemap_df, mut_metric_df, included_chains = dummy_data

    # Define the parameters for formatting mutation data
    metric_col = "mut_escape"
    condition_col = "condition"
    alphabet = "RKHDEQNSTYWFAILMVGPC-*"

    # Format the sitemap and mutation data
    formatted_data = format_mutation_data(
        mut_metric_df, metric_col, condition_col, alphabet
    )
    formatted_sitemap = format_sitemap_data(sitemap_df, formatted_data, included_chains)

    result = check_wildtype_residues(structure, formatted_data, formatted_sitemap, None)
    # Dummy data is only a subset of a full dataset
    assert result[0] == 1.0
    assert result[1] > 0.0


def test_check_wildtype_residues_with_no_matches(dummy_data):
    """Test that check_wildtype_residues correctly identifies no matching wildtype residues."""
    structure, sitemap_df, mut_metric_df, included_chains = dummy_data

    # Define the parameters for formatting mutation data
    metric_col = "mut_escape"
    condition_col = "condition"
    alphabet = "RKHDEQNSTYWFAILMVGPC-*"

    # Format the sitemap and mutation data
    formatted_data = format_mutation_data(
        mut_metric_df, metric_col, condition_col, alphabet
    )
    formatted_sitemap = format_sitemap_data(sitemap_df, formatted_data, included_chains)

    # Manipulate the mut_metric_df to ensure no matches
    formatted_data["wildtype"] = "X"
    result = check_wildtype_residues(structure, formatted_data, formatted_sitemap, None)
    # Expect no matches
    assert result[0] == 0.0
    assert result[1] > 0.0
