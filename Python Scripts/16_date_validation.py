import pandas as pd
from pathlib import Path

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

deduplicated_path = BASE_DIR / "Cleaned Data" / "online_retail_II_deduplicated.csv"
analysis_path = BASE_DIR / "Cleaned Data" / "online_retail_II_analysis_ready.csv"

results_dir = BASE_DIR / "Investigation Results"
results_dir.mkdir(exist_ok=True)

# ============================================================
# LOAD DATA WITHOUT AUTOMATIC DATE CONVERSION
# ============================================================

print("=" * 65)
print("DATE VALIDATION AND CONSISTENCY INVESTIGATION")
print("=" * 65)

datasets = {
    "Deduplicated": pd.read_csv(
        deduplicated_path,
        dtype={"InvoiceDate": "string"}
    ),
    "Analysis Ready": pd.read_csv(
        analysis_path,
        dtype={"InvoiceDate": "string"}
    )
}

print("\n1. RAW DATE SAMPLES")

for name, df in datasets.items():
    print(f"\n{name} Dataset:")
    print(df["InvoiceDate"].head(10).to_string(index=False))

# ============================================================
# COMPARE DATE PARSING METHODS
# ============================================================

summary_results = []
monthly_results = []

for name, df in datasets.items():

    print("\n" + "=" * 65)
    print(f"{name.upper()} DATASET")
    print("=" * 65)

    raw_dates = df["InvoiceDate"]

    parsing_methods = {
        "Default": pd.to_datetime(raw_dates, errors="coerce"),
        "Day First": pd.to_datetime(
            raw_dates,
            errors="coerce",
            dayfirst=True
        )
    }

    for method, dates in parsing_methods.items():

        valid_count = dates.notna().sum()
        invalid_count = dates.isna().sum()

        earliest = dates.min()
        latest = dates.max()

        print(f"\n{method} Parsing:")
        print(f"Valid Dates: {valid_count:,}")
        print(f"Invalid Dates: {invalid_count:,}")
        print(f"Earliest Date: {earliest}")
        print(f"Latest Date: {latest}")

        summary_results.append({
            "Dataset": name,
            "Parsing Method": method,
            "Valid Dates": valid_count,
            "Invalid Dates": invalid_count,
            "Earliest Date": earliest,
            "Latest Date": latest
        })

        monthly = (
            dates.dropna()
            .dt.to_period("M")
            .value_counts()
            .sort_index()
        )

        print("\nMonthly Record Distribution:")
        print(monthly.to_string())

        for month, count in monthly.items():
            monthly_results.append({
                "Dataset": name,
                "Parsing Method": method,
                "Month": str(month),
                "Records": count
            })

# ============================================================
# SALES-ONLY DATE VALIDATION
# ============================================================

print("\n" + "=" * 65)
print("2. SALES-ONLY DATE VALIDATION")
print("=" * 65)

df = datasets["Analysis Ready"].copy()

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

sales_df = df[
    (~df["Invoice"].astype(str).str.startswith("C")) &
    (df["Quantity"] > 0) &
    (df["Price"] >= 0) &
    (
        df["Description"].fillna("")
        .astype(str).str.strip().str.lower() != "adjust bad debt"
    )
].copy()

print(f"\nSales Records: {len(sales_df):,}")
print(f"Earliest Sales Date: {sales_df['InvoiceDate'].min()}")
print(f"Latest Sales Date: {sales_df['InvoiceDate'].max()}")

sales_monthly = (
    sales_df.dropna(subset=["InvoiceDate"])
    .groupby(sales_df["InvoiceDate"].dt.to_period("M"))
    .size()
    .sort_index()
)

print("\nSales Records by Month:")
print(sales_monthly.to_string())

for month, count in sales_monthly.items():
    monthly_results.append({
        "Dataset": "Sales Only",
        "Parsing Method": "Default",
        "Month": str(month),
        "Records": count
    })

# ============================================================
# EXPORT RESULTS
# ============================================================

summary_df = pd.DataFrame(summary_results)
monthly_df = pd.DataFrame(monthly_results)

summary_df.to_csv(
    results_dir / "date_validation_comparison.csv",
    index=False
)

monthly_df.to_csv(
    results_dir / "date_validation_monthly_comparison.csv",
    index=False
)

print("\n" + "=" * 65)
print("DATE VALIDATION COMPLETED")
print("=" * 65)

print("\nFiles Exported:")
print("- date_validation_comparison.csv")
print("- date_validation_monthly_comparison.csv")

print("\nNo dates or source records have been modified.")