# Online Retail II – Exploratory Data Analysis and Data Integrity Assessment

## Project Overview

This project focuses on Exploratory Data Analysis (EDA), data cleaning, and data integrity assessment using the Online Retail II dataset.

The objective was to investigate the structure and quality of the dataset, identify inconsistencies and anomalies, clean and prepare the data, and uncover meaningful business insights through Python-based analysis.

The project was completed as part of the **Progree Data Analytics Internship Programme – Task 2: EDA and Data Integrity**.

## Project Objectives

- Inspect and understand the structure of the dataset.
- Identify and remove duplicate records.
- Investigate missing values and data inconsistencies.
- Examine negative quantities, zero prices, and negative prices.
- Investigate cancellations, returns, and adjustment records.
- Validate transaction dates and identify unusual records.
- Perform exploratory analysis across products, customers, countries, and time.
- Prepare a reliable dataset for further analysis.

## Dataset Description

The Online Retail II dataset contains historical transactional records from a UK-based online retailer.

It originally consists of two worksheets:

- Year 2009–2010
- Year 2010–2011

**Combined original records:** 1,067,371

The dataset contains fields such as:

- Invoice
- StockCode
- Description
- Quantity
- InvoiceDate
- Price
- Customer ID
- Country

**Note:** The original Excel dataset is not included in this repository. Users should obtain the dataset separately and place it in the appropriate location before running the scripts.

## Tools and Technologies

- Python
- Pandas
- NumPy
- Visual Studio Code

## Project Workflow

The project followed a structured data analysis workflow:

1. **Dataset Profiling:** Examined the original worksheets, dimensions, columns, missing values, and duplicate records.
2. **Data Cleaning:** Combined the worksheets, removed duplicate records, and recovered missing product descriptions where possible.
3. **Data Quality Assessment:** Investigated missing values, negative quantities, zero prices, negative prices, and other inconsistencies.
4. **Data Integrity Investigation:** Examined cancellations, adjustments, unusual transactions, and date consistency.
5. **Data Preparation:** Created enriched and analysis-ready datasets.
6. **Exploratory Data Analysis:** Investigated overall sales, product performance, customer behaviour, geographical distribution, and sales trends.
7. **Outlier Investigation:** Applied the Interquartile Range (IQR) method to identify unusual quantities, unit prices, and transaction values.
8. **Final Validation:** Conducted a final assessment of the cleaned and analysis-ready data.

## Key Data Quality Findings

| Data Quality Check | Finding |
|---|---:|
| Original combined records | 1,067,371 |
| Duplicate records removed | 34,335 |
| Deduplicated records | 1,033,036 |
| Missing product descriptions remaining | 1,301 |
| Missing Customer IDs | 235,151 |
| Zero-price records | 6,014 |
| Negative-price records | 5 |
| Negative-quantity records | 22,496 |
| Invalid transaction dates | 0 |
| Analysis-ready records | 1,033,031 |

Not every unusual record was automatically removed. Records such as cancellations, negative quantities, and zero-price transactions were investigated to understand their possible business meaning.

## Key Business Insights

- Total sales revenue from the defined sales records was approximately **20.47 million**.
- The analysis identified **5,881 customers** with identifiable customer IDs.
- The dataset contained **4,984 unique products**.
- The United Kingdom contributed approximately **85.02%** of total sales revenue.
- November 2011 recorded the highest monthly revenue, at approximately **1.50 million**.
- A small group of high-value customers contributed a significant share of identifiable customer revenue.
- Several unusually high-quantity transactions were identified and flagged for further investigation rather than automatically removed.

## Repository Structure

```text
Task 2 - Data Integrity/
│
├── Python Scripts/
│   ├── 01_dataset_profiling.py
│   ├── 02_data_cleaning.py
│   ├── 03_data_quality_validation.py
│   ├── ...
│   └── 16_date_validation.py
│
├── Cleaned Data/
│   ├── online_retail_II_deduplicated.csv
│   ├── online_retail_II_full_enriched.csv
│   └── online_retail_II_analysis_ready.csv
│
├── Investigation Results/
│   └── Generated investigation and analysis outputs
│
├── Final Documentation/
│   └── Online_Retail_II_EDA_and_Data_Integrity_Report.docx
│
└── README.md
```

## How to Run the Project

1. Obtain the Online Retail II dataset separately.
2. Place the original Excel workbook in the project directory or update the input file path in the relevant Python scripts.
3. Install the required libraries:

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

4. Run the Python scripts in numerical order from the `Python Scripts` folder.
5. Review the generated datasets in `Cleaned Data` and the investigation outputs in `Investigation Results`.

**Important:** Some scripts depend on files generated by earlier scripts. Run them in sequence and ensure the input and output paths are correctly configured.

## Documentation

The `Final Documentation` folder contains the detailed project report, covering the methodology, data cleaning process, integrity investigations, exploratory analysis, key findings, recommendations, and conclusion.

## Conclusion

This project demonstrates a structured approach to data profiling, cleaning, validation, integrity assessment, and exploratory data analysis.

Beyond identifying data quality issues, the investigation focused on understanding the context behind unusual records and preserving meaningful business information.

The resulting analysis-ready dataset provides a more reliable foundation for further business intelligence and analytical work.

---

**Project:** Progree Data Analytics Internship – Task 2  
**Focus:** Exploratory Data Analysis and Data Integrity  
**Tools:** Python, Pandas, NumPy, Visual Studio Code
