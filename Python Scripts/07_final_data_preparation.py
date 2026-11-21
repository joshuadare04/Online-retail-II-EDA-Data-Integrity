import pandas as pd
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Cleaned Data" / "online_retail_II_deduplicated.csv"
OUTPUT_DIR = BASE_DIR / "Cleaned Data"

print("Loading cleaned dataset...")
df = pd.read_csv(INPUT_FILE)

print("\nPreparing analytical dataset...")

# 1. Identify invoice types
df["Invoice"] = df["Invoice"].astype(str)
df["IsCancellation"] = df["Invoice"].str.startswith("C")

# 2. Identify negative quantities
df["IsNegativeQuantity"] = df["Quantity"] < 0

# 3. Identify zero-priced transactions
df["IsZeroPrice"] = df["Price"] == 0

# 4. Identify bad debt adjustments
df["IsBadDebtAdjustment"] = (
    df["Description"].fillna("").str.strip().str.lower()
    == "adjust bad debt"
)

# 5. Calculate transaction value
df["TransactionValue"] = df["Quantity"] * df["Price"]

# 6. Classify transaction records
df["TransactionCategory"] = "Regular Transaction"

df.loc[
    df["IsCancellation"],
    "TransactionCategory"
] = "Cancellation"

df.loc[
    (~df["IsCancellation"]) & df["IsNegativeQuantity"],
    "TransactionCategory"
] = "Negative Quantity Adjustment"

df.loc[
    df["IsBadDebtAdjustment"],
    "TransactionCategory"
] = "Bad Debt Adjustment"

# 7. Create analysis-ready dataset
# Exclude only the five negative-priced bad debt adjustments
analysis_df = df[df["Price"] >= 0].copy()

# 8. Export datasets
df.to_csv(
    OUTPUT_DIR / "online_retail_II_full_enriched.csv",
    index=False
)

analysis_df.to_csv(
    OUTPUT_DIR / "online_retail_II_analysis_ready.csv",
    index=False
)

# 9. Display preparation summary
print("\n" + "=" * 60)
print("FINAL DATA PREPARATION SUMMARY")
print("=" * 60)

print(f"Original Records: {len(df):,}")
print(f"Bad Debt Adjustments Excluded: {len(df) - len(analysis_df):,}")
print(f"Analysis-Ready Records: {len(analysis_df):,}")

print("\nTRANSACTION CLASSIFICATION")
print(df["TransactionCategory"].value_counts().to_string())

print("\nADDITIONAL FLAGS")
print(f"Cancellation Records: {df['IsCancellation'].sum():,}")
print(f"Negative Quantity Records: {df['IsNegativeQuantity'].sum():,}")
print(f"Zero-Priced Records: {df['IsZeroPrice'].sum():,}")

print("\nEXPORTED FILES:")
print("1. online_retail_II_full_enriched.csv")
print("2. online_retail_II_analysis_ready.csv")

print("\nFINAL DATA PREPARATION COMPLETED.")
print("=" * 60)