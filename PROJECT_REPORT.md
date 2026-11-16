# Global Economic Intelligence
## Emerging Economies vs Established Global Powers
### Project report framework

## 1. Introduction
This project explores economic performance and development patterns across eight selected countries from 2000 to 2024. Four countries are assigned to an emerging-economy group and four to an established-power group for the purpose of comparative analysis.

## 2. Problem statement
Total GDP alone cannot provide a complete comparison of economic progress. Population size, price changes and exchange rates influence nominal GDP. This project therefore examines real output, income per person, industrial structure, trade, employment, health, connectivity and infrastructure.

## 3. Countries and analytical grouping
Emerging (project-defined): India, Brazil, Indonesia and Mexico.
Established (project-defined): United States, Germany, Japan and United Kingdom.
These group labels are project-defined and should not be presented as a universal or official classification.

## 4. Objectives
- Collect annual comparable economic and development indicators.
- Profile each country individually.
- Compare country and group trends.
- Explore distributions, relationships and multivariate patterns.
- Evaluate relative income convergence.
- Build an exploratory composite development index.
- Communicate findings through an interactive dashboard.

## 5. Data source and variables
Primary source: World Bank World Development Indicators API V2. Variables include GDP (current and constant-price), GDP growth, GDP per capita (current US$ and PPP), population, manufacturing share, exports, imports, unemployment, life expectancy, internet usage, electricity access and urban population.

## 6. Methodology
1. Retrieve country-year indicator observations from the World Bank API.
2. Merge indicator data by ISO country code and year.
3. Inspect data types, dimensions, duplicate keys and missingness.
4. Clean invalid values and preserve genuine missing observations.
5. Engineer trade openness and annual per-capita changes.
6. Perform country-wise and cross-country statistical analysis.
7. Use descriptive statistics, bar charts, time-series charts, histograms, box plots, violin plots, heatmaps and scatter matrices.
8. Evaluate relative PPP income convergence.
9. Construct a sample-relative composite index with explicit weights.
10. Present results in Streamlit.

## 7. Analysis modules
- Country profiles: individual time trends, latest indicators and descriptive summaries.
- Economic comparison: GDP levels, real growth, GDP per capita and population.
- Industry and trade: manufacturing, exports, imports and trade openness.
- Human development: life expectancy, internet, electricity, urbanization and unemployment.
- Statistical analysis: mean, median, standard deviation, skewness, distributions and outlier inspection.
- Multivariate analysis: correlation heatmap, scatter matrix and standardized country profile heatmap.
- Convergence: emerging-country PPP GDP per capita relative to the established-country mean.
- Composite index: annual min-max normalization of six dimensions with documented weights.

## 8. Interpretation limitations
- Current-US-dollar GDP is affected by inflation and exchange rates.
- PPP GDP per capita does not describe inequality or distribution.
- Group means are unweighted country averages.
- Correlations are not causal evidence.
- Observations are repeated within countries over time.
- Indicator coverage varies by country and year.
- Composite-index scores depend on the selected sample, variables and weights.

## 9. Results
Populate this section only after running the pipeline and inspecting the actual retrieved dataset and dashboard. Report data coverage, missingness, country-level trends, group differences, convergence patterns and index rankings with charts and evidence. Do not invent numerical findings.

## 10. Conclusion
The final conclusion should state which indicators show convergence, divergence or persistent gaps, identify differences among individual countries, and acknowledge limitations. Avoid claiming that all emerging economies follow the same trajectory.
