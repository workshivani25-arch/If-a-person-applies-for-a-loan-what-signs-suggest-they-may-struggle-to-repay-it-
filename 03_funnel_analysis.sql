-- 03 Funnel Analysis
-- Purpose: build counts for a Tableau funnel chart.

WITH funnel AS (
    SELECT
        '1. Raw applications' AS stage,
        COUNT(*) AS applicant_count
    FROM loan_applications

    UNION ALL

    SELECT
        '2. Has valid target' AS stage,
        COUNT(*) AS applicant_count
    FROM loan_applications
    WHERE target_default IS NOT NULL

    UNION ALL

    SELECT
        '3. Has income and loan amount' AS stage,
        COUNT(*) AS applicant_count
    FROM loan_applications
    WHERE target_default IS NOT NULL
      AND annual_income IS NOT NULL
      AND loan_amount IS NOT NULL

    UNION ALL

    SELECT
        '4. Modelling-ready records' AS stage,
        COUNT(*) AS applicant_count
    FROM loan_applications
    WHERE target_default IS NOT NULL
      AND annual_income IS NOT NULL
      AND loan_amount IS NOT NULL
      AND annual_income > 0
      AND loan_amount > 0
)
SELECT
    stage,
    applicant_count,
    ROUND(100.0 * applicant_count / FIRST_VALUE(applicant_count) OVER (ORDER BY stage), 2) AS percent_of_raw
FROM funnel
ORDER BY stage;

