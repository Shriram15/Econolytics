"""Reusable calculations for country profiles and comparative analysis."""
import numpy as np
import pandas as pd

METRICS = {
    "gdp_current_usd": "GDP (current US$)",
    "gdp_constant_usd": "GDP (constant 2015 US$)",
    "gdp_growth_pct": "GDP growth (%)",
    "gdp_per_capita_usd": "GDP per capita (current US$)",
    "gdp_per_capita_ppp": "GDP per capita (PPP)",
    "population": "Population",
    "manufacturing_pct_gdp": "Manufacturing (% GDP)",
    "exports_pct_gdp": "Exports (% GDP)",
    "imports_pct_gdp": "Imports (% GDP)",
    "trade_openness_pct_gdp": "Trade openness (% GDP)",
    "unemployment_pct": "Unemployment (%)",
    "life_expectancy": "Life expectancy (years)",
    "internet_users_pct": "Internet users (%)",
    "electricity_access_pct": "Electricity access (%)",
    "urban_population_pct": "Urban population (%)",
    "gdp_per_capita_yoy_pct": "GDP per capita annual change (%)",
}

# Higher is desirable for all except unemployment, which is reversed.
INDEX_WEIGHTS = {
    "gdp_per_capita_ppp": 0.30,
    "life_expectancy": 0.25,
    "internet_users_pct": 0.15,
    "electricity_access_pct": 0.15,
    "manufacturing_pct_gdp": 0.10,
    "unemployment_pct": 0.05,
}

def latest_by_country(df, year=None):
    data = df.copy()
    if year is not None:
        data = data[data["year"] <= year]
    return data.sort_values("year").groupby("country", as_index=False).tail(1)

def build_development_index(df):
    """Annual cross-sectional min-max index. Requires >= 4 of 6 dimensions."""
    data = df.copy()
    directions = {k: 1 for k in INDEX_WEIGHTS}
    directions["unemployment_pct"] = -1

    # Normalize within each year so changes in global scale over time do not
    # dominate the comparison. A constant or fully missing annual column stays NaN.
    for col, direction in directions.items():
        norm_col = col + "_norm"
        if col not in data:
            data[norm_col] = np.nan
            continue

        def normalize_year(series):
            lo, hi = series.min(), series.max()
            if pd.isna(lo) or pd.isna(hi) or hi == lo:
                return pd.Series(np.nan, index=series.index)
            scaled = (series - lo) / (hi - lo)
            return scaled if direction == 1 else 1 - scaled

        data[norm_col] = data.groupby("year")[col].transform(normalize_year)

    norm_cols = [k + "_norm" for k in INDEX_WEIGHTS]
    weights = pd.Series(INDEX_WEIGHTS)
    numerator = data[norm_cols].mul(weights.values, axis=1).sum(axis=1, min_count=1)
    available_weight = data[norm_cols].notna().mul(weights.values, axis=1).sum(axis=1)
    data["development_index"] = np.where(
        (data[norm_cols].notna().sum(axis=1) >= 4) & (available_weight > 0),
        numerator / available_weight * 100,
        np.nan
    )
    return data

def convergence_table(df):
    """Compare each emerging country's PPP income with established-group mean."""
    data = df.dropna(subset=["gdp_per_capita_ppp"]).copy()
    group_mean = data[data.group == "Established"].groupby("year")[
        "gdp_per_capita_ppp"
    ].mean().rename("established_mean_ppp")
    data = data.join(group_mean, on="year")
    data["income_ratio_to_established"] = (
        data["gdp_per_capita_ppp"] / data["established_mean_ppp"]
    )
    data["income_gap_ppp"] = (
        data["established_mean_ppp"] - data["gdp_per_capita_ppp"]
    )
    return data
