# ============================================================
# PROGREE DATA ANALYTICS INTERNSHIP
# TASK 2: EDA AND DATA INTEGRITY
# STEP 5: CROSS-WORKSHEET VALIDATION
# ============================================================

import pandas as pd
from pathlib import Path

data_path = (
    Path(__file__).resolve().parent.parent
    / "Source Data"
    / "online+retail+ii"
    / "online_retail_II.xlsx"
)

# Load both worksheets
df_1 = pd.read_excel(
    data_path,
    sheet_name="Year 2009-2010"
)

df_2 = pd.read_excel(
    data_path,
    sheet_name="Year 2010-2011"
)

# Combine worksheets for comparison
combined_df = pd.concat(
    [df_1, df_2],
    ignore_index=True
)

print("=" * 65)
print("CROSS-WORKSHEET DATA VALIDATION")
print("=" * 65)

# 1. Dataset dimensions
print("\n1. COMBINED DATASET OVERVIEW")

print(f"Worksheet 1 Records: {len(df_1):,}")
print(f"Worksheet 2 Records: {len(df_2):,}")
print(f"Combined Records: {len(combined_df):,}")

# 2. Date overlap
print("\n2. DATE RANGE COMPARISON")

print(f"Worksheet 1: {df_1['InvoiceDate'].min()} "
      f"to {df_1['InvoiceDate'].max()}")

print(f"Worksheet 2: {df_2['InvoiceDate'].min()} "
      f"to {df_2['InvoiceDate'].max()}")

overlap = combined_df[
    (combined_df["InvoiceDate"] >= df_2["InvoiceDate"].min()) &
    (combined_df["InvoiceDate"] <= df_1["InvoiceDate"].max())
]

print(f"Records within overlapping date period: {len(overlap):,}")

# 3. Cross-worksheet exact duplicates
print("\n3. CROSS-WORKSHEET DUPLICATE CHECK")

duplicates = combined_df[
    combined_df.duplicated(keep=False)
]

print(f"Combined Exact Duplicate Records: "
      f"{combined_df.duplicated().sum():,}")

print(f"Records Involved in Duplicates: {len(duplicates):,}")

# 4. Records shared by both worksheets
print("\n4. RECORDS SHARED BETWEEN WORKSHEETS")

shared_records = pd.merge(
    df_1,
    df_2,
    how="inner"
)

print(f"Exact Records Appearing in Both Worksheets: "
      f"{len(shared_records):,}")

# 5. Combined data quality summary
print("\n5. COMBINED DATA QUALITY SUMMARY")

print("\nMissing Values:")
print(combined_df.isnull().sum())

print(f"\nTotal Missing Customer IDs: "
      f"{combined_df['Customer ID'].isna().sum():,}")

print(f"Total Missing Descriptions: "
      f"{combined_df['Description'].isna().sum():,}")

print("\nCROSS-WORKSHEET VALIDATION COMPLETED.")