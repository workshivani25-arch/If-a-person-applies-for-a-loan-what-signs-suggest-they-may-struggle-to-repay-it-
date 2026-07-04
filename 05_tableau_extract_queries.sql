-- 05 Tableau Extract Queries
-- Purpose: create small summary tables that are easy to connect to Tableau.

-- Extract 1: Applicant funnel.
WITH funnel AS (
    SELECT 1 AS stage_order, 'Raw applications' AS stage, COUNT(*) AS applicant_count
    FROM loan_applications

    UNION ALL

    SELECT 2, 'Valid target', COUNT(*)
    FROM loan_applications
    WHERE target_default IS NOT NULL

    UNION ALL

    SELECT 3, 'Income and loan present', COUNT(*)
    FROM loan_applications
    WHERE target_default IS NOT NULL
      AND annual_income IS NOT NULL
      AND loan_amount IS NOT NULL

    UNION ALL

    SELECT 4, 'Model-ready', COUNT(*)
    FROM loan_applications
    WHERE target_default IS NOT NULL
      AND annual_income > 0
      AND loan_amount > 0
      AND annual_repayment IS NOT NULL

    UNION ALL

    SELECT 5, 'High-risk review', COUNT(*)
    FROM loan_applications
    WHERE risk_band = 'High'
)
SELECT
    stage_order,
    stage,
    applicant_count,
    ROUND(
        100.0 * applicant_count / FIRST_VALUE(applicant_count) OVER (ORDER BY stage_order),
        2
    ) AS percent_of_raw
FROM funnel
ORDER BY stage_order;

-- Extract 2: Risk segment summary.
SELECT
    risk_band,
    COUNT(*) AS applicant_count,
    SUM(target_default) AS default_count,
    ROUND(100.0 * SUM(target_default) / COUNT(*), 2) AS default_rate_percent,
    ROUND(AVG(annual_income), 2) AS avg_annual_income,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(repayment_burden_ratio), 4) AS avg_repayment_burden_ratio
FROM loan_applications
GROUP BY risk_band;

-- Extract 3: Borrower profile by income band.
SELECT
    income_band,
    COUNT(*) AS applicant_count,
    SUM(target_default) AS default_count,
    ROUND(100.0 * SUM(target_default) / COUNT(*), 2) AS default_rate_percent,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(loan_to_income_ratio), 4) AS avg_loan_to_income_ratio
FROM loan_applications
GROUP BY income_band;

