COUNTRIES = {
    "IND": {"name": "India", "group": "Emerging"},
    "BRA": {"name": "Brazil", "group": "Emerging"},
    "IDN": {"name": "Indonesia", "group": "Emerging"},
    "MEX": {"name": "Mexico", "group": "Emerging"},
    "USA": {"name": "United States", "group": "Established"},
    "DEU": {"name": "Germany", "group": "Established"},
    "JPN": {"name": "Japan", "group": "Established"},
    "GBR": {"name": "United Kingdom", "group": "Established"},
}
START_YEAR = 2000
END_YEAR = 2024

# Keys are stable internal column names; values are (display label, WDI code, unit).
INDICATORS = {
    "gdp_current_usd": ("GDP (current US$)", "NY.GDP.MKTP.CD", "US$"),
    "gdp_constant_usd": ("GDP (constant 2015 US$)", "NY.GDP.MKTP.KD", "constant 2015 US$"),
    "gdp_growth_pct": ("GDP growth (annual %)", "NY.GDP.MKTP.KD.ZG", "%"),
    "gdp_per_capita_usd": ("GDP per capita (current US$)", "NY.GDP.PCAP.CD", "US$ per person"),
    "gdp_per_capita_ppp": ("GDP per capita, PPP (current international $)", "NY.GDP.PCAP.PP.CD", "international $"),
    "population": ("Population, total", "SP.POP.TOTL", "people"),
    "manufacturing_pct_gdp": ("Manufacturing value added (% GDP)", "NV.IND.MANF.ZS", "%"),
    "exports_pct_gdp": ("Exports of goods and services (% GDP)", "NE.EXP.GNFS.ZS", "%"),
    "imports_pct_gdp": ("Imports of goods and services (% GDP)", "NE.IMP.GNFS.ZS", "%"),
    "unemployment_pct": ("Unemployment, modeled ILO estimate (%)", "SL.UEM.TOTL.ZS", "%"),
    "life_expectancy": ("Life expectancy at birth (years)", "SP.DYN.LE00.IN", "years"),
    "internet_users_pct": ("Individuals using the Internet (%)", "IT.NET.USER.ZS", "%"),
    "electricity_access_pct": ("Access to electricity (%)", "EG.ELC.ACCS.ZS", "%"),
    "urban_population_pct": ("Urban population (% of total)", "SP.URB.TOTL.IN.ZS", "%"),
}
