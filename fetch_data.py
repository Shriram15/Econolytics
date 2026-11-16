"""Download WDI data. Bulk requests fall back to country-by-country requests."""
from pathlib import Path
import time
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import COUNTRIES, INDICATORS, START_YEAR, END_YEAR

BASE = Path(__file__).resolve().parent
RAW_DIR = BASE / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
API = "https://api.worldbank.org/v2"

def make_session():
    retry = Retry(
        total=3, connect=3, read=3, backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"], respect_retry_after_header=True
    )
    s = requests.Session()
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.headers.update({"User-Agent": "GlobalEconomicIntelligenceStudentProject/1.0"})
    return s

def get_country_indicator(session, country_codes, key, code):
    url = f"{API}/country/{country_codes}/indicator/{code}"
    params = {"date": f"{START_YEAR}:{END_YEAR}", "format": "json", "per_page": 20000}
    response = session.get(url, params=params, timeout=(20, 75))
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2:
        raise RuntimeError(f"Unexpected API response for {code}: {str(payload)[:200]}")
    rows = []
    for item in payload[1] or []:
        iso = item.get("countryiso3code")
        if iso in COUNTRIES:
            rows.append({
                "country_code": iso,
                "year": int(item["date"]),
                key: item.get("value")
            })
    return pd.DataFrame(rows, columns=["country_code", "year", key])

def fetch_with_fallback(session, key, label, code):
    codes = ";".join(COUNTRIES.keys())
    try:
        print(f"  Bulk request: {label}")
        return get_country_indicator(session, codes, key, code)
    except (requests.RequestException, ValueError, RuntimeError) as exc:
        print(f"  Bulk request failed ({exc}); retrying country by country.")
        parts = []
        for iso in COUNTRIES:
            try:
                part = get_country_indicator(session, iso, key, code)
                parts.append(part)
                print(f"    {iso}: {len(part)} rows")
            except Exception as country_exc:
                print(f"    WARNING {iso} {key}: {country_exc}")
            time.sleep(0.25)
        return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(
            columns=["country_code", "year", key]
        )

def main():
    session = make_session()
    merged = None
    for i, (key, (label, code, unit)) in enumerate(INDICATORS.items(), 1):
        print(f"\nIndicator {i}/{len(INDICATORS)}")
        part = fetch_with_fallback(session, key, label, code)
        if not part.empty:
            part[key] = pd.to_numeric(part[key], errors="coerce")
            part = part.drop_duplicates(["country_code", "year"])
        if merged is None:
            merged = part
        else:
            merged = merged.merge(part, on=["country_code", "year"], how="outer",
                                  validate="one_to_one")
        time.sleep(0.4)

    if merged is None or merged.empty:
        raise RuntimeError("No data retrieved. Test the API URL in a browser and retry.")

    merged["country"] = merged["country_code"].map({k:v["name"] for k,v in COUNTRIES.items()})
    merged["group"] = merged["country_code"].map({k:v["group"] for k,v in COUNTRIES.items()})
    merged = merged.sort_values(["country_code", "year"]).reset_index(drop=True)
    out = RAW_DIR / "world_bank_raw.csv"
    merged.to_csv(out, index=False)
    print(f"\nSaved {out}")
    print(f"Shape: {merged.shape}; countries: {merged.country.nunique()}")
    print(merged.groupby(["group", "country"]).size().to_string())

if __name__ == "__main__":
    main()
