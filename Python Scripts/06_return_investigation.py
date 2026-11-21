import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Cleaned Data" / "online_retail_II_deduplicated.csv"

df = pd.read_csv(INPUT_FILE)

df["Invoice"] = df["Invoice"].astype(str)

# Negative quantities in regular invoices
regular_returns = df[
    (~df["Invoice"].str.startswith("C")) &
    (df["Quantity"] < 0)
]

# Cancellation records with non-negative quantities
other_cancellations = df[
    (df["Invoice"].str.startswith("C")) &
    (df["Quantity"] >= 0)
]

print("=" * 60)
print("RETURN AND EXCEPTION INVESTIGATION")
print("=" * 60)

print("\n1. NEGATIVE QUANTITIES IN REGULAR INVOICES")
print(f"Records: {len(regular_returns):,}")
print(f"Unique Invoices: {regular_returns['Invoice'].nunique():,}")
print(f"Unique StockCodes: {regular_returns['StockCode'].nunique():,}")

print("\nSample Records:")
print(regular_returns[
    ["Invoice", "StockCode", "Description", "Quantity", "Price"]
].head(15).to_string(index=False))

print("\n2. NON-NEGATIVE CANCELLATION RECORDS")
print(f"Records: {len(other_cancellations):,}")

print(other_cancellations[
    ["Invoice", "StockCode", "Description", "Quantity", "Price"]
].to_string(index=False))

print("\nINVESTIGATION COMPLETED")
print("=" * 60)