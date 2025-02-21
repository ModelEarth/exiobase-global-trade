# Comtrade API

## Objective
This project aims to develop an open-source solution to:
1. Include reporting on changing trade tariffs.
2. Fetch data related to consumer products, prices, and tariff rates by country.
3. Allow the assembly of a basket of goods using industry sector or commodity codes.
4. Ensure the solution integrates seamlessly with Model.Earth workflows.

## Summary of Work Completed
1. **Selected API**: UN Comtrade API (Public Version).
2. **Key Features Implemented**: 
   - Fetch trade and tariff data by country, partner, year, and product using HS Codes.
   - Process and aggregate data for insights.
   - Visualize trade flows, tariff impacts, and trends.
   - Extract the most recent year's trade records for further analysis, including **month-over-month growth rate calculations** and **anomaly detection using Z-scores**.
   - Integrate with Model.Earth by providing reproducible and clear outputs.

## Key Steps Undertaken
1. **Explored Open-Source Options**:
   - Evaluated UN Comtrade API and WITS API.
   - Selected UN Comtrade due to its extensive trade and tariff data, including support for HS codes and flexible API queries.

2. **Implemented Data Retrieval**:
   - Developed Python Jupyter Notebook to query the UN Comtrade Public API.
   - Sample query parameters include:
     - **Reporter**: USA (or any other country ISO code).
     - **Partner**: World, or specific trading partners (e.g., China).
     - **Year**: Historical data from 2000 onwards.
     - **Product**: Specific HS codes or all products.

3. **Processed and Cleaned Data**:
   - Removed unnecessary columns like metadata flags.
   - Transformed period into a datetime format for easier time-series analysis.
   - Aggregated total records by reporter country, partner, and period.
   - Extracted **HS Code-level yearly trends** to analyze long-term trade patterns.
   - Filtered data for the **most recent year** to enable **short-term trade insights**.
   - Computed **month-over-month (MoM) growth rates** for each HS Code.
   - Identified **outliers using Z-score analysis** to detect anomalies in trade records.

4. **Generated Visualizations**:
   - **Bar Plot**: Top countries by total trade records.
   - **Line Chart**: Trade trends over time.
   - **Heatmap**: Relationships between countries and time periods.
   - **Yearly Trend Analysis by HS Code**: Identifies trade patterns for different commodity categories.

   **For the most recent year:**
   - **Monthly Trade Trends**: Displays fluctuations in trade volume over time.
   - **Month-over-Month Growth Bar Chart**: Highlighting percentage changes in trade volume.
   - **Z-score Analysis for Outliers**: Identifying potential trade anomalies based on standard deviation.

5. **Exported Processed Data**:
   - Provided clean and ready-to-use datasets in CSV format.
   - Output files are suitable for further analysis or integration into Model.Earth.

## **API Features and Constraints**

The **UN Comtrade Public API (v1)** provides multiple free endpoints, including `getComtradeReleases`, `getDA`, `getDATariffline`, `getMBS`, `getMetadata`, `getWorldShare`, `preview`, and `previewTariffline`. However, these APIs have **limitations** such as:
- **Data is only available at the HS code level**, requiring manual aggregation for sector-level insights.
- **Limited coverage**—some endpoints focus on metadata, availability checks, or previews rather than actual trade flows.
- **Restricted data retrieval**—certain APIs provide only a subset of records, making large-scale analysis challenging.
- **Tariff-line data limitations**—only available for select countries and does not allow sector-based aggregation.

Below are the key response fields from the API:

| **Field**             | **Example** | **Description** |
|----------------------|------------|----------------|
| `datasetCode`        | `30008201201092100` | Unique UN Comtrade dataset identifier |
| `typeCode`           | `"C"` | `"C"` = Commodities (Goods), `"S"` = Services |
| `freqCode`           | `"M"` | `"M"` = Monthly data, `"A"` = Annual data |
| `period`             | `201201` | **Trade period (YYYYMM format)** (e.g., `201201` = Jan 2012) |
| `reporterCode`       | `8` | **Country Code of the Reporter** (e.g., `8` = Albania) |
| `reporterISO`        | `"ALB"` | **ISO 3-letter code for the reporter country** (e.g., `ALB` = Albania) |
| `classificationCode` | `"H4"` | **HS Code Classification Level** (`H4` = 4-digit HS Code) |
| `totalRecords`       | `15051` | **Total trade records** for this query |
| `datasetChecksum`    | `-1630968198` | Used for **data integrity verification** (not needed for analysis) |

The **UN Comtrade API** is a powerful tool for commodity-level trade data analysis, but sector-level insights require **manual aggregation of HS codes** into industry categories.

## Next Steps
1. **Incorporate Feedback**: Review and implement suggestions from the **Model.Earth team** to enhance functionality.  
2. **Enhance Analysis Granularity**: Incorporate **sector-level information** to improve the depth of analysis, enabling a more detailed investigation of **trade flows across different countries and industries**.  
3. **Optimize Deployment**: Finalize scripts and notebooks for **cloud deployment**, ensuring seamless **API integration** and scalability.  

## Conclusion
1. The **UN Comtrade API** provides robust trade and tariff data.
2. The delivered **scripts, datasets, and visualizations** enable Model.Earth participants to analyze trade patterns effectively.
3. The solution is **scalable, adaptable, and ready** for further integration into Model.Earth workflows.

## Attachments
- **Jupyter Notebook**: `modelEarth.ipynb`
- **Processed Dataset**: `comtrade-output.csv`
- **Annual Trade Data**: `comtrade-output-last-year.csv`


