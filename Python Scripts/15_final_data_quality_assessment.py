import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_FILE = (
    BASE_DIR / "Cleaned Data" /
    "online_retail_II_deduplicated.csv"
)

ANALYSIS_FILE = (
    BASE_DIR / "Cleaned Data" /
    "online_retail_II_analysis_ready.csv"
)

OUTPUT_DIR = BASE_DIR / "Investigation Results"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading datasets...")

source = pd.read_csv(SOURCE_FILE)
analysis = pd.read_csv(ANALYSIS_FILE)

source["Invoice"] = source["Invoice"].astype(str)

source["InvoiceDate"] = pd.to_datetime(
    source["InvoiceDate"], errors="coerce"
)

analysis["Invoice"] = analysis["Invoice"].astype(str)

analysis["InvoiceDate"] = pd.to_datetime(
    analysis["InvoiceDate"], errors="coerce"
)

print("\n" + "=" * 65)
print("FINAL DATA QUALITY ASSESSMENT")
print("=" * 65)

# --------------------------------------------------
# 1. DATASET STRUCTURE
# --------------------------------------------------

print("\n1. DATASET STRUCTURE")

print(f"Deduplicated Dataset Records: {len(source):,}")
print(f"Analysis-Ready Dataset Records: {len(analysis):,}")
print(f"Columns: {len(source.columns)}")

print("\nColumn Data Types:")
print(source.dtypes.to_string())

# --------------------------------------------------
# 2. MISSING VALUE ASSESSMENT
# --------------------------------------------------

print("\n2. MISSING VALUE ASSESSMENT")

missing_summary = pd.DataFrame({
    "MissingValues": source.isnull().sum(),
    "MissingPercentage": (
        source.isnull().mean() * 100
    ).round(2)
})

print(missing_summary.to_string())

# --------------------------------------------------
# 3. DUPLICATE ASSESSMENT
# --------------------------------------------------

print("\n3. DUPLICATE ASSESSMENT")

duplicate_count = source.duplicated().sum()

print(f"Duplicate Records: {duplicate_count:,}")

# --------------------------------------------------
# 4. PRICE AND QUANTITY VALIDATION
# --------------------------------------------------

print("\n4. PRICE AND QUANTITY VALIDATION")

print(f"Zero Unit Prices: {(source['Price'] == 0).sum():,}")
print(f"Negative Unit Prices: {(source['Price'] < 0).sum():,}")
print(f"Negative Quantities: {(source['Quantity'] < 0).sum():,}")
print(f"Zero Quantities: {(source['Quantity'] == 0).sum():,}")

# --------------------------------------------------
# 5. TRANSACTION AND DESCRIPTION VALIDATION
# --------------------------------------------------

print("\n5. TRANSACTION AND DESCRIPTION VALIDATION")

cancellation_records = source[
    source["Invoice"].str.startswith("C")
]

regular_records = source[
    ~source["Invoice"].str.startswith("C")
]

print(f"Cancellation Records: {len(cancellation_records):,}")
print(f"Regular Transaction Records: {len(regular_records):,}")

print(
    f"Missing StockCodes: "
    f"{source['StockCode'].isnull().sum():,}"
)

print(
    f"Missing Descriptions: "
    f"{source['Description'].isnull().sum():,}"
)

print(
    f"Bad Debt Description Records: "
    f"{source['Description'].fillna('').str.strip().str.lower().eq('adjust bad debt').sum():,}"
)

# --------------------------------------------------
# 6. DATE VALIDATION
# --------------------------------------------------

print("\n6. DATE VALIDATION")

invalid_dates = source["InvoiceDate"].isnull().sum()

print(f"Invalid Invoice Dates: {invalid_dates:,}")

print(f"Earliest Transaction: {source['InvoiceDate'].min()}")
print(f"Latest Transaction: {source['InvoiceDate'].max()}")

# --------------------------------------------------
# 7. SALES DATA QUALITY
# --------------------------------------------------

sales = analysis[
    (~analysis["Invoice"].str.startswith("C")) &
    (analysis["Quantity"] > 0) &
    (analysis["Price"] >= 0) &
    (
        analysis["Description"].fillna("")
        .str.strip().str.lower() != "adjust bad debt"
    )
].copy()

sales["Revenue"] = sales["Quantity"] * sales["Price"]

print("\n7. SALES DATA QUALITY")

print(f"Analysis-Ready Records: {len(analysis):,}")
print(f"Valid Sales Records: {len(sales):,}")

print(
    f"Zero-Price Sales Records: "
    f"{(sales['Price'] == 0).sum():,}"
)

print(
    f"Sales Records Missing Customer ID: "
    f"{sales['Customer ID'].isnull().sum():,}"
)

print(
    f"Sales Records Missing Description: "
    f"{sales['Description'].isnull().sum():,}"
)

print(f"Total Sales Revenue: {sales['Revenue'].sum():,.2f}")

# --------------------------------------------------
# 8. OUTLIER SUMMARY
# --------------------------------------------------

print("\n8. STATISTICAL OUTLIER SUMMARY")

quantity_q1 = sales["Quantity"].quantile(0.25)
quantity_q3 = sales["Quantity"].quantile(0.75)
quantity_iqr = quantity_q3 - quantity_q1
quantity_limit = quantity_q3 + (1.5 * quantity_iqr)

revenue_q1 = sales["Revenue"].quantile(0.25)
revenue_q3 = sales["Revenue"].quantile(0.75)
revenue_iqr = revenue_q3 - revenue_q1
revenue_limit = revenue_q3 + (1.5 * revenue_iqr)

positive_prices = sales.loc[sales["Price"] > 0, "Price"]

price_q1 = positive_prices.quantile(0.25)
price_q3 = positive_prices.quantile(0.75)
price_iqr = price_q3 - price_q1
price_limit = price_q3 + (1.5 * price_iqr)

print(
    f"High-Quantity Records: "
    f"{(sales['Quantity'] > quantity_limit).sum():,}"
)

print(
    f"High-Value Records: "
    f"{(sales['Revenue'] > revenue_limit).sum():,}"
)

print(
    f"High-Unit-Price Records: "
    f"{(sales['Price'] > price_limit).sum():,}"
)

# --------------------------------------------------
# 9. DATA QUALITY SUMMARY
# --------------------------------------------------

quality_summary = pd.DataFrame([
    ["Deduplicated Records", len(source)],
    ["Analysis-Ready Records", len(analysis)],
    ["Duplicate Records", duplicate_count],
    ["Missing Descriptions", source["Description"].isnull().sum()],
    ["Missing Customer IDs", source["Customer ID"].isnull().sum()],
    ["Missing StockCodes", source["StockCode"].isnull().sum()],
    ["Invalid Invoice Dates", invalid_dates],
    ["Zero Unit Prices", (source["Price"] == 0).sum()],
    ["Negative Unit Prices", (source["Price"] < 0).sum()],
    ["Negative Quantities", (source["Quantity"] < 0).sum()],
    ["Zero Quantities", (source["Quantity"] == 0).sum()],
    ["Cancellation Records", len(cancellation_records)],
    ["Valid Sales Records", len(sales)],
    ["Zero-Price Sales Records", (sales["Price"] == 0).sum()],
    ["High-Quantity Outliers", (sales["Quantity"] > quantity_limit).sum()],
    ["High-Value Outliers", (sales["Revenue"] > revenue_limit).sum()],
    ["High-Unit-Price Outliers", (sales["Price"] > price_limit).sum()]
], columns=["QualityMetric", "Value"])

quality_summary.to_csv(
    OUTPUT_DIR / "final_data_quality_summary.csv",
    index=False
)

missing_summary.to_csv(
    OUTPUT_DIR / "final_missing_value_assessment.csv"
)

print("\n9. FINAL QUALITY SUMMARY")
print(quality_summary.to_string(index=False))

print("\nAssessment results exported successfully.")
print("\nFINAL DATA QUALITY ASSESSMENT COMPLETED.")
print("=" * 65)