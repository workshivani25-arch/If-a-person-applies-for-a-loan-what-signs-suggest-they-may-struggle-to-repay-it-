-- 06 Cleaned Data Validation
-- Purpose: validate the cleaned applicant-level table before EDA and modelling.
-- Assumed table: loan_applications

-- 1. Confirm row count and applicant uniqueness.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT applicant_id) AS unique_applicants,
    COUNT(*) - COUNT(DISTINCT applicant_id) AS duplicate_applicant_rows
FROM loan_applications;

-- 2. Confirm target values are valid.
SELECT
    target_default,
    COUNT(*) AS applicant_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS applicant_percent
FROM loan_applications
GROUP BY target_default
ORDER BY target_default;

-- 3. Check core numeric fields for missing or invalid values.
SELECT
    SUM(CASE WHEN annual_income IS NULL THEN 1 ELSE 0 END) AS missing_income,
    SUM(CASE WHEN annual_income <= 0 THEN 1 ELSE 0 END) AS non_positive_income,
    SUM(CASE WHEN loan_amount IS NULL THEN 1 ELSE 0 END) AS missing_loan_amount,
    SUM(CASE WHEN loan_amount <= 0 THEN 1 ELSE 0 END) AS non_positive_loan_amount,
    SUM(CASE WHEN annual_repayment IS NULL THEN 1 ELSE 0 END) AS missing_annual_repayment
FROM loan_applications;

-- 4. Check age and employment ranges after transformation.
SELECT
    MIN(age_years) AS min_age_years,
    MAX(age_years) AS max_age_years,
    MIN(employment_years) AS min_employment_years,
    MAX(employment_years) AS max_employment_years,
    SUM(CASE WHEN employment_years_missing = 1 THEN 1 ELSE 0 END) AS employment_years_missing_count
FROM loan_applications;

-- 5. Validate engineered risk bands.
SELECT
    risk_band,
    COUNT(*) AS applicant_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS applicant_percent,
    ROUND(AVG(target_default) * 100, 2) AS default_rate_percent
FROM loan_applications
GROUP BY risk_band
ORDER BY default_rate_percent;

