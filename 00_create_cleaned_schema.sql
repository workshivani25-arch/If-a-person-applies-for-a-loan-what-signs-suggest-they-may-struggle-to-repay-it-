-- 00 Create Cleaned Schema
-- Purpose: define the SQL table structure for the cleaned applicant-level dataset.
-- Source file created locally by Python:
-- data/processed/loan_applications_clean.csv

DROP TABLE IF EXISTS loan_applications;

CREATE TABLE loan_applications (
    applicant_id INTEGER PRIMARY KEY,
    target_default INTEGER,
    contract_type TEXT,
    gender TEXT,
    owns_car BOOLEAN,
    owns_property BOOLEAN,
    children_count INTEGER,
    annual_income REAL,
    loan_amount REAL,
    annual_repayment REAL,
    goods_price REAL,
    income_type TEXT,
    education_type TEXT,
    family_status TEXT,
    housing_type TEXT,
    occupation_type TEXT,
    family_members_count REAL,
    region_rating INTEGER,
    age_years REAL,
    employment_years REAL,
    employment_years_missing BOOLEAN,
    repayment_burden_ratio REAL,
    loan_to_income_ratio REAL,
    income_band TEXT,
    external_score_mean REAL,
    external_score_1_missing BOOLEAN,
    external_score_2_missing BOOLEAN,
    external_score_3_missing BOOLEAN,
    credit_bureau_requests_year REAL,
    credit_bureau_requests_year_missing BOOLEAN,
    risk_proxy_score REAL,
    risk_band TEXT
);

-- Example load command for SQLite CLI:
-- .mode csv
-- .import --skip 1 data/processed/loan_applications_clean.csv loan_applications

