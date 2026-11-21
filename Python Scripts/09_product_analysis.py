import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Cleaned Data" / "online_retail_II_analysis_ready.csv"

print("Loading analysis-ready dataset...")
df = pd.read_csv(INPUT_FILE)

# Identify genuine sales
df["Invoice"] = df["Invoice"].astype(str)

sales = df[
    (~df["Invoice"].str.startswith("C")) &
    (df["Quantity"] > 0) &
    (df["Price"] >= 0) &
    (df["Description"].fillna("").str.strip().str.lower()
     != "adjust bad debt")
].copy()

# Calculate revenue
sales["Revenue"] = sales["Quantity"] * sales["Price"]

print("\n" + "=" * 60)
print("PRODUCT PERFORMANCE ANALYSIS")
print("=" * 60)

# 1. Product overview
print("\n1. PRODUCT OVERVIEW")
print(f"Unique Products: {sales['StockCode'].nunique():,}")
print(f"Total Units Sold: {sales['Quantity'].sum():,}")
print(f"Total Product Revenue: {sales['Revenue'].sum():,.2f}")

# 2. Top products by revenue
print("\n2. TOP 15 PRODUCTS BY REVENUE")

product_revenue = sales.groupby(
    ["StockCode", "Description"]
).agg(
    Revenue=("Revenue", "sum"),
    QuantitySold=("Quantity", "sum"),
    Orders=("Invoice", "nunique")
).sort_values("Revenue", ascending=False)

print(product_revenue.head(15).to_string())

# 3. Top products by quantity
print("\n3. TOP 15 PRODUCTS BY QUANTITY SOLD")

product_quantity = product_revenue.sort_values(
    "QuantitySold", ascending=False
)

print(product_quantity.head(15).to_string())

# 4. Top products by number of orders
print("\n4. TOP 15 PRODUCTS BY ORDER FREQUENCY")

product_orders = product_revenue.sort_values(
    "Orders", ascending=False
)

print(product_orders.head(15).to_string())

# 5. Product revenue concentration
total_revenue = sales["Revenue"].sum()

top_10_revenue = product_revenue.head(10)["Revenue"].sum()

print("\n5. REVENUE CONCENTRATION")
print(f"Top 10 Products Revenue: {top_10_revenue:,.2f}")
print(f"Top 10 Products Revenue Share: "
      f"{(top_10_revenue / total_revenue) * 100:.2f}%")

# 6. Export results
OUTPUT_DIR = BASE_DIR / "Investigation Results"
OUTPUT_DIR.mkdir(exist_ok=True)

product_revenue.to_csv(
    OUTPUT_DIR / "product_performance.csv"
)

print("\nProduct performance results exported.")
print("\nPRODUCT ANALYSIS COMPLETED.")
print("=" * 60)