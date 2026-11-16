
# Econolytics — Economic Data Exploration and Visualization

## Project Overview

Econolytics is an interactive data exploration and visualization project that studies economic indicators across selected emerging and established economies from 2000 to 2024.

The project uses data from the **World Bank World Development Indicators (WDI)** to explore economic growth, income, industrial development, trade and human development.

## Project Scope

- **Emerging economies (project-defined):** India, Brazil, Indonesia and Mexico.
- **Established economies (project-defined):** United States, Germany, Japan and United Kingdom.
- **Time period:** 2000–2024.
- **Data source:** World Bank World Development Indicators API V2.

The two country groups are analytical choices made for this project. They are not official World Bank emerging-market classifications.

## Features

The project consists of three main stages:

1. **Data Collection:** Downloads economic indicators from the World Bank API.
2. **Data Preprocessing:** Cleans, transforms and prepares the downloaded dataset.
3. **Data Visualization:** Presents the processed data through an interactive Streamlit dashboard.

## Dashboard Sections

The dashboard contains five sections:

1. **Overview**
   - Key dataset statistics.
   - Latest available indicator values by country.
   - Economic trends across the two country groups.

2. **Country Profiles**
   - Select an individual country.
   - Explore its economic indicators over time.
   - View its historical data.

3. **Country Comparison**
   - Compare economic indicators across countries.
   - Visualize historical trends.
   - Compare the latest available country values.

4. **Statistical Analysis**
   - Histograms to examine data distributions.
   - Box plots to compare distributions.
   - Descriptive statistics: count, mean, median, standard deviation, minimum and maximum.
   - Correlation heatmap to examine relationships between indicators.

5. **Data Explorer**
   - View the cleaned dataset.
   - Examine missing values and their percentages.
   - Download the filtered dataset as a CSV file.

## Economic Indicators

| Category | Indicators |
|---|---|
| Economic output | GDP (current US$), GDP (constant 2015 US$), GDP growth (%) |
| Income | GDP per capita (current US$), GDP per capita (PPP) |
| Demographics | Population, urban population (%) |
| Industry and trade | Manufacturing (% GDP), exports (% GDP), imports (% GDP) |
| Employment | Unemployment (%) |
| Human development | Life expectancy, internet users (%), electricity access (%) |

## Derived Features

The preprocessing stage calculates two additional indicators:

- **Trade openness:** Exports (% GDP) + Imports (% GDP).
- **GDP per capita annual percentage change:** Calculated using the percentage change between consecutive yearly GDP-per-capita observations for each country.

## Technologies Used

- **Python** — Programming language.
- **Pandas** — Data manipulation and preprocessing.
- **NumPy** — Numerical operations.
- **Requests** — Fetching data from the World Bank API.
- **Streamlit** — Interactive dashboard development.
- **Plotly** — Interactive data visualizations.

## Project Structure

```text
Econolytics/
│
├── app.py
├── config.py
├── fetch_data.py
├── preprocess.py
├── analysis_utils.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   │   └── world_bank_raw.csv
│   │
│   └── processed/
│       └── economic_data_clean.csv
│
└── reports/
    ├── missing_values.csv
    └── descriptive_statistics.csv
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/Shriram15/Econolytics.git
cd Econolytics
```

### 2. Create a virtual environment

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the data

**macOS / Linux:**

```bash
python3 fetch_data.py
```

**Windows:**

```powershell
python fetch_data.py
```

### 5. Preprocess the data

**macOS / Linux:**

```bash
python3 preprocess.py
```

**Windows:**

```powershell
python preprocess.py
```

### 6. Launch the dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser. The initial data download requires an internet connection. Once the processed CSV file has been generated, the dashboard reads the local dataset.

## Important Interpretation Considerations

- GDP at current US$ is affected by inflation and exchange-rate movements.
- GDP at constant 2015 US$ is more suitable for comparing real GDP levels over time.
- GDP growth (%) represents the annual real GDP growth rate.
- GDP per capita PPP is useful for broad international living-standard comparisons, but does not account for income inequality.
- Country-year observations are repeated measurements over time. Correlations should therefore be interpreted descriptively.
- Correlation does not imply causation.
- Missing values are retained rather than automatically replaced with zero.
- Group averages are unweighted averages of the available country observations.

## Data Sources

1. [World Bank — World Development Indicators](https://databank.worldbank.org/source/world-development-indicators)
2. [World Bank — Indicators API Overview](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api)
3. [World Bank — API Basic Call Structures](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures)
4. [World Bank — Country Classification](https://datahelpdesk.worldbank.org/knowledgebase/articles/378834-how-does-the-world-bank-classify-countries)

---

**Econolytics — Exploring Global Economic Trends Through Data.**
