import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Cleaned Data" / "online_retail_II_analysis_ready.csv"

print("Loading analysis-ready dataset...")
df = pd.read_csv(INPUT_FILE)

df["Invoice"] = df["Invoice"].astype(str)

# Identify genuine sales
sales = df[
    (~df["Invoice"].str.startswith("C")) &
    (df["Quantity"] > 0) &
    (df["Price"] >= 0) &
    (df["Description"].fillna("").str.strip().str.lower()
     != "adjust bad debt")
].copy()

sales["Revenue"] = sales["Quantity"] * sales["Price"]

print("\n" + "=" * 60)
print("GEOGRAPHICAL SALES ANALYSIS")
print("=" * 60)

# 1. Country performance
country_summary = sales.groupby("Country").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Invoice", "nunique"),
    QuantitySold=("Quantity", "sum"),
    Customers=("Customer ID", "nunique")
).sort_values("Revenue", ascending=False)

print("\n1. COUNTRY PERFORMANCE")
print(f"Total Countries: {sales['Country'].nunique()}")
print(country_summary.to_string())

# 2. Top 10 countries by revenue
print("\n2. TOP 10 COUNTRIES BY REVENUE")
print(country_summary.head(10).to_string())

# 3. Top 10 countries by order volume
print("\n3. TOP 10 COUNTRIES BY ORDER VOLUME")
print(
    country_summary.sort_values(
        "Orders", ascending=False
    ).head(10).to_string()
)

# 4. Revenue concentration
total_revenue = sales["Revenue"].sum()

uk_revenue = country_summary.loc["United Kingdom", "Revenue"]

top_5_revenue = country_summary.head(5)["Revenue"].sum()

print("\n4. GEOGRAPHICAL REVENUE CONCENTRATION")
print(f"Total Revenue: {total_revenue:,.2f}")
print(f"UK Revenue Share: {uk_revenue / total_revenue * 100:.2f}%")
print(f"Top 5 Countries Revenue Share: "
      f"{top_5_revenue / total_revenue * 100:.2f}%")

# 5. Export results
OUTPUT_DIR = BASE_DIR / "Investigation Results"
OUTPUT_DIR.mkdir(exist_ok=True)

country_summary.to_csv(
    OUTPUT_DIR / "geographical_performance.csv"
)

print("\nGeographical analysis exported successfully.")
print("\nGEOGRAPHICAL ANALYSIS COMPLETED.")
print("=" * 60)