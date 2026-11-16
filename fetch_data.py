
import requests
import pandas as pd
from pathlib import Path

from config import COUNTRIES, INDICATORS, START_YEAR, END_YEAR


# Folder to save the downloaded data
BASE = Path(__file__).resolve().parent
RAW_DIR = BASE / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

API = "https://api.worldbank.org/v2"


# Download data for one indicator
def fetch_indicator(key, label, code):

    print("Fetching:", label)

    country_codes = ";".join(COUNTRIES.keys())

    url = f"{API}/country/{country_codes}/indicator/{code}"

    params = {
        "date": f"{START_YEAR}:{END_YEAR}",
        "format": "json",
        "per_page": 20000
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    result = response.json()

    if len(result) < 2 or result[1] is None:
        print("No data available for:", label)
        return pd.DataFrame(columns=["country_code", "year", key])

    rows = []

    for item in result[1]:

        country_code = item["countryiso3code"]

        if country_code in COUNTRIES:

            rows.append({
                "country_code": country_code,
                "year": int(item["date"]),
                key: item["value"]
            })

    return pd.DataFrame(rows)


# Main function
def main():

    final_data = None

    # Fetch every indicator
    for key, (label, code, unit) in INDICATORS.items():

        data = fetch_indicator(key, label, code)

        if final_data is None:
            final_data = data

        else:
            final_data = pd.merge(
                final_data,
                data,
                on=["country_code", "year"],
                how="outer"
            )

    if final_data is None or final_data.empty:
        print("No data was downloaded.")
        return

    # Add country names
    final_data["country"] = final_data["country_code"].map(
        lambda x: COUNTRIES[x]["name"]
    )

    # Add economic groups
    final_data["group"] = final_data["country_code"].map(
        lambda x: COUNTRIES[x]["group"]
    )

    # Sort the dataset
    final_data = final_data.sort_values(
        ["country_code", "year"]
    )

    # Save as CSV
    output_file = RAW_DIR / "world_bank_raw.csv"

    final_data.to_csv(output_file, index=False)

    print("\nData downloaded successfully!")
    print("Dataset shape:", final_data.shape)
    print("Countries:", final_data["country"].nunique())
    print("Saved to:", output_file)


if __name__ == "__main__":
    main()
