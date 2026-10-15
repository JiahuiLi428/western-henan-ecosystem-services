from pathlib import Path

import pytest

from src.portfolio_analysis import (
    county_summary,
    load_data,
    regional_totals,
    service_summary,
    validate_data,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "ecosystem_values_2018_2023.csv"


@pytest.fixture(scope="module")
def data():
    return load_data(DATA)


def test_dataset_integrity(data):
    checks = validate_data(data)
    assert checks["rows"] == 110
    assert checks["regional_change_pct"] == pytest.approx(22.44219, abs=1e-4)


def test_regional_totals(data):
    totals = regional_totals(data).set_index("year")
    assert totals.loc[2018, "total_cny_100m"] == pytest.approx(2201.879988, abs=1e-5)
    assert totals.loc[2023, "total_cny_100m"] == pytest.approx(2696.030084, abs=1e-5)


def test_service_shares_sum_to_100(data):
    summary = service_summary(data)
    shares = summary.groupby("year", observed=True)["share_pct"].sum()
    assert shares.loc[2018] == pytest.approx(100.0)
    assert shares.loc[2023] == pytest.approx(100.0)


def test_county_growth_extremes(data):
    counties = county_summary(data)
    assert counties.index[0] == "Lushan County"
    assert counties.index[-1] == "Luanchuan County"
