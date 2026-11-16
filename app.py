from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from config import COUNTRIES, INDICATORS
from analysis_utils import (
    METRICS,
    INDEX_WEIGHTS,
    build_development_index,
    convergence_table,
    latest_by_country
)

BASE = Path(__file__).resolve().parent
DATA_PATH = BASE / "data/processed/economic_data_clean.csv"

st.set_page_config(
    page_title="Global Economic Intelligence",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Economic Intelligence Dashboard")
st.caption("Emerging Economies vs Established Global Powers | 2000–2024")


# ============================================================
# COLOUR PALETTES
# ============================================================

# Used when comparing the two economic groups
GROUP_COLORS = {
    "Emerging": "#1F4E79",
    "Established": "#E67E22"
}

# Used when comparing individual countries
COUNTRY_COLORS = {
    "India": "#1F4E79",
    "Brazil": "#00A6A6",
    "Indonesia": "#5375D8",
    "Mexico": "#16A34A",
    "United States": "#E67E22",
    "Germany": "#DC3545",
    "Japan": "#9B59B6",
    "United Kingdom": "#D4A017"
}


# ============================================================
# LOAD DATA
# ============================================================

if not DATA_PATH.exists():
    st.warning("Processed dataset not found. Run the data pipeline first.")
    st.code(
        "pip install -r requirements.txt\n"
        "python fetch_data.py\n"
        "python preprocess.py\n"
        "streamlit run app.py"
    )
    st.stop()

df = pd.read_csv(DATA_PATH)

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df = df.sort_values(["country", "year"])

available_metrics = [
    k for k in METRICS
    if k in df.columns and df[k].notna().any()
]

country_list = sorted(df.country.dropna().unique())


# ============================================================
# SIDEBAR FILTERS
# ============================================================

with st.sidebar:

    st.header("Global filters")

    min_year = int(df.year.min())
    max_year = int(df.year.max())

    year_range = st.slider(
        "Analysis period",
        min_year,
        max_year,
        (min_year, max_year)
    )

    countries_selected = st.multiselect(
        "Countries",
        country_list,
        default=country_list
    )

    primary_metric = st.selectbox(
        "Primary indicator",
        available_metrics,
        format_func=lambda x: METRICS[x],
        index=(
            available_metrics.index("gdp_growth_pct")
            if "gdp_growth_pct" in available_metrics
            else 0
        )
    )


view = df[
    df.year.between(*year_range)
    & df.country.isin(countries_selected)
].copy()

if view.empty:
    st.info("Select at least one country.")
    st.stop()

latest = latest_by_country(view)
indexed = build_development_index(view)
latest_index = latest_by_country(indexed)


# ============================================================
# TOP-LEVEL KPI ROW
# ============================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Countries in analysis",
    view.country.nunique()
)

c2.metric(
    "Emerging economies",
    view.loc[view.group == "Emerging", "country"].nunique()
)

c3.metric(
    "Established powers",
    view.loc[view.group == "Established", "country"].nunique()
)

c4.metric(
    "Country-year observations",
    f"{len(view):,}"
)


# ============================================================
# DASHBOARD TABS
# ============================================================

tabs = st.tabs([
    "Global overview",
    "Country profiles",
    "Economic comparison",
    "Industry & trade",
    "Human development",
    "Statistical analysis",
    "Multivariate analysis",
    "Convergence & index",
    "Data quality",
    "Data explorer"
])


# ============================================================
# 1. GLOBAL OVERVIEW
# ============================================================

with tabs[0]:

    st.subheader("Global economic snapshot")

    a, b = st.columns(2)

    # Latest country comparison
    with a:

        fig = px.bar(
            latest.dropna(subset=[primary_metric]),
            x="country",
            y=primary_metric,
            color="group",
            color_discrete_map=GROUP_COLORS,
            title=f"Latest available {METRICS[primary_metric]}",
            hover_data=["year"]
        )

        st.plotly_chart(fig, use_container_width=True)

    # Emerging vs established group trend
    with b:

        trend = view.groupby(
            ["year", "group"],
            as_index=False
        )[primary_metric].mean()

        fig = px.line(
            trend,
            x="year",
            y=primary_metric,
            color="group",
            color_discrete_map=GROUP_COLORS,
            markers=True,
            title=f"Unweighted group average: {METRICS[primary_metric]}"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Group means are unweighted averages of available country "
        "observations; they are not GDP-weighted aggregates."
    )

    # Country data coverage
    st.subheader("Indicator coverage")

    coverage = (
        view.groupby(["group", "country"])
        .size()
        .rename("observations")
        .reset_index()
    )

    fig = px.bar(
        coverage,
        x="country",
        y="observations",
        color="group",
        color_discrete_map=GROUP_COLORS,
        title="Available country-year records"
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 2. COUNTRY PROFILES
# ============================================================

with tabs[1]:

    st.subheader("Individual country deep dive")

    profile_countries = sorted(view["country"].dropna().unique())

    chosen_country = st.selectbox(
        "Choose a country",
        profile_countries,
        key="profile_country_v3"
    )

    country_df = view[
        view.country == chosen_country
    ].sort_values("year")

    if country_df.empty:
        st.warning("No data available for the selected country and period.")
        st.stop()

    info_group = country_df["group"].iloc[0]
    st.markdown(
        f"**{chosen_country}** · {info_group} economy · "
        f"{int(country_df.year.min())}–{int(country_df.year.max())}"
    )

    # Country KPIs
    kpis = [
        "gdp_current_usd",
        "gdp_growth_pct",
        "gdp_per_capita_ppp",
        "life_expectancy"
    ]

    cols = st.columns(4)

    for colbox, key in zip(cols, kpis):

        if key in country_df and country_df[key].notna().any():

            val = country_df[key].dropna().iloc[-1]
            label = METRICS[key]

            if key in ["gdp_current_usd", "gdp_per_capita_ppp"]:
                shown = f"{val:,.0f}"
            else:
                shown = f"{val:,.2f}"

            colbox.metric(label, shown)

    # Selected country trend
    country_metric = st.selectbox(
        "Country indicator",
        available_metrics,
        format_func=lambda x: METRICS[x],
        key="country_metric"
    )

    fig = px.line(
        country_df,
        x="year",
        y=country_metric,
        color="country",
        color_discrete_map=COUNTRY_COLORS,
        markers=True,
        title=f"{chosen_country}: {METRICS[country_metric]} over time"
    )

    fig.update_traces(line=dict(width=2.5))

    st.plotly_chart(fig, use_container_width=True)

    # Country profile small multiples
    profile_cols = [
        x for x in [
            "gdp_growth_pct",
            "manufacturing_pct_gdp",
            "exports_pct_gdp",
            "life_expectancy",
            "internet_users_pct",
            "electricity_access_pct"
        ]
        if x in country_df and country_df[x].notna().any()
    ]

    if profile_cols:

        long = country_df[
            ["year", "country"] + profile_cols
        ].melt(
            id_vars=["year", "country"],
            var_name="indicator",
            value_name="value"
        )

        long["indicator"] = long["indicator"].map(METRICS)

        fig = px.line(
            long,
            x="year",
            y="value",
            color="country",
            color_discrete_map=COUNTRY_COLORS,
            facet_col="indicator",
            facet_col_wrap=2,
            title=f"{chosen_country}: selected indicator trajectories"
        )

        fig.update_traces(line=dict(width=2.5))
        fig.update_yaxes(matches=None)

        st.plotly_chart(fig, use_container_width=True)

    st.write("Country data table")
    st.dataframe(country_df, use_container_width=True)


# ============================================================
# 3. ECONOMIC COMPARISON
# ============================================================

with tabs[2]:

    st.subheader("Economic size, growth and income")

    metric_options = [
        x for x in [
            "gdp_current_usd",
            "gdp_constant_usd",
            "gdp_growth_pct",
            "gdp_per_capita_usd",
            "gdp_per_capita_ppp",
            "population"
        ]
        if x in available_metrics
    ]

    selected_econ = st.selectbox(
        "Economic measure",
        metric_options,
        format_func=lambda x: METRICS[x],
        key="econ_metric"
    )

    left, right = st.columns(2)

    # Individual country trends
    with left:

        fig = px.line(
            view,
            x="year",
            y=selected_econ,
            color="country",
            color_discrete_map=COUNTRY_COLORS,
            title=f"{METRICS[selected_econ]}: individual country trends"
        )

        fig.update_traces(line=dict(width=2.5))

        st.plotly_chart(fig, use_container_width=True)

    # Group distribution
    with right:

        fig = px.box(
            view,
            x="group",
            y=selected_econ,
            color="group",
            color_discrete_map=GROUP_COLORS,
            points="outliers",
            title=f"{METRICS[selected_econ]}: group distributions"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Latest country ranking
    snap = latest_by_country(view)

    fig = px.bar(
        snap,
        x="country",
        y=selected_econ,
        color="group",
        color_discrete_map=GROUP_COLORS,
        title=f"Country ranking: {METRICS[selected_econ]}"
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 4. INDUSTRY AND TRADE
# ============================================================

with tabs[3]:

    st.subheader("Industrial structure and external trade")

    industry = [
        x for x in [
            "manufacturing_pct_gdp",
            "exports_pct_gdp",
            "imports_pct_gdp",
            "trade_openness_pct_gdp"
        ]
        if x in view.columns
    ]

    if industry:

        col1, col2 = st.columns(2)

        # Manufacturing trends
        with col1:

            if (
                "manufacturing_pct_gdp" in view.columns
                and view["manufacturing_pct_gdp"].notna().any()
            ):

                fig = px.line(
                    view,
                    x="year",
                    y="manufacturing_pct_gdp",
                    color="country",
                    color_discrete_map=COUNTRY_COLORS,
                    title="Manufacturing value added (% GDP)"
                )

                fig.update_traces(line=dict(width=2.5))

            else:
                fig = go.Figure()
                fig.add_annotation(
                    text="Manufacturing data unavailable",
                    showarrow=False
                )

            st.plotly_chart(fig, use_container_width=True)

        # Exports and imports
        with col2:

            trade_vars = [
                x for x in [
                    "exports_pct_gdp",
                    "imports_pct_gdp"
                ]
                if x in view.columns and view[x].notna().any()
            ]

            if trade_vars:

                trade_long = view.melt(
                    id_vars=["country", "group", "year"],
                    value_vars=trade_vars,
                    var_name="trade_type",
                    value_name="share"
                )

                fig = px.line(
                    trade_long,
                    x="year",
                    y="share",
                    color="country",
                    color_discrete_map=COUNTRY_COLORS,
                    facet_col="trade_type",
                    title="Exports and imports (% GDP)"
                )

                fig.update_traces(line=dict(width=2.5))

                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("Export/import data unavailable.")

        # Trade openness
        if (
            "trade_openness_pct_gdp" in view.columns
            and view["trade_openness_pct_gdp"].notna().any()
        ):

            snap = latest_by_country(view)

            fig = px.bar(
                snap,
                x="country",
                y="trade_openness_pct_gdp",
                color="group",
                color_discrete_map=GROUP_COLORS,
                title="Trade openness: exports + imports (% GDP)"
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Trade/industry indicators are unavailable in this dataset.")


# ============================================================
# 5. HUMAN DEVELOPMENT
# ============================================================

with tabs[4]:

    st.subheader("Human development, connectivity and infrastructure")

    dev_vars = [
        x for x in [
            "life_expectancy",
            "internet_users_pct",
            "electricity_access_pct",
            "urban_population_pct",
            "unemployment_pct"
        ]
        if x in view.columns and view[x].notna().any()
    ]

    if dev_vars:

        chosen_dev = st.selectbox(
            "Development indicator",
            dev_vars,
            format_func=lambda x: METRICS[x]
        )

        # Country trends
        fig = px.line(
            view,
            x="year",
            y=chosen_dev,
            color="country",
            color_discrete_map=COUNTRY_COLORS,
            title=f"{METRICS[chosen_dev]}: country trends"
        )

        fig.update_traces(line=dict(width=2.5))

        st.plotly_chart(fig, use_container_width=True)

        # Latest country comparison
        snap = latest_by_country(view)

        fig = px.bar(
            snap,
            x="country",
            y=chosen_dev,
            color="group",
            color_discrete_map=GROUP_COLORS,
            title=f"Latest available {METRICS[chosen_dev]}"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Animated income vs life expectancy scatter plot
        if (
            "life_expectancy" in view.columns
            and "gdp_per_capita_ppp" in view.columns
        ):

            scatter = view.dropna(
                subset=["life_expectancy", "gdp_per_capita_ppp"]
            )

            if not scatter.empty:

                fig = px.scatter(
                    scatter,
                    x="gdp_per_capita_ppp",
                    y="life_expectancy",
                    color="country",
                    color_discrete_map=COUNTRY_COLORS,
                    animation_frame="year",
                    hover_name="country",
                    title="Income (PPP) vs life expectancy over time"
                )

                st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Human development indicators are unavailable.")


# ============================================================
# 6. STATISTICAL ANALYSIS
# ============================================================

with tabs[5]:

    st.subheader("Univariate distributions and descriptive statistics")

    stat_var = st.selectbox(
        "Select variable",
        available_metrics,
        format_func=lambda x: METRICS[x],
        key="stat_var"
    )

    d = view.dropna(subset=[stat_var])

    col1, col2 = st.columns(2)

    # Histogram
    with col1:

        fig = px.histogram(
            d,
            x=stat_var,
            color="group",
            color_discrete_map=GROUP_COLORS,
            marginal="box",
            barmode="overlay",
            opacity=.65,
            title=f"Histogram: {METRICS[stat_var]}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Violin plot
    with col2:

        fig = px.violin(
            d,
            x="group",
            y=stat_var,
            color="group",
            color_discrete_map=GROUP_COLORS,
            box=True,
            points="outliers",
            title=f"Violin distribution: {METRICS[stat_var]}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Descriptive statistics
    stats = d.groupby("country")[stat_var].agg(
        ["count", "mean", "median", "std", "min", "max", "skew"]
    ).round(3)

    st.write("Country-level descriptive statistics")
    st.dataframe(stats, use_container_width=True)

    # Country-wise box plot
    st.write("Country-wise box plot")

    fig = px.box(
        d,
        x="country",
        y=stat_var,
        color="group",
        color_discrete_map=GROUP_COLORS,
        points="outliers",
        title=f"{METRICS[stat_var]} by country"
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 7. MULTIVARIATE ANALYSIS
# ============================================================

with tabs[6]:

    st.subheader("Correlation and multivariate relationships")

    numeric_vars = [
        x for x in available_metrics
        if view[x].notna().sum() >= 3
    ]

    if len(numeric_vars) >= 2:

        corr = view[numeric_vars].corr(method="pearson")

        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title="Pearson correlation heatmap"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Not enough numeric indicators for correlation analysis.")

    st.caption(
        "Correlation is association, not causation. "
        "Pooled country-year observations are repeated measures."
    )

    pair_vars = [
        x for x in [
            "gdp_per_capita_ppp",
            "gdp_growth_pct",
            "life_expectancy",
            "manufacturing_pct_gdp",
            "internet_users_pct",
            "unemployment_pct"
        ]
        if x in numeric_vars
    ]

    # Scatter matrix
    if len(pair_vars) >= 2:

        pair = view[
            pair_vars + ["country", "group"]
        ].dropna()

        if not pair.empty:

            fig = px.scatter_matrix(
                pair,
                dimensions=pair_vars,
                color="group",
                color_discrete_map=GROUP_COLORS,
                hover_name="country",
                title="Multivariate scatter matrix"
            )

            st.plotly_chart(fig, use_container_width=True)

    # Standardized country-indicator heatmap
    snap = latest_by_country(view).set_index("country")

    heat_vars = [
        x for x in pair_vars
        if x in snap.columns
    ]

    if heat_vars:

        z = snap[heat_vars].apply(
            lambda s: (
                (s - s.mean()) / s.std(ddof=0)
                if s.std(ddof=0) != 0
                else s * 0
            ),
            axis=0
        )

        z.columns = [
            METRICS[x] for x in z.columns
        ]

        fig = px.imshow(
            z,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Latest country profile: standardized indicator heatmap"
        )

        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 8. CONVERGENCE AND DEVELOPMENT INDEX
# ============================================================

with tabs[7]:

    st.subheader("Economic convergence and composite development index")

    conv = convergence_table(view)

    emerging = conv[
        conv.group == "Emerging"
    ]

    if not emerging.empty:

        fig = px.line(
            emerging,
            x="year",
            y="income_ratio_to_established",
            color="country",
            color_discrete_map=COUNTRY_COLORS,
            title=(
                "GDP per capita PPP relative to "
                "established-country average"
            )
        )

        fig.update_traces(line=dict(width=2.5))

        # Parity reference line
        fig.add_hline(
            y=1,
            line_dash="dash",
            annotation_text="Parity with established average"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "A rising ratio indicates relative catch-up against the "
            "selected established-country mean. It does not by itself "
            "prove causation."
        )

    # Composite development index
    idx = build_development_index(view)

    idx_latest = latest_by_country(idx).dropna(
        subset=["development_index"]
    )

    if not idx_latest.empty:

        fig = px.bar(
            idx_latest.sort_values(
                "development_index",
                ascending=False
            ),
            x="country",
            y="development_index",
            color="group",
            color_discrete_map=GROUP_COLORS,
            title="Composite development index (0–100, latest available)"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            idx_latest[
                ["country", "group", "year", "development_index"]
            ].sort_values(
                "development_index",
                ascending=False
            ),
            use_container_width=True
        )

    st.write("Index dimensions and weights")

    st.dataframe(
        pd.DataFrame({
            "indicator": [
                METRICS[k] for k in INDEX_WEIGHTS
            ],
            "weight": list(INDEX_WEIGHTS.values()),
            "direction": [
                "Lower is better"
                if k == "unemployment_pct"
                else "Higher is better"
                for k in INDEX_WEIGHTS
            ]
        }),
        use_container_width=True
    )

    st.warning(
        "The index is an exploratory, sample-relative composite, "
        "not an official development measure. It uses annual "
        "cross-sectional min-max normalization and requires at "
        "least four of six dimensions."
    )


# ============================================================
# 9. DATA QUALITY
# ============================================================

with tabs[8]:

    st.subheader("Data quality and coverage")

    missing = pd.DataFrame({
        "missing_count": view.isna().sum(),
        "missing_percent": (
            view.isna().mean() * 100
        ).round(2)
    })

    st.dataframe(
        missing.sort_values(
            "missing_percent",
            ascending=False
        ),
        use_container_width=True
    )

    # Missingness heatmap
    heatcols = [
        x for x in available_metrics
    ]

    missmat = view[heatcols].isna().astype(int)

    missmat.index = (
        view.country.astype(str)
        + " "
        + view.year.astype("Int64").astype(str)
    )

    fig = px.imshow(
        missmat.T,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Missingness heatmap (1 = missing, 0 = observed)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # IQR outlier detection
    out_var = st.selectbox(
        "IQR outlier check",
        available_metrics,
        format_func=lambda x: METRICS[x],
        key="outlier_var"
    )

    s = view[out_var].dropna()

    if len(s) >= 4:

        q1, q3 = s.quantile([.25, .75])
        iqr = q3 - q1

        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr

        flagged = view[
            view[out_var].notna()
            & (
                (view[out_var] < low)
                | (view[out_var] > high)
            )
        ]

        st.write(
            f"IQR fences: {low:,.3f} to {high:,.3f} "
            f"· flagged observations: {len(flagged)}"
        )

        st.dataframe(
            flagged[["country", "year", out_var]],
            use_container_width=True
        )

    st.caption(
        "Outliers are flagged for investigation, not automatically "
        "removed. Missing values are not zero-filled."
    )


# ============================================================
# 10. DATA EXPLORER
# ============================================================

with tabs[9]:

    st.subheader("Dataset explorer")

    st.dataframe(
        view,
        use_container_width=True,
        height=500
    )

    st.download_button(
        "Download filtered data CSV",
        view.to_csv(index=False).encode("utf-8"),
        "filtered_economic_data.csv",
        "text/csv"
    )

    st.download_button(
        "Download latest country snapshot",
        latest.to_csv(index=False).encode("utf-8"),
        "latest_country_snapshot.csv",
        "text/csv"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Data: World Bank World Development Indicators API V2. "
    "Country groups are project-defined. Current-US-dollar GDP "
    "is nominal and affected by inflation and exchange rates."
)