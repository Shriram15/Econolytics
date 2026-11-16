# Econolytics
## Economic Data Exploration and Visualization
### Project Report

## 1. Introduction
This project explores economic performance and development patterns across eight selected countries from 2000 to 2024. Four countries are assigned to an emerging-economy group and four to an established-power group for the purpose of comparative analysis.

## 2. Problem statement
Total GDP alone cannot provide a complete comparison of economic progress. Population size, price changes and exchange rates influence nominal GDP. This project therefore examines real output, income per person, industrial structure, trade, employment, health, connectivity and infrastructure.

## 3. Countries and analytical grouping
Emerging (project-defined): India, Brazil, Indonesia and Mexico.
Established (project-defined): United States, Germany, Japan and United Kingdom.
These group labels are project-defined and should not be presented as a universal or official classification.

## 4. Objectives

- Collect annual economic and development indicators from the World Bank.
- Explore economic trends across selected emerging and established economies.
- Analyse individual country performance over time.
- Compare economic indicators across countries.
- Apply data cleaning and preprocessing techniques to prepare the dataset.
- Perform exploratory data analysis using descriptive statistics and visualizations.
- Examine distributions, missing values and correlations among economic indicators.
- Develop an interactive dashboard for exploring and comparing economic data.


## 5. Data Source and Variables

### 5.1 Data Source

The primary data source for this project is the **World Bank World Development Indicators (WDI) API V2**.

The dataset contains annual economic and development indicators for eight selected countries covering the period 2000–2024.

### 5.2 Economic Indicators

The project uses the following indicators:

| Category | Indicators |
|---|---|
| Economic Output | GDP (current US$), GDP (constant 2015 US$), GDP growth (%) |
| Income | GDP per capita (current US$), GDP per capita (PPP) |
| Demographics | Total population, urban population (%) |
| Industry and Trade | Manufacturing (% GDP), exports (% GDP), imports (% GDP) |
| Employment | Unemployment (%) |
| Human Development | Life expectancy, internet users (%), electricity access (%) |

### 5.3 Derived Variables

Two additional variables are calculated during preprocessing:

1. **Trade Openness (% GDP):** Calculated as the sum of exports and imports as percentages of GDP.

2. **GDP Per Capita Annual Percentage Change:** Calculated using the percentage change in GDP per capita (current US$) between consecutive years for each country.

### 5.4 Dataset Dimensions

The final processed dataset contains:
- 8 countries.
- 25 years of observations per country.
- 200 country-year observations.
- 20 columns, including country information, original indicators and derived variables.



## 6. Methodology

The project follows a structured data collection, preprocessing and exploratory data analysis workflow.

1. **Data Collection:** Retrieve annual economic indicators for the eight selected countries using the World Bank World Development Indicators API V2.

2. **Data Integration:** Merge the downloaded indicator datasets using country codes and year as common keys.

3. **Data Cleaning:** Convert year and indicator columns into appropriate numeric data types, standardize country codes and remove duplicate country-year records.

4. **Data Filtering:** Retain observations belonging to the selected countries and the study period of 2000–2024.

5. **Feature Engineering:** Calculate trade openness as the sum of exports and imports as percentages of GDP. Calculate the annual percentage change in GDP per capita for each country.

6. **Missing Data Analysis:** Generate a report containing missing-value counts and percentages for each column.

7. **Descriptive Statistical Analysis:** Generate summary statistics to understand the distribution and characteristics of the economic indicators.

8. **Data Visualization:** Use interactive charts, including bar charts, line charts, histograms, box plots and correlation heatmaps, to explore economic patterns and relationships.

9. **Interactive Dashboard:** Develop a Streamlit application that allows users to filter data by year and country, select economic indicators, compare countries and download filtered datasets.

10. **Result Interpretation:** Interpret the observed trends, distributions and relationships while considering data limitations and the descriptive nature of the analysis.



## 7. Analysis Modules

The Econolytics dashboard consists of five main modules:

### 7.1 Overview

- Displays the number of selected countries, years and observations.
- Compares the latest available values of the selected economic indicator across countries.
- Visualizes average economic trends across emerging and established country groups.

### 7.2 Country Profiles

- Allows users to select an individual country.
- Displays its economic group.
- Visualizes historical trends for selected economic indicators.
- Provides access to the country's historical dataset.

### 7.3 Country Comparison

- Compares selected economic indicators across countries.
- Displays historical trends using interactive line charts.
- Compares the latest available indicator values using bar charts.

### 7.4 Statistical Analysis

- Uses histograms to examine the distribution of economic indicators.
- Uses box plots to compare distributions across economic groups.
- Calculates descriptive statistics, including count, mean, median, standard deviation, minimum and maximum.
- Uses a correlation heatmap to examine relationships between numerical economic indicators.

### 7.5 Data Explorer

- Displays the cleaned economic dataset.
- Provides missing-value counts and percentages for each column.
- Allows users to download the filtered dataset in CSV format.



## 8. Interpretation Limitations

The analysis has the following limitations:

1. **Current US Dollar Values:** GDP and GDP per capita at current US$ are affected by inflation and exchange-rate fluctuations.

2. **Constant Price GDP:** GDP at constant 2015 US$ provides a better basis for comparing real output over time, but does not represent purchasing power differences between countries.

3. **Purchasing Power Parity:** GDP per capita PPP accounts for differences in price levels but does not capture income inequality or income distribution.

4. **Missing Data:** World Bank indicator coverage varies across countries and years. Missing observations may affect comparisons and statistical results.

5. **Group Averages:** Emerging and established economy trends are calculated using unweighted averages of available country observations. Each country therefore contributes equally to its group's average.

6. **Correlation:** Correlation analysis identifies statistical relationships between variables but does not establish causation.

7. **Repeated Observations:** The dataset contains annual observations for the same countries over multiple years. These observations are not necessarily statistically independent.

8. **Country Grouping:** The emerging and established classifications are defined specifically for this project and should not be interpreted as official or universal classifications.



## 9. Results and Observations

The analysis was performed using the cleaned dataset containing 200 observations across eight countries for the period 2000–2024.

### 9.1 Dataset Overview

- The final dataset contains 200 rows and 20 columns.
- All eight selected countries have 25 annual observations each.
- The dataset covers the complete study period from 2000 to 2024.
- The dataset contains original economic indicators and two derived features: trade openness and GDP per capita annual percentage change.

### 9.2 Missing Data Analysis

The missing-value analysis identified:

- Manufacturing value added (% GDP): 3 missing observations, representing 1.5% of the dataset.
- GDP per capita annual percentage change: 8 missing observations, representing 4% of the dataset.
- All remaining columns contain no missing observations.

The missing annual percentage-change values are associated with the initial observations for each country's time series, where a previous year's value is unavailable for calculating percentage change.

### 9.3 Economic Growth Comparison

The average GDP growth rate across the study period was:

- Emerging economy group: 3.79%.
- Established economy group: 1.45%.

The selected emerging economies recorded a higher average GDP growth rate than the selected established economies during the study period.

These values represent averages across available country-year observations and do not imply that every emerging economy grew faster than every established economy.

### 9.4 Life Expectancy Comparison

The average life expectancy across the study period was:

- Emerging economy group: 70.86 years.
- Established economy group: 80.30 years.

The established economy group recorded a higher average life expectancy than the emerging economy group.

This indicates differences in the average health and demographic outcomes of the two selected country groups.

### 9.5 GDP Per Capita at Purchasing Power Parity

The latest available GDP per capita PPP observations for 2024 were:

| Country | GDP per capita PPP (2024) |
|---|---:|
| United States | 86,169.66 |
| Germany | 73,957.00 |
| United Kingdom | 62,839.47 |
| Japan | 54,156.27 |
| Mexico | 25,820.35 |
| Brazil | 22,370.92 |
| Indonesia | 16,472.48 |
| India | 10,718.59 |

The results show considerable differences in purchasing-power-adjusted income per person across the selected countries. The four established economies recorded higher values than the four emerging economies in 2024.

### 9.6 Overall Observations

The exploratory analysis highlights differences in economic growth, income levels and life expectancy across the selected countries.

The results indicate that higher average economic growth does not necessarily correspond to higher average income per person or life expectancy.

The dashboard enables further exploration of these patterns through country profiles, comparative visualizations, descriptive statistics and correlation analysis.



## 10. Conclusion

Econolytics demonstrates the application of data collection, preprocessing, exploratory data analysis and interactive visualization to the study of economic indicators across eight selected countries from 2000 to 2024.

The project uses World Bank World Development Indicators data to examine economic performance across two project-defined groups: emerging and established economies.

The analysis produced several observations:

1. The selected emerging economies recorded a higher average GDP growth rate of 3.79%, compared with 1.45% for the established economies.

2. The established economies recorded a higher average life expectancy of 80.30 years, compared with 70.86 years for the emerging economies.

3. The 2024 GDP per capita PPP observations showed higher values for all four selected established economies than for the four selected emerging economies.

4. The dataset provided complete annual coverage for all eight countries, with limited missing observations in manufacturing and the derived GDP per capita annual percentage-change indicator.

The project also demonstrates how Python libraries such as Pandas, NumPy and Plotly can be used for data manipulation, statistical analysis and visualization, while Streamlit provides an interactive interface for exploring economic data.

Overall, Econolytics provides a structured platform for examining economic trends, comparing countries and identifying relationships between economic and development indicators.

The findings are descriptive and limited to the selected countries, indicators and study period. Further research could extend the analysis to additional countries, incorporate more indicators and apply advanced statistical techniques to investigate long-term economic relationships.
