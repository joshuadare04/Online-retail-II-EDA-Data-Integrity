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

# Filter genuine sales
sales = df[
    (~df["Invoice"].str.startswith("C")) &
    (df["Quantity"] > 0) &
    (df["Price"] >= 0) &
    (df["Description"].fillna("").str.strip().str.lower()
     != "adjust bad debt")
].copy()

sales["Revenue"] = sales["Quantity"] * sales["Price"]

# Extract time components
sales["Year"] = sales["InvoiceDate"].dt.year
sales["Month"] = sales["InvoiceDate"].dt.month
sales["YearMonth"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
sales["DayOfWeek"] = sales["InvoiceDate"].dt.day_name()
sales["Hour"] = sales["InvoiceDate"].dt.hour
sales["Date"] = sales["InvoiceDate"].dt.date

print("\n" + "=" * 65)
print("TIME-BASED SALES ANALYSIS")
print("=" * 65)

# --------------------------------------------------
# 1. YEARLY SALES PERFORMANCE
# --------------------------------------------------

yearly = sales.groupby("Year").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Invoice", "nunique"),
    QuantitySold=("Quantity", "sum")
).sort_index()

print("\n1. YEARLY SALES PERFORMANCE")
print(yearly.to_string())

# --------------------------------------------------
# 2. MONTHLY SALES PERFORMANCE
# --------------------------------------------------

monthly = sales.groupby("YearMonth").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Invoice", "nunique"),
    QuantitySold=("Quantity", "sum")
).sort_index()

print("\n2. MONTHLY SALES PERFORMANCE")
print(monthly.to_string())

print("\nTOP 5 MONTHS BY REVENUE")
print(monthly.sort_values("Revenue", ascending=False).head(5).to_string())

# --------------------------------------------------
# 3. DAY-OF-WEEK PERFORMANCE
# --------------------------------------------------

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

weekday = sales.groupby("DayOfWeek").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Invoice", "nunique"),
    QuantitySold=("Quantity", "sum")
).reindex(day_order)

print("\n3. DAY-OF-WEEK PERFORMANCE")
print(weekday.to_string())

# --------------------------------------------------
# 4. HOURLY SALES PERFORMANCE
# --------------------------------------------------

hourly = sales.groupby("Hour").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Invoice", "nunique"),
    QuantitySold=("Quantity", "sum")
).sort_index()

print("\n4. HOURLY SALES PERFORMANCE")
print(hourly.to_string())

print("\nTOP 5 HOURS BY REVENUE")
print(hourly.sort_values("Revenue", ascending=False).head(5).to_string())

# --------------------------------------------------
# 5. DAILY SALES PERFORMANCE
# --------------------------------------------------

daily = sales.groupby("Date").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Invoice", "nunique"),
    QuantitySold=("Quantity", "sum")
).sort_index()

print("\n5. DAILY SALES SUMMARY")
print(f"Trading Days: {len(daily):,}")
print(f"Average Daily Revenue: {daily['Revenue'].mean():,.2f}")
print(f"Highest Daily Revenue: {daily['Revenue'].max():,.2f}")
print(f"Lowest Daily Revenue: {daily['Revenue'].min():,.2f}")

print("\nTOP 10 DAYS BY REVENUE")
print(daily.sort_values("Revenue", ascending=False).head(10).to_string())

# --------------------------------------------------
# 6. EXPORT RESULTS
# --------------------------------------------------

yearly.to_csv(OUTPUT_DIR / "yearly_sales_performance.csv")
monthly.to_csv(OUTPUT_DIR / "monthly_sales_performance.csv")
weekday.to_csv(OUTPUT_DIR / "weekday_sales_performance.csv")
hourly.to_csv(OUTPUT_DIR / "hourly_sales_performance.csv")
daily.to_csv(OUTPUT_DIR / "daily_sales_performance.csv")

print("\nTime-based analysis exported successfully.")
print("\nTIME-BASED SALES ANALYSIS COMPLETED.")
print("=" * 65)
