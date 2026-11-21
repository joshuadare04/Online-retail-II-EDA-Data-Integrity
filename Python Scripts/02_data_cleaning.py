# ============================================================
# PROGREE DATA ANALYTICS INTERNSHIP
# TASK 2: EDA AND DATA INTEGRITY
# DATA CLEANING PIPELINE
# STEP 6.1: COMBINE WORKSHEETS AND REMOVE EXACT DUPLICATES
# STEP 6.2: HANDLE MISSING DESCRIPTIONS
# ============================================================

import pandas as pd
from pathlib import Path

# ============================================================
# 1. FILE PATHS
# ============================================================

base_path = Path(__file__).resolve().parent.parent

data_path = (
    base_path
    / "Source Data"
    / "online+retail+ii"
    / "online_retail_II.xlsx"
)

output_path = (
    base_path
    / "Cleaned Data"
    / "online_retail_II_deduplicated.csv"
)

# ============================================================
# 2. LOAD AND COMBINE WORKSHEETS
# ============================================================

print("Loading worksheets...")

df_1 = pd.read_excel(
    data_path,
    sheet_name="Year 2009-2010"
)

df_2 = pd.read_excel(
    data_path,
    sheet_name="Year 2010-2011"
)

print("Combining datasets...")

combined_df = pd.concat(
    [df_1, df_2],
    ignore_index=True
)

original_records = len(combined_df)

# ============================================================
# 3. REMOVE EXACT DUPLICATES
# ============================================================

duplicate_count = combined_df.duplicated().sum()

cleaned_df = combined_df.drop_duplicates().copy()

remaining_records = len(cleaned_df)

# ============================================================
# 4. DUPLICATE REMOVAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATE REMOVAL SUMMARY")
print("=" * 60)

print(f"Worksheet 1 Records: {len(df_1):,}")
print(f"Worksheet 2 Records: {len(df_2):,}")
print(f"Original Combined Records: {original_records:,}")

print(f"\nDuplicate Records Identified: {duplicate_count:,}")
print(f"Records Removed: {original_records - remaining_records:,}")
print(f"Remaining Records: {remaining_records:,}")

print(
    f"\nRemaining Duplicate Records: "
    f"{cleaned_df.duplicated().sum():,}"
)

# ============================================================
# 5. INVESTIGATE AND HANDLE MISSING DESCRIPTIONS
# ============================================================

print("\n" + "=" * 60)
print("MISSING DESCRIPTION INVESTIGATION")
print("=" * 60)

missing_before = cleaned_df["Description"].isna().sum()

# Identify StockCodes with exactly one unique description
description_counts = (
    cleaned_df.dropna(subset=["Description"])
    .groupby("StockCode")["Description"]
    .nunique()
)

unambiguous_codes = description_counts[
    description_counts == 1
].index

# Build reliable StockCode-to-Description mapping
description_mapping = (
    cleaned_df[
        cleaned_df["StockCode"].isin(unambiguous_codes)
        & cleaned_df["Description"].notna()
    ]
    .drop_duplicates(subset=["StockCode"])
    .set_index("StockCode")["Description"]
)

# Fill missing descriptions only where mapping is unambiguous
cleaned_df["Description"] = cleaned_df["Description"].fillna(
    cleaned_df["StockCode"].map(description_mapping)
)

missing_after = cleaned_df["Description"].isna().sum()

recovered = missing_before - missing_after

print(f"Missing descriptions before: {missing_before:,}")
print(f"Reliable descriptions recovered: {recovered:,}")
print(f"Missing descriptions remaining: {missing_after:,}")

# ============================================================
# 6. SAVE CLEANED DATASET
# ============================================================

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

cleaned_df.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 60)
print("CLEANING PIPELINE SUMMARY")
print("=" * 60)

print(f"Final Records: {len(cleaned_df):,}")
print(f"Remaining Duplicate Records: {cleaned_df.duplicated().sum():,}")
print(f"Remaining Missing Descriptions: {missing_after:,}")

print(f"\nCleaned dataset saved to:\n{output_path}")

print("\nDATA CLEANING OPERATIONS COMPLETED.")