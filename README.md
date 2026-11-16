# Global Economic Intelligence — EDA Project

## Scope
- Emerging (project-defined): India, Brazil, Indonesia, Mexico
- Established (project-defined): United States, Germany, Japan, United Kingdom
- Period: 2000–2024
- Source: World Bank World Development Indicators (WDI), Indicators API V2

The two country groups are analytical choices for this project, not official World Bank emerging-market classifications.

## Run on Windows
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python fetch_data.py
python preprocess.py
streamlit run app.py
```

The downloader first attempts a bulk request and falls back to country-by-country requests if the bulk request fails. The initial download needs internet. After data files are created, the dashboard reads the local processed CSV.

## Dashboard sections
1. Global overview
2. Country profiles — individual country deep dives
3. Economic comparison
4. Industry and trade
5. Human development
6. Statistical analysis — histograms, box plots, violin plots, descriptive statistics
7. Multivariate analysis — correlation heatmap, scatter matrix, standardized profile heatmap
8. Convergence and development index
9. Data quality — missingness heatmap and IQR outliers
10. Data explorer — table and CSV downloads

## Indicators
GDP current US$, GDP constant 2015 US$, GDP growth, GDP per capita current US$, GDP per capita PPP, population, manufacturing share, exports share, imports share, unemployment, life expectancy, internet usage, electricity access, urban population.

## Derived features
- Trade openness = exports (% GDP) + imports (% GDP)
- GDP per capita annual percentage change
- Real GDP constant-price annual percentage change check
- Exploratory composite development index

## Composite index methodology
Six dimensions: PPP GDP per capita (30%), life expectancy (25%), internet usage (15%), electricity access (15%), manufacturing value added (10%), unemployment (5%). Each is min-max normalized within each year across the selected sample. Unemployment is reverse-scored. At least four of six dimensions must be observed. The score is rescaled to 0–100 after renormalizing available weights.

This is an exploratory sample-relative index, not an official development index. Its score depends on country sample, year, selected dimensions and chosen weights. Test sensitivity to weights before making strong conclusions.

## Important interpretation cautions
- GDP at current US$ is nominal and affected by inflation and exchange rates.
- GDP constant 2015 US$ is better for comparing real output levels over time.
- GDP growth annual % is a real growth-rate measure.
- GDP per capita PPP is more suitable than current-US-dollar GDP per capita for broad living-standard comparisons, but still does not measure income distribution.
- Country-year observations are repeated measures; pooled correlations should be interpreted descriptively.
- Correlation does not imply causation.
- Missing observations are retained; there is no blanket zero-fill.
- IQR outliers are flagged, not automatically deleted.
- Group averages in this dashboard are unweighted country means.

## Official sources
- WDI: https://databank.worldbank.org/source/world-development-indicators
- Indicators API overview: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api
- API basic call structures: https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures
- World Bank country classifications: https://datahelpdesk.worldbank.org/knowledgebase/articles/378834-how-does-the-world-bank-classify-countries
- Emerging markets note: https://datahelpdesk.worldbank.org/knowledgebase/articles/114958-what-are-emerging-markets
