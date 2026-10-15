from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


YEARS = (2018, 2023)
SERVICE_ORDER = (
    "provisioning",
    "water_retention",
    "carbon_storage",
    "soil_retention",
    "recreation",
)
SERVICE_LABELS = {
    "provisioning": "Provisioning",
    "water_retention": "Water retention",
    "carbon_storage": "Carbon storage",
    "soil_retention": "Soil retention",
    "recreation": "Recreation",
}


def load_data(path: str | Path) -> pd.DataFrame:
    """Load the processed long-format dataset and enforce stable dtypes."""
    data = pd.read_csv(path)
    data["year"] = data["year"].astype(int)
    data["service"] = pd.Categorical(
        data["service"], categories=SERVICE_ORDER, ordered=True
    )
    return data


def validate_data(data: pd.DataFrame) -> dict[str, float | int]:
    """Run structural and numerical checks; raise AssertionError on failure."""
    required = {
        "year",
        "county",
        "county_zh",
        "service",
        "service_label",
        "service_zh",
        "value_yuan",
        "value_cny_100m",
    }
    assert required.issubset(data.columns), "Missing required columns"
    assert set(data["year"]) == set(YEARS), "Unexpected year set"
    assert data["county"].nunique() == 11, "Expected 11 counties"
    assert data["service"].nunique() == 5, "Expected five services"
    assert len(data) == 110, "Expected 110 year-county-service rows"
    assert not data.duplicated(["year", "county", "service"]).any(), "Duplicate keys"
    assert not data[list(required)].isna().any().any(), "Missing values"
    assert (data["value_yuan"] >= 0).all(), "Negative value detected"
    assert np.allclose(
        data["value_cny_100m"], data["value_yuan"] / 100_000_000, atol=5e-7
    ), "Unit conversion mismatch"

    county_sets = data.groupby("year", observed=True)["county"].apply(set)
    service_sets = data.groupby("year", observed=True)["service"].apply(
        lambda x: set(x.astype(str))
    )
    assert county_sets.iloc[0] == county_sets.iloc[1], "County sets differ by year"
    assert service_sets.iloc[0] == service_sets.iloc[1], "Service sets differ by year"

    totals = data.groupby("year", observed=True)["value_cny_100m"].sum()
    assert round(float(totals.loc[2018]), 2) == 2201.88
    assert round(float(totals.loc[2023]), 2) == 2696.03

    return {
        "rows": len(data),
        "counties": data["county"].nunique(),
        "services": data["service"].nunique(),
        "total_2018_cny_100m": float(totals.loc[2018]),
        "total_2023_cny_100m": float(totals.loc[2023]),
        "regional_change_pct": float((totals.loc[2023] / totals.loc[2018] - 1) * 100),
    }


def regional_totals(data: pd.DataFrame) -> pd.DataFrame:
    result = (
        data.groupby("year", observed=True, as_index=False)["value_cny_100m"]
        .sum()
        .rename(columns={"value_cny_100m": "total_cny_100m"})
    )
    result["total_cny_billion"] = result["total_cny_100m"] / 10
    return result


def service_summary(data: pd.DataFrame) -> pd.DataFrame:
    summary = (
        data.groupby(["year", "service"], observed=True, as_index=False)[
            "value_cny_100m"
        ]
        .sum()
        .sort_values(["year", "service"])
    )
    totals = summary.groupby("year", observed=True)["value_cny_100m"].transform("sum")
    summary["share_pct"] = summary["value_cny_100m"] / totals * 100
    return summary


def county_summary(data: pd.DataFrame) -> pd.DataFrame:
    totals = (
        data.groupby(["county", "year"], observed=True)["value_cny_100m"]
        .sum()
        .unstack("year")
        .rename(columns={2018: "value_2018", 2023: "value_2023"})
    )
    totals["absolute_change"] = totals["value_2023"] - totals["value_2018"]
    totals["change_pct"] = (totals["value_2023"] / totals["value_2018"] - 1) * 100
    return totals.sort_values("change_pct", ascending=True)


def county_service_change(data: pd.DataFrame) -> pd.DataFrame:
    wide = data.pivot_table(
        index="county",
        columns=["service", "year"],
        values="value_cny_100m",
        observed=True,
        aggfunc="sum",
    )
    change = pd.DataFrame(index=wide.index)
    for service in SERVICE_ORDER:
        change[SERVICE_LABELS[service]] = (
            wide[(service, 2023)] / wide[(service, 2018)] - 1
        ) * 100
    order = county_summary(data).index[::-1]
    return change.loc[order]
