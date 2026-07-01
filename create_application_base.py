"""Create the first clean applicant-level dataset from Kaggle raw files.

This script starts with the main application table only. It creates clearer
column names, handles known messy values, and adds simple banking-style
features that can be used in SQL, Tableau, and early machine learning work.
"""

from __future__ import annotations

import pandas as pd

from data_audit import read_csv_with_fallback
from project_paths import KAGGLE_HOME_CREDIT_DIR, PROCESSED_DATA_DIR, REPORTS_DIR


RAW_FILE = KAGGLE_HOME_CREDIT_DIR / "application_train.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "loan_applications_clean.csv"
CLEANING_REPORT = REPORTS_DIR / "cleaning_summary.md"


COLUMN_MAP = {
    "SK_ID_CURR": "applicant_id",
    "TARGET": "target_default",
    "NAME_CONTRACT_TYPE": "contract_type",
    "CODE_GENDER": "gender",
    "FLAG_OWN_CAR": "owns_car",
    "FLAG_OWN_REALTY": "owns_property",
    "CNT_CHILDREN": "children_count",
    "AMT_INCOME_TOTAL": "annual_income",
    "AMT_CREDIT": "loan_amount",
    "AMT_ANNUITY": "annual_repayment",
    "AMT_GOODS_PRICE": "goods_price",
    "NAME_INCOME_TYPE": "income_type",
    "NAME_EDUCATION_TYPE": "education_type",
    "NAME_FAMILY_STATUS": "family_status",
    "NAME_HOUSING_TYPE": "housing_type",
    "DAYS_BIRTH": "days_birth",
    "DAYS_EMPLOYED": "days_employed",
    "OCCUPATION_TYPE": "occupation_type",
    "CNT_FAM_MEMBERS": "family_members_count",
    "REGION_RATING_CLIENT": "region_rating",
    "EXT_SOURCE_1": "external_score_1",
    "EXT_SOURCE_2": "external_score_2",
    "EXT_SOURCE_3": "external_score_3",
    "AMT_REQ_CREDIT_BUREAU_YEAR": "credit_bureau_requests_year",
}


def assign_income_band(income: pd.Series) -> pd.Series:
    """Group annual income into readable bands for SQL and Tableau."""
    return pd.cut(
        income,
        bins=[-float("inf"), 30_000, 60_000, 100_000, 150_000, float("inf")],
        labels=["Under 30k", "30k to 60k", "60k to 100k", "100k to 150k", "150k+"],
    ).astype("string")


def assign_risk_band(proxy_score: pd.Series) -> pd.Series:
    """Create an early rule-based risk band before machine learning is trained."""
    return pd.cut(
        proxy_score,
        bins=[-float("inf"), 0.90, 1.20, float("inf")],
        labels=["Low", "Medium", "High"],
    ).astype("string")


def yes_no_to_boolean(series: pd.Series) -> pd.Series:
    """Convert Kaggle Y/N flags into true/false values."""
    return series.map({"Y": True, "N": False}).astype("boolean")


def safe_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Calculate a ratio only when the denominator is positive."""
    ratio = numerator / denominator.where(denominator > 0)
    return ratio.replace([float("inf"), -float("inf")], pd.NA).round(4)


def build_application_base() -> pd.DataFrame:
    """Load, clean, and lightly feature engineer the main application table."""
    df = read_csv_with_fallback(RAW_FILE, usecols=list(COLUMN_MAP)).rename(columns=COLUMN_MAP)

    df["gender"] = df["gender"].replace({"XNA": "Unknown"})
    df["owns_car"] = yes_no_to_boolean(df["owns_car"])
    df["owns_property"] = yes_no_to_boolean(df["owns_property"])
    df["occupation_type"] = df["occupation_type"].fillna("Unknown")
    df["credit_bureau_requests_year_missing"] = df["credit_bureau_requests_year"].isna()
    df["credit_bureau_requests_year"] = df["credit_bureau_requests_year"].fillna(0)

    df["age_years"] = (-df["days_birth"] / 365.25).round(1)
    df["employment_years_missing"] = df["days_employed"].eq(365243)
    df["employment_years"] = (-df["days_employed"] / 365.25).round(1)
    df.loc[df["days_employed"] == 365243, "employment_years"] = pd.NA

    df["repayment_burden_ratio"] = safe_ratio(df["annual_repayment"], df["annual_income"])
    df["loan_to_income_ratio"] = safe_ratio(df["loan_amount"], df["annual_income"])
    df["income_band"] = assign_income_band(df["annual_income"])

    score_cols = ["external_score_1", "external_score_2", "external_score_3"]
    for score_col in score_cols:
        df[f"{score_col}_missing"] = df[score_col].isna()
    df["external_score_mean"] = df[score_cols].mean(axis=1)
    median_score = df["external_score_mean"].median()
    df["risk_proxy_score"] = (
        df["repayment_burden_ratio"].fillna(0)
        + df["loan_to_income_ratio"].fillna(0) / 10
        + (1 - df["external_score_mean"].fillna(median_score))
    ).round(4)
    df["risk_band"] = assign_risk_band(df["risk_proxy_score"])

    clean_columns = [
        "applicant_id",
        "target_default",
        "contract_type",
        "gender",
        "owns_car",
        "owns_property",
        "children_count",
        "annual_income",
        "loan_amount",
        "annual_repayment",
        "goods_price",
        "income_type",
        "education_type",
        "family_status",
        "housing_type",
        "occupation_type",
        "family_members_count",
        "region_rating",
        "age_years",
        "employment_years",
        "employment_years_missing",
        "repayment_burden_ratio",
        "loan_to_income_ratio",
        "income_band",
        "external_score_mean",
        "external_score_1_missing",
        "external_score_2_missing",
        "external_score_3_missing",
        "credit_bureau_requests_year",
        "credit_bureau_requests_year_missing",
        "risk_proxy_score",
        "risk_band",
    ]
    return df[clean_columns]


def build_cleaning_report(clean_df: pd.DataFrame) -> str:
    """Create a Markdown summary of the cleaning output."""
    default_rate = clean_df["target_default"].mean() * 100
    missing_summary = (
        clean_df.isna()
        .sum()
        .rename("missing_count")
        .reset_index()
        .rename(columns={"index": "column"})
    )
    missing_summary["missing_percent"] = (
        missing_summary["missing_count"] / len(clean_df) * 100
    ).round(2)
    top_missing = missing_summary.sort_values("missing_percent", ascending=False).head(10)

    lines = [
        "# Cleaning Summary",
        "",
        "## Output File",
        "",
        "`data/processed/loan_applications_clean.csv`",
        "",
        "This processed file is created locally and is not uploaded to GitHub because it is a large derived dataset.",
        "",
        "## Shape",
        "",
        f"- Rows: {len(clean_df):,}",
        f"- Columns: {len(clean_df.columns):,}",
        f"- Default rate: {default_rate:.2f}%",
        "",
        "## Cleaning Decisions",
        "",
        "- Renamed raw Kaggle columns into clearer business-friendly names.",
        "- Converted `FLAG_OWN_CAR` and `FLAG_OWN_REALTY` from Y/N values into boolean fields.",
        "- Converted `DAYS_BIRTH` into `age_years`.",
        "- Converted `DAYS_EMPLOYED` into `employment_years`.",
        "- Treated the special `DAYS_EMPLOYED = 365243` value as missing employment tenure.",
        "- Replaced missing occupation with `Unknown` so SQL and Tableau grouping is easier.",
        "- Created missing-value flags for external scores and bureau request count.",
        "- Created repayment burden and loan-to-income ratios using safe denominator checks.",
        "- Created income bands for readable analysis.",
        "- Created an early rule-based `risk_band` for dashboard and SQL examples.",
        "",
        "## Top Remaining Missing Values",
        "",
        "| Column | Missing Count | Missing Percent |",
        "|---|---:|---:|",
    ]
    for row in top_missing.itertuples(index=False):
        lines.append(f"| `{row.column}` | {int(row.missing_count):,} | {row.missing_percent:.2f}% |")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "This is the first cleaned applicant-level table. Later project stages will add aggregated features from bureau, previous application, instalment, credit card, and POS/cash balance tables.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    """Write the first processed application table."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    clean_df = build_application_base()
    clean_df.to_csv(OUTPUT_FILE, index=False)
    CLEANING_REPORT.write_text(build_cleaning_report(clean_df), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")
    print(f"Wrote {CLEANING_REPORT}")
    print(f"Rows: {len(clean_df):,}")
    print(f"Columns: {len(clean_df.columns):,}")


if __name__ == "__main__":
    main()
