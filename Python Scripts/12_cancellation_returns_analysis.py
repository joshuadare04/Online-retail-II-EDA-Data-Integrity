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

df["Revenue"] = df["Quantity"] * df["Price"]

# Separate cancellations and regular transactions
cancellations = df[df["Invoice"].str.startswith("C")].copy()
regular = df[~df["Invoice"].str.startswith("C")].copy()

print("\n" + "=" * 65)
print("CANCELLATION AND RETURNS ANALYSIS")
print("=" * 65)

# --------------------------------------------------
# 1. CANCELLATION OVERVIEW
# --------------------------------------------------

cancelled_invoices = cancellations["Invoice"].nunique()
regular_invoices = regular["Invoice"].nunique()

total_invoices = cancelled_invoices + regular_invoices

cancellation_rate = (
    cancelled_invoices / total_invoices * 100
    if total_invoices else 0
)

print("\n1. CANCELLATION OVERVIEW")
print(f"Cancellation Records: {len(cancellations):,}")
print(f"Unique Cancelled Invoices: {cancelled_invoices:,}")
print(f"Regular Transaction Records: {len(regular):,}")
print(f"Unique Regular Invoices: {regular_invoices:,}")
print(f"Invoice-Based Cancellation Rate: {cancellation_rate:.2f}%")

print(
    f"Negative Quantity Cancellation Records: "
    f"{(cancellations['Quantity'] < 0).sum():,}"
)

print(
    f"Non-Negative Quantity Cancellation Records: "
    f"{(cancellations['Quantity'] >= 0).sum():,}"
)

# --------------------------------------------------
# 2. CANCELLATION VALUE
# --------------------------------------------------

cancellation_value = cancellations["Revenue"].sum()

print("\n2. CANCELLATION VALUE")
print(f"Net Cancellation Transaction Value: {cancellation_value:,.2f}")
print(
    f"Absolute Cancellation Transaction Value: "
    f"{abs(cancellation_value):,.2f}"
)

# --------------------------------------------------
# 3. MONTHLY CANCELLATION TRENDS
# --------------------------------------------------

cancellations["YearMonth"] = (
    cancellations["InvoiceDate"].dt.to_period("M").astype(str)
)

monthly_cancellations = cancellations.groupby("YearMonth").agg(
    CancellationRecords=("Invoice", "size"),
    CancelledInvoices=("Invoice", "nunique"),
    CancellationValue=("Revenue", "sum")
).sort_index()

print("\n3. MONTHLY CANCELLATION TRENDS")
print(monthly_cancellations.to_string())

# --------------------------------------------------
# 4. NEGATIVE QUANTITY ADJUSTMENTS IN REGULAR INVOICES
# --------------------------------------------------

negative_adjustments = regular[
    regular["Quantity"] < 0
].copy()

print("\n4. NEGATIVE QUANTITY ADJUSTMENTS")
print(f"Adjustment Records: {len(negative_adjustments):,}")
print(
    f"Unique Invoices: "
    f"{negative_adjustments['Invoice'].nunique():,}"
)
print(
    f"Unique StockCodes: "
    f"{negative_adjustments['StockCode'].nunique():,}"
)
print(
    f"Total Negative Quantity: "
    f"{negative_adjustments['Quantity'].sum():,}"
)
print(
    f"Total Adjustment Value: "
    f"{negative_adjustments['Revenue'].sum():,.2f}"
)

print("\nTOP 20 ADJUSTMENT DESCRIPTIONS")

adjustment_descriptions = negative_adjustments.groupby(
    "Description", dropna=False
).agg(
    Records=("Invoice", "size"),
    TotalQuantity=("Quantity", "sum"),
    TotalValue=("Revenue", "sum")
).sort_values("Records", ascending=False).head(20)

print(adjustment_descriptions.to_string())

# --------------------------------------------------
# 5. CANCELLATION RECORDS WITH NON-NEGATIVE QUANTITY
# --------------------------------------------------

unusual_cancellations = cancellations[
    cancellations["Quantity"] >= 0
].copy()

print("\n5. UNUSUAL CANCELLATION RECORDS")
print(f"Records Identified: {len(unusual_cancellations):,}")

if not unusual_cancellations.empty:
    print(
        unusual_cancellations[
            ["Invoice", "StockCode", "Description",
             "Quantity", "Price", "InvoiceDate"]
        ].to_string(index=False)
    )

# --------------------------------------------------
# 6. EXPORT INVESTIGATION RESULTS
# --------------------------------------------------

cancellations.to_csv(
    OUTPUT_DIR / "cancellation_records.csv",
    index=False
)

negative_adjustments.to_csv(
    OUTPUT_DIR / "negative_quantity_adjustments.csv",
    index=False
)

monthly_cancellations.to_csv(
    OUTPUT_DIR / "monthly_cancellation_trends.csv"
)

adjustment_descriptions.to_csv(
    OUTPUT_DIR / "adjustment_description_summary.csv"
)

unusual_cancellations.to_csv(
    OUTPUT_DIR / "unusual_cancellation_records.csv",
    index=False
)

print("\nInvestigation results exported successfully.")
print("\nCANCELLATION AND RETURNS ANALYSIS COMPLETED.")
print("=" * 65)