import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Cleaned Data" / "online_retail_II_deduplicated.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("ANOMALY INVESTIGATION")
print("=" * 60)

# Zero-priced transactions
zero_price = df[df["Price"] == 0]

print("\n1. ZERO-PRICED TRANSACTIONS")
print(f"Total Records: {len(zero_price):,}")
print(f"Unique StockCodes: {zero_price['StockCode'].nunique():,}")
print("\nTop 10 StockCodes:")
print(zero_price["StockCode"].value_counts().head(10))

# Negative-priced transactions
negative_price = df[df["Price"] < 0]

print("\n2. NEGATIVE-PRICED TRANSACTIONS")
print(f"Total Records: {len(negative_price):,}")
print(negative_price[["Invoice", "StockCode", "Description",
                      "Quantity", "Price"]].to_string(index=False))

# Negative quantities
negative_quantity = df[df["Quantity"] < 0]

print("\n3. NEGATIVE QUANTITY INVESTIGATION")
print(f"Total Records: {len(negative_quantity):,}")
print(f"Associated Invoice Records: {negative_quantity['Invoice'].nunique():,}")

# Save investigation results
output_dir = BASE_DIR / "Investigation Results"
output_dir.mkdir(exist_ok=True)

zero_price.to_csv(output_dir / "zero_price_records.csv", index=False)
negative_price.to_csv(output_dir / "negative_price_records.csv", index=False)
negative_quantity.to_csv(output_dir / "negative_quantity_records.csv", index=False)

print("\nInvestigation records exported successfully.")
print("=" * 60)