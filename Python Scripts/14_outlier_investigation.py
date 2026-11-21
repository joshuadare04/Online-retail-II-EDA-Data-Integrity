import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Cleaned Data" / "online_retail_II_analysis_ready.csv"
OUTPUT_DIR = BASE_DIR / "Investigation Results"

OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading analysis-ready dataset...")
df = pd.read_csv(INPUT_FILE)

df["Invoice"] = df["Invoice"].astype(str)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# Identify genuine sales
sales = df[
    (~df["Invoice"].str.startswith("C")) &
    (df["Quantity"] > 0) &
    (df["Price"] >= 0) &
    (df["Description"].fillna("").str.strip().str.lower()
     != "adjust bad debt")
].copy()

sales["Revenue"] = sales["Quantity"] * sales["Price"]

print("\n" + "=" * 65)
print("OUTLIER AND ANOMALY INVESTIGATION")
print("=" * 65)

# --------------------------------------------------
# 1. EXTREME QUANTITY INVESTIGATION
# --------------------------------------------------

q1 = sales["Quantity"].quantile(0.25)
q3 = sales["Quantity"].quantile(0.75)
iqr = q3 - q1
quantity_limit = q3 + (1.5 * iqr)

high_quantity = sales[
    sales["Quantity"] > quantity_limit
].copy()

print("\n1. EXTREME QUANTITY INVESTIGATION")
print(f"Q1: {q1:,.2f}")
print(f"Q3: {q3:,.2f}")
print(f"IQR Upper Limit: {quantity_limit:,.2f}")
print(f"High-Quantity Records: {len(high_quantity):,}")

print("\nTOP 15 TRANSACTIONS BY QUANTITY")
print(
    sales.nlargest(15, "Quantity")[
        ["Invoice", "StockCode", "Description",
         "Quantity", "Price", "Revenue", "InvoiceDate"]
    ].to_string(index=False)
)

# --------------------------------------------------
# 2. HIGH TRANSACTION VALUE INVESTIGATION
# --------------------------------------------------

q1_revenue = sales["Revenue"].quantile(0.25)
q3_revenue = sales["Revenue"].quantile(0.75)
revenue_iqr = q3_revenue - q1_revenue
revenue_limit = q3_revenue + (1.5 * revenue_iqr)

high_value = sales[
    sales["Revenue"] > revenue_limit
].copy()

print("\n2. HIGH TRANSACTION VALUE INVESTIGATION")
print(f"Revenue Q1: {q1_revenue:,.2f}")
print(f"Revenue Q3: {q3_revenue:,.2f}")
print(f"IQR Upper Limit: {revenue_limit:,.2f}")
print(f"High-Value Records: {len(high_value):,}")

print("\nTOP 15 TRANSACTIONS BY REVENUE")
print(
    sales.nlargest(15, "Revenue")[
        ["Invoice", "StockCode", "Description",
         "Quantity", "Price", "Revenue", "InvoiceDate"]
    ].to_string(index=False)
)

# --------------------------------------------------
# 3. UNUSUALLY HIGH UNIT PRICE INVESTIGATION
# --------------------------------------------------

positive_prices = sales[sales["Price"] > 0]["Price"]

price_q1 = positive_prices.quantile(0.25)
price_q3 = positive_prices.quantile(0.75)
price_iqr = price_q3 - price_q1
price_limit = price_q3 + (1.5 * price_iqr)

high_price = sales[
    sales["Price"] > price_limit
].copy()

print("\n3. HIGH UNIT PRICE INVESTIGATION")
print(f"Unit Price Q1: {price_q1:,.2f}")
print(f"Unit Price Q3: {price_q3:,.2f}")
print(f"IQR Upper Limit: {price_limit:,.2f}")
print(f"High-Price Records: {len(high_price):,}")

print("\nTOP 15 RECORDS BY UNIT PRICE")
print(
    sales.nlargest(15, "Price")[
        ["Invoice", "StockCode", "Description",
         "Quantity", "Price", "Revenue", "InvoiceDate"]
    ].to_string(index=False)
)

# --------------------------------------------------
# 4. PRODUCT QUANTITY AND ORDER PATTERNS
# --------------------------------------------------

product_summary = sales.groupby(
    ["StockCode", "Description"], dropna=False
).agg(
    TotalQuantity=("Quantity", "sum"),
    TotalRevenue=("Revenue", "sum"),
    OrderCount=("Invoice", "nunique"),
    AverageUnitPrice=("Price", "mean")
).reset_index()

product_summary["QuantityPerOrder"] = (
    product_summary["TotalQuantity"] /
    product_summary["OrderCount"]
)

print("\n4. PRODUCT QUANTITY AND ORDER PATTERNS")

print("\nTOP 15 PRODUCTS BY QUANTITY SOLD")
print(
    product_summary.nlargest(15, "TotalQuantity").to_string(index=False)
)

print("\nTOP 15 PRODUCTS BY QUANTITY PER ORDER")
print(
    product_summary.nlargest(15, "QuantityPerOrder").to_string(index=False)
)

# --------------------------------------------------
# 5. INVESTIGATE KNOWN UNUSUAL PRODUCT
# --------------------------------------------------

unusual_product = sales[
    sales["StockCode"].astype(str).str.strip() == "23843"
]

print("\n5. INVESTIGATION OF STOCKCODE 23843")
print(f"Transaction Records: {len(unusual_product):,}")
print(f"Unique Invoices: {unusual_product['Invoice'].nunique():,}")
print(f"Total Quantity: {unusual_product['Quantity'].sum():,}")
print(f"Total Revenue: {unusual_product['Revenue'].sum():,.2f}")

if not unusual_product.empty:
    print(
        unusual_product[
            ["Invoice", "StockCode", "Description",
             "Quantity", "Price", "Revenue", "InvoiceDate"]
        ].to_string(index=False)
    )

# --------------------------------------------------
# 6. ZERO-PRICE SALES RECORDS
# --------------------------------------------------

zero_price = sales[sales["Price"] == 0].copy()

print("\n6. ZERO-PRICE SALES RECORDS")
print(f"Zero-Price Records: {len(zero_price):,}")
print(f"Unique StockCodes: {zero_price['StockCode'].nunique():,}")
print(f"Total Quantity: {zero_price['Quantity'].sum():,}")

# --------------------------------------------------
# 7. EXPORT INVESTIGATION RESULTS
# --------------------------------------------------

high_quantity.to_csv(
    OUTPUT_DIR / "high_quantity_transactions.csv",
    index=False
)

high_value.to_csv(
    OUTPUT_DIR / "high_value_transactions.csv",
    index=False
)

high_price.to_csv(
    OUTPUT_DIR / "high_unit_price_transactions.csv",
    index=False
)

product_summary.sort_values(
    "TotalQuantity", ascending=False
).to_csv(
    OUTPUT_DIR / "product_quantity_anomaly_analysis.csv",
    index=False
)

unusual_product.to_csv(
    OUTPUT_DIR / "stockcode_23843_investigation.csv",
    index=False
)

zero_price.to_csv(
    OUTPUT_DIR / "zero_price_sales_records.csv",
    index=False
)

print("\nInvestigation results exported successfully.")
print("\nOUTLIER AND ANOMALY INVESTIGATION COMPLETED.")
print("=" * 65)