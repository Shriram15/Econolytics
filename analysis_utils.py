
import numpy as np
import pandas as pd


# Names of indicators used in the dashboard
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


# Weights used to calculate the development index
INDEX_WEIGHTS = {
    "gdp_per_capita_ppp": 0.30,
    "life_expectancy": 0.25,
    "internet_users_pct": 0.15,
    "electricity_access_pct": 0.15,
    "manufacturing_pct_gdp": 0.10,
    "unemployment_pct": 0.05,
}


# Get the latest available record for each country
def latest_by_country(df, year=None):

    data = df.copy()

    if year is not None:
        data = data[data["year"] <= year]

    data = data.sort_values("year")

    return data.groupby("country", as_index=False).tail(1)


# Calculate a development index for each country and year
def build_development_index(df):

    data = df.copy()

    for column in INDEX_WEIGHTS:

        if column not in data.columns:
            data[column] = np.nan

        # Normalize values between 0 and 1 for each year
        minimum = data.groupby("year")[column].transform("min")
        maximum = data.groupby("year")[column].transform("max")

        difference = maximum - minimum

        data[column + "_norm"] = (
            (data[column] - minimum) / difference
        )

        # Lower unemployment is better
        if column == "unemployment_pct":
            data[column + "_norm"] = 1 - data[column + "_norm"]

    # Calculate weighted average
    total_score = 0
    total_weight = 0
    available_dimensions = 0

    for column, weight in INDEX_WEIGHTS.items():

        normalized_column = column + "_norm"

        total_score += data[normalized_column].fillna(0) * weight
        total_weight += data[normalized_column].notna() * weight
        available_dimensions += data[normalized_column].notna()

    data["development_index"] = np.where(
        (available_dimensions >= 4) & (total_weight > 0),
        total_score / total_weight * 100,
        np.nan
    )

    return data


# Compare emerging economies with established economies
def convergence_table(df):

    data = df.dropna(
        subset=["gdp_per_capita_ppp"]
    ).copy()

    established = data[data["group"] == "Established"]

    average = established.groupby("year")[
        "gdp_per_capita_ppp"
    ].mean()

    data["established_mean_ppp"] = data["year"].map(average)

    data["income_ratio_to_established"] = (
        data["gdp_per_capita_ppp"] / data["established_mean_ppp"]
    )

    data["income_gap_ppp"] = (
        data["established_mean_ppp"] - data["gdp_per_capita_ppp"]
    )

    return data
