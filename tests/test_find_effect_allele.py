import sys

import pytest

import pandas as pd

from effect_alleles.gwas_catalogue import find_trait, find_direction

@pytest.fixture
def whole_df():

    return pd.read_table("tests/test_data.tsv", sep="\t")


@pytest.fixture
def rs_df():

    return pd.read_table("tests/rs543874.txt", sep="\t")

@pytest.fixture
def bmi():
    return ["bmi", "body mass index", "body fat", "circumference"]

@pytest.fixture
def expected_result_find_traits():

    return pd.read_table("tests/expected_result_find_trait.txt", sep="\t", index_col=False)

def test_find_trait(rs_df, bmi, expected_result_find_traits):

    trait_df = find_trait(rs_df, bmi)

    assert trait_df.equals(expected_result_find_traits)



def test_find_direction(expected_result_find_traits):

    up_down = find_direction(expected_result_find_traits)

    assert up_down == ("G", "A")
