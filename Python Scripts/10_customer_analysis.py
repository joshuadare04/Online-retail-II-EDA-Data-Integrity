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

# Exclude records without Customer ID for customer-level analysis
customer_sales = sales.dropna(subset=["Customer ID"]).copy()

print("\n" + "=" * 60)
print("CUSTOMER PURCHASING ANALYSIS")
print("=" * 60)

# 1. Customer overview
print("\n1. CUSTOMER OVERVIEW")
print(f"Identifiable Customers: {customer_sales['Customer ID'].nunique():,}")
print(f"Transactions: {len(customer_sales):,}")
print(f"Customer Revenue: {customer_sales['Revenue'].sum():,.2f}")

# 2. Customer spending
customer_summary = customer_sales.groupby("Customer ID").agg(
    TotalRevenue=("Revenue", "sum"),
    TotalOrders=("Invoice", "nunique"),
    TotalQuantity=("Quantity", "sum")
).sort_values("TotalRevenue", ascending=False)

print("\n2. TOP 15 CUSTOMERS BY REVENUE")
print(customer_summary.head(15).to_string())

# 3. Customer order frequency
print("\n3. TOP 15 CUSTOMERS BY ORDER FREQUENCY")
print(
    customer_summary.sort_values(
        "TotalOrders", ascending=False
    ).head(15).to_string()
)

# 4. Customer spending distribution
print("\n4. CUSTOMER SPENDING DISTRIBUTION")
print(customer_summary["TotalRevenue"].describe().to_string())

# 5. Revenue concentration
total_revenue = customer_summary["TotalRevenue"].sum()

top_10_revenue = customer_summary.head(10)["TotalRevenue"].sum()

print("\n5. CUSTOMER REVENUE CONCENTRATION")
print(f"Top 10 Customer Revenue: {top_10_revenue:,.2f}")
print(f"Top 10 Customer Revenue Share: "
      f"{top_10_revenue / total_revenue * 100:.2f}%")

# 6. Customer export
OUTPUT_DIR = BASE_DIR / "Investigation Results"
OUTPUT_DIR.mkdir(exist_ok=True)

customer_summary.to_csv(
    OUTPUT_DIR / "customer_performance.csv"
)

print("\nCustomer analysis exported successfully.")
print("\nCUSTOMER ANALYSIS COMPLETED.")
print("=" * 60)