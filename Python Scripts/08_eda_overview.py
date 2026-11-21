import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Cleaned Data" / "online_retail_II_analysis_ready.csv"

print("Loading analysis-ready dataset...")
df = pd.read_csv(INPUT_FILE)

df["Invoice"] = df["Invoice"].astype(str)
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], dayfirst=True, errors="coerce"
)

# Calculate transaction value
df["Revenue"] = df["Quantity"] * df["Price"]

# Identify genuine sales transactions
sales = df[
    (~df["Invoice"].str.startswith("C")) &
    (df["Quantity"] > 0) &
    (df["Price"] >= 0) &
    (df["Description"].fillna("").str.strip().str.lower()
     != "adjust bad debt")
].copy()

print("\n" + "=" * 60)
print("EXPLORATORY DATA ANALYSIS - OVERVIEW")
print("=" * 60)

# Dataset overview
print("\n1. DATASET OVERVIEW")
print(f"Total Records: {len(df):,}")
print(f"Sales Records: {len(sales):,}")
print(f"Unique Invoices: {sales['Invoice'].nunique():,}")
print(f"Unique Customers: {sales['Customer ID'].nunique():,}")
print(f"Unique Products: {sales['StockCode'].nunique():,}")
print(f"Countries: {sales['Country'].nunique():,}")

# Sales performance
print("\n2. OVERALL SALES PERFORMANCE")
print(f"Total Revenue: {sales['Revenue'].sum():,.2f}")
print(f"Total Quantity Sold: {sales['Quantity'].sum():,}")
print(f"Average Order Value: "
      f"{sales.groupby('Invoice')['Revenue'].sum().mean():,.2f}")

# Date range
print("\n3. TRANSACTION PERIOD")
print(f"First Transaction: {sales['InvoiceDate'].min()}")
print(f"Last Transaction: {sales['InvoiceDate'].max()}")

# Monthly revenue
sales["YearMonth"] = sales["InvoiceDate"].dt.to_period("M")

monthly_sales = sales.groupby("YearMonth").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Invoice", "nunique"),
    Quantity=("Quantity", "sum")
)

print("\n4. MONTHLY SALES PERFORMANCE")
print(monthly_sales.to_string())

# Top countries
print("\n5. TOP 10 COUNTRIES BY REVENUE")

country_sales = sales.groupby("Country").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Invoice", "nunique"),
    Quantity=("Quantity", "sum")
).sort_values("Revenue", ascending=False)

print(country_sales.head(10).to_string())

print("\n" + "=" * 60)
print("INITIAL EDA COMPLETED")
print("=" * 60)