-- 01 Data Quality Checks
-- Purpose: profile the raw loan-risk data before modelling.
-- Note: table names will be finalised after the Kaggle dataset is selected.

-- 1. Count total records.
SELECT
    COUNT(*) AS total_records
FROM loan_applications;

-- 2. Count duplicate applicant IDs.
SELECT
    applicant_id,
    COUNT(*) AS record_count
FROM loan_applications
GROUP BY applicant_id
HAVING COUNT(*) > 1
ORDER BY record_count DESC;

-- 3. Check important missing values.
SELECT
    COUNT(*) AS total_records,
    SUM(CASE WHEN target_default IS NULL THEN 1 ELSE 0 END) AS missing_target,
    SUM(CASE WHEN annual_income IS NULL THEN 1 ELSE 0 END) AS missing_income,
    SUM(CASE WHEN loan_amount IS NULL THEN 1 ELSE 0 END) AS missing_loan_amount,
    SUM(CASE WHEN employment_type IS NULL THEN 1 ELSE 0 END) AS missing_employment_type
FROM loan_applications;

-- 4. Check target balance.
SELECT
    target_default,
    COUNT(*) AS applicant_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS applicant_percent
FROM loan_applications
GROUP BY target_default
ORDER BY target_default;

