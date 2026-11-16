
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

from config import COUNTRIES
from analysis_utils import METRICS, latest_by_country


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Econolytics",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Econolytics")
st.caption("Exploring Economic Indicators Across Emerging and Established Economies | 2000–2024")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

BASE = Path(__file__).resolve().parent
DATA_PATH = BASE / "data" / "processed" / "economic_data_clean.csv"

if not DATA_PATH.exists():
    st.error("Cleaned dataset not found. Please run the data pipeline first.")
    st.code("python3 fetch_data.py\npython3 preprocess.py")
    st.stop()

df = pd.read_csv(DATA_PATH)

df["year"] = pd.to_numeric(df["year"], errors="coerce")

for column in METRICS:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=["year", "country"])
df = df.sort_values(["country", "year"])

available_metrics = [
    column for column in METRICS
    if column in df.columns and df[column].notna().any()
]

if not available_metrics:
    st.error("No usable economic indicators were found.")
    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Data Filters")

min_year = int(df["year"].min())
max_year = int(df["year"].max())

year_range = st.sidebar.slider(
    "Select year range",
    min_year,
    max_year,
    (min_year, max_year)
)

country_list = sorted(df["country"].unique())

selected_countries = st.sidebar.multiselect(
    "Select countries",
    country_list,
    default=country_list
)

selected_metric = st.sidebar.selectbox(
    "Select primary indicator",
    available_metrics,
    format_func=lambda x: METRICS[x]
)


# Apply filters
view = df[
    df["year"].between(year_range[0], year_range[1])
    & df["country"].isin(selected_countries)
].copy()

if view.empty:
    st.warning("No data available. Please select at least one country.")
    st.stop()

latest = latest_by_country(view)


# --------------------------------------------------
# DASHBOARD TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Country Profiles",
    "Country Comparison",
    "Statistical Analysis",
    "Data Explorer"
])


# --------------------------------------------------
# 1. OVERVIEW
# --------------------------------------------------

with tab1:

    st.subheader("Global Economic Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Countries", view["country"].nunique())
    col2.metric("Years", view["year"].nunique())
    col3.metric("Observations", len(view))

    st.divider()

    # Latest value for each country
    st.subheader("Latest Country Values")

    fig = px.bar(
        latest,
        x="country",
        y=selected_metric,
        color="group",
        title=METRICS[selected_metric]
    )

    st.plotly_chart(fig, use_container_width=True)

    # Indicator trend over time
    st.subheader("Economic Trends Over Time")

    trend = view.groupby(
        ["year", "group"],
        as_index=False
    )[selected_metric].mean()

    fig = px.line(
        trend,
        x="year",
        y=selected_metric,
        color="group",
        markers=True,
        title="Average Indicator by Economic Group"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Group averages are calculated as the unweighted mean "
        "of available country values."
    )


# --------------------------------------------------
# 2. COUNTRY PROFILES
# --------------------------------------------------

with tab2:

    st.subheader("Explore an Individual Country")

    countries = sorted(view["country"].unique())

    chosen_country = st.selectbox(
        "Choose a country",
        countries
    )

    country_data = view[
        view["country"] == chosen_country
    ].sort_values("year")

    st.write("Economic group:", country_data["group"].iloc[0])

    country_metric = st.selectbox(
        "Choose an indicator",
        available_metrics,
        format_func=lambda x: METRICS[x],
        key="country_metric"
    )

    fig = px.line(
        country_data,
        x="year",
        y=country_metric,
        markers=True,
        title=f"{chosen_country}: {METRICS[country_metric]}"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Country Data")

    st.dataframe(
        country_data,
        use_container_width=True
    )


# --------------------------------------------------
# 3. COUNTRY COMPARISON
# --------------------------------------------------

with tab3:

    st.subheader("Compare Countries")

    comparison_metric = st.selectbox(
        "Select an indicator to compare",
        available_metrics,
        format_func=lambda x: METRICS[x],
        key="comparison_metric"
    )

    # Compare trends across countries
    fig = px.line(
        view,
        x="year",
        y=comparison_metric,
        color="country",
        markers=True,
        title=f"{METRICS[comparison_metric]} Across Countries"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Compare latest available values
    st.subheader("Latest Available Values")

    comparison_data = latest.dropna(
        subset=[comparison_metric]
    ).sort_values(
        comparison_metric,
        ascending=False
    )

    fig = px.bar(
        comparison_data,
        x="country",
        y=comparison_metric,
        color="group",
        title="Country Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# 4. STATISTICAL ANALYSIS
# --------------------------------------------------

with tab4:

    st.subheader("Descriptive Statistics")

    stat_metric = st.selectbox(
        "Choose a variable",
        available_metrics,
        format_func=lambda x: METRICS[x],
        key="stat_metric"
    )

    stat_data = view.dropna(
        subset=[stat_metric]
    )

    # Histogram
    st.write("Distribution of Values")

    fig = px.histogram(
        stat_data,
        x=stat_metric,
        color="group",
        title=f"Distribution of {METRICS[stat_metric]}"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Box plot
    st.write("Comparison of Distributions")

    fig = px.box(
        stat_data,
        x="group",
        y=stat_metric,
        color="group",
        title=f"{METRICS[stat_metric]} by Economic Group"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Descriptive statistics
    st.write("Summary Statistics")

    statistics = stat_data.groupby("country")[stat_metric].agg(
        ["count", "mean", "median", "std", "min", "max"]
    ).round(2)

    st.dataframe(
        statistics,
        use_container_width=True
    )

    # Correlation analysis
    st.divider()
    st.subheader("Correlation Analysis")

    numeric_data = view[available_metrics]

    if len(available_metrics) >= 2:

        correlation = numeric_data.corr()

        fig = px.imshow(
            correlation,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title="Correlation Heatmap"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Correlation measures the strength and direction of a relationship. "
            "Correlation does not necessarily imply causation."
        )

    else:
        st.info("At least two indicators are needed for correlation analysis.")


# --------------------------------------------------
# 5. DATA EXPLORER
# --------------------------------------------------

with tab5:

    st.subheader("Explore the Dataset")

    st.write("Cleaned Economic Dataset")

    st.dataframe(
        view,
        use_container_width=True
    )

    st.divider()

    # Missing value analysis
    st.subheader("Missing Value Analysis")

    missing_values = pd.DataFrame({
        "Missing Count": view.isna().sum(),
        "Missing Percentage": (
            view.isna().mean() * 100
        ).round(2)
    })

    st.dataframe(
        missing_values,
        use_container_width=True
    )

    # Download dataset
    st.subheader("Download Data")

    csv_data = view.to_csv(index=False)

    st.download_button(
        label="Download Filtered Dataset",
        data=csv_data,
        file_name="economic_data.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Econolytics | Economic Data Exploration and Visualization Project"
)
