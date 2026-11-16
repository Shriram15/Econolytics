
from pathlib import Path
import pandas as pd

from config import COUNTRIES, INDICATORS, START_YEAR, END_YEAR


# File locations
BASE = Path(__file__).resolve().parent

RAW_FILE = BASE / "data" / "raw" / "world_bank_raw.csv"
OUTPUT_DIR = BASE / "data" / "processed"
REPORT_DIR = BASE / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    # Check whether raw data exists
    if not RAW_FILE.exists():
        print("Raw data not found. Run fetch_data.py first.")
        return

    # Load raw dataset
    df = pd.read_csv(RAW_FILE)

    print("Original dataset shape:", df.shape)

    # Convert year and indicator columns to numeric
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    for column in INDICATORS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # Clean country codes
    df["country_code"] = (
        df["country_code"].astype(str).str.strip().str.upper()
    )

    # Remove duplicate records
    df = df.drop_duplicates(subset=["country_code", "year"])

    # Keep only selected countries and years
    df = df[
        df["country_code"].isin(COUNTRIES)
        & df["year"].between(START_YEAR, END_YEAR)
    ].copy()

    # Sort the dataset
    df = df.sort_values(
        ["country_code", "year"]
    ).reset_index(drop=True)

    # Calculate trade openness
    df["trade_openness_pct_gdp"] = (
        df["exports_pct_gdp"] + df["imports_pct_gdp"]
    )

    # Calculate annual GDP per capita percentage change
    df["gdp_per_capita_yoy_pct"] = (
        df.groupby("country_code")["gdp_per_capita_usd"]
        .pct_change() * 100
    )

    # Generate missing-value report
    missing_report = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percentage": (df.isna().mean() * 100).round(2)
    })

    missing_report.to_csv(
        REPORT_DIR / "missing_values.csv"
    )

    # Generate descriptive statistics
    df.describe().T.to_csv(
        REPORT_DIR / "descriptive_statistics.csv"
    )

    # Save cleaned dataset
    output_file = OUTPUT_DIR / "economic_data_clean.csv"

    df.to_csv(output_file, index=False)

    print("\nData preprocessing completed!")
    print("Cleaned dataset shape:", df.shape)
    print("Countries:", df["country"].nunique())
    print("Year range:", int(df["year"].min()), "-", int(df["year"].max()))
    print("Saved to:", output_file)
    print("Reports saved to:", REPORT_DIR)


if __name__ == "__main__":
    main()
