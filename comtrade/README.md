# Comtrade API

Report on tariffs, product prices, and trade data by country, enabling basket assembly using HS codes, integration-ready workflows

Jupyter Notebook, processed datasets (CSV), and visualizations (bar chart, line chart, heatmap)

### Includes:

1. comtrade-report.ipynb (Notebook)

2. comtrade-output.csv (Dataset)

3. comtrade-report.pdf (Report)

### Issue:

Unable to limit rows returned. Tried maxrec, count, max, and cdlimit parameters to limit the records. Instead, the API returns all available records.

[Example of API call](https://comtradeapi.un.org/public/v1/getDATariffline/C/M/HS?reporter=USA&year=2020&trade_type=1)