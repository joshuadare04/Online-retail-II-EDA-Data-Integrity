import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Cleaned Data" / "online_retail_II_deduplicated.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("CANCELLATION ANALYSIS")
print("=" * 60)

# Identify cancelled invoices
df["Invoice"] = df["Invoice"].astype(str)

cancelled = df[df["Invoice"].str.startswith("C", na=False)]
regular = df[~df["Invoice"].str.startswith("C", na=False)]

print(f"\nTotal Records: {len(df):,}")
print(f"Cancellation Records: {len(cancelled):,}")
print(f"Regular Invoice Records: {len(regular):,}")

print(f"\nUnique Cancelled Invoices: {cancelled['Invoice'].nunique():,}")
print(f"Unique Regular Invoices: {regular['Invoice'].nunique():,}")

print("\nQUANTITY ANALYSIS")
print(f"Negative Quantities in Cancellation Records: {(cancelled['Quantity'] < 0).sum():,}")
print(f"Negative Quantities in Regular Records: {(regular['Quantity'] < 0).sum():,}")

print("\nVALUE ANALYSIS")
cancelled["TransactionValue"] = cancelled["Quantity"] * cancelled["Price"]

print(f"Cancellation Transaction Value: {cancelled['TransactionValue'].sum():,.2f}")

print("\nTOP 10 CANCELLATION STOCKCODES")
print(cancelled["StockCode"].value_counts().head(10))

print("\nCANCELLATION ANALYSIS COMPLETED")
print("=" * 60)