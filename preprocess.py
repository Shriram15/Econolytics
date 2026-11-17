"""Prepare analysis-ready data and auditable quality reports."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from config import COUNTRIES, INDICATORS

BASE = Path(__file__).resolve().parent
RAW = BASE / "data/raw/world_bank_raw.csv"
OUT = BASE / "data/processed"
REPORTS = BASE / "reports"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

def main():
    if not RAW.exists():
        raise FileNotFoundError("Run python fetch_data.py first.")
    df = pd.read_csv(RAW)
    initial_rows = len(df)
    initial_duplicate_keys = int(df.duplicated(["country_code", "year"]).sum())

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    for col in INDICATORS:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["country_code"] = df["country_code"].astype(str).str.upper().str.strip()
    df = df.drop_duplicates()
    df = df.drop_duplicates(["country_code", "year"], keep="last")
    df = df[df.country_code.isin(COUNTRIES) & df.year.between(2000, 2024)].copy()

    # Range checks; invalid values become NaN, never arbitrary zeros.
    bounds = {
        "gdp_current_usd": (0, None), "gdp_constant_usd": (0, None),
        "gdp_per_capita_usd": (0, None), "gdp_per_capita_ppp": (0, None),
        "population": (0, None), "life_expectancy": (0, 120),
        "internet_users_pct": (0, 100), "electricity_access_pct": (0, 100),
        "urban_population_pct": (0, 100), "unemployment_pct": (0, 100),
        "manufacturing_pct_gdp": (None, 100),
        "exports_pct_gdp": (0, None), "imports_pct_gdp": (0, None),
    }
    invalid_counts = {}
    for col, (low, high) in bounds.items():
        if col not in df:
            continue
        bad = pd.Series(False, index=df.index)
        if low is not None:
            bad |= df[col].notna() & (df[col] < low)
        if high is not None:
            bad |= df[col].notna() & (df[col] > high)
        invalid_counts[col] = int(bad.sum())
        df.loc[bad, col] = np.nan

    df = df.sort_values(["country_code", "year"]).reset_index(drop=True)
    df["trade_openness_pct_gdp"] = df["exports_pct_gdp"] + df["imports_pct_gdp"]
    df["gdp_per_capita_yoy_pct"] = (
        df.groupby("country_code")["gdp_per_capita_usd"].pct_change() * 100
    )
    df["real_gdp_yoy_pct_check"] = (
        df.groupby("country_code")["gdp_constant_usd"].pct_change() * 100
    )

    missing = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_pct": (df.isna().mean() * 100).round(2)
    })
    missing.to_csv(REPORTS / "missing_values.csv")

    outlier_records = []
    for col in INDICATORS:
        if col not in df:
            continue
        s = df[col].dropna()
        if len(s) < 4:
            continue
        q1, q3 = s.quantile([.25, .75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        bad = df[col].notna() & ((df[col] < low) | (df[col] > high))
        for _, r in df.loc[bad, ["country", "year", col]].iterrows():
            outlier_records.append({
                "country": r.country, "year": int(r.year), "indicator": col,
                "value": float(r[col]), "lower_fence": float(low), "upper_fence": float(high)
            })
    pd.DataFrame(outlier_records).to_csv(REPORTS / "outlier_flags.csv", index=False)
    df.describe(include="all").T.to_csv(REPORTS / "descriptive_statistics.csv")
    df.to_csv(OUT / "economic_data_clean.csv", index=False)

    summary = {
        "initial_rows": initial_rows,
        "initial_duplicate_country_year_keys": initial_duplicate_keys,
        "cleaned_rows": int(len(df)),
        "countries_present": sorted(df.country.dropna().unique().tolist()),
        "year_min": int(df.year.min()) if df.year.notna().any() else None,
        "year_max": int(df.year.max()) if df.year.notna().any() else None,
        "invalid_values_changed_to_missing": invalid_counts,
        "missing_by_column": df.isna().sum().to_dict(),
        "missing_policy": "No blanket imputation; missing values retained.",
        "outlier_policy": "IQR flags reported; observations retained."
    }
    (REPORTS / "data_quality_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"Cleaned data saved: {OUT / 'economic_data_clean.csv'}")
    print(f"Rows: {initial_rows} -> {len(df)}")
    print("Reports saved to:", REPORTS)

if __name__ == "__main__":
    main()
