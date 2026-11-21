import pandas as pd
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "Cleaned Data" / "online_retail_II_deduplicated.csv"

print("Loading cleaned dataset...")
df = pd.read_csv(INPUT_FILE)

print("\n" + "=" * 60)
print("DATA QUALITY VALIDATION REPORT")
print("=" * 60)

# 1. Dataset overview
print("\n1. DATASET OVERVIEW")
print(f"Total Records: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")

# 2. Missing values
print("\n2. MISSING VALUES")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "No missing values")

# 3. Unit Price validation
print("\n3. UNIT PRICE VALIDATION")
print(f"Zero Unit Prices: {(df['Price'] == 0).sum():,}")
print(f"Negative Unit Prices: {(df['Price'] < 0).sum():,}")

# 4. Quantity validation
print("\n4. QUANTITY VALIDATION")
print(f"Negative Quantities: {(df['Quantity'] < 0).sum():,}")
print(f"Zero Quantities: {(df['Quantity'] == 0).sum():,}")

# 5. Date validation
print("\n5. DATE VALIDATION")
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
print(f"Invalid Invoice Dates: {df['InvoiceDate'].isna().sum():,}")

# 6. Customer ID validation
print("\n6. CUSTOMER ID VALIDATION")
print(f"Missing Customer IDs: {df['Customer ID'].isna().sum():,}")

# 7. StockCode validation
print("\n7. STOCKCODE VALIDATION")
print(f"Missing StockCodes: {df['StockCode'].isna().sum():,}")

# 8. Final duplicate check
print("\n8. DUPLICATE VALIDATION")
print(f"Duplicate Records: {df.duplicated().sum():,}")

print("\n" + "=" * 60)
print("DATA QUALITY VALIDATION COMPLETED")
print("=" * 60)