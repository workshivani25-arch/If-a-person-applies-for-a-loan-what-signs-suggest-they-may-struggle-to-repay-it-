# Data Audit Summary

Download instructions are documented in [kaggle_home_credit_download.md](kaggle_home_credit_download.md).
## Australian Context, Purpose and Source  of the Data

| Data Source | Purpose | Use In Project |
|---|---|---|
| ABS Lending Indicators | Adds Australian lending context. Useful for showing housing loan commitments, investor lending, owner-occupier lending, and first-home buyer trends. | Trend charts in Python and Tableau. Australian market context section in final report. |
| APRA ADI Statistics | Adds Australian banking and mortgage exposure context. Useful for discussing residential mortgage exposure and lending standards. | Banking-sector framing. Risk commentary and market context charts. |
| RBA Statistical Tables | Adds interest-rate, housing credit, and household finance context. | Interest-rate pressure analysis. Housing credit trend analysis. Tableau market context dashboard. |
| NSW Property Sales or Rental Bond Data | Adds housing affordability or rental-pressure context if needed. | Optional postcode or region-level housing stress analysis. Optional Tableau map or suburb comparison. |
## Raw Table Inventory

| File | Rows | Columns | Size MB |
|---|---:|---:|---:|
| `HomeCredit_columns_description.csv` | 219 | 5 | 0.04 |
| `POS_CASH_balance.csv` | 10,001,358 | 8 | 392.70 |
| `application_test.csv` | 48,744 | 121 | 26.57 |
| `application_train.csv` | 307,511 | 122 | 166.13 |
| `bureau.csv` | 1,716,428 | 17 | 170.02 |
| `bureau_balance.csv` | 27,299,925 | 3 | 375.59 |
| `credit_card_balance.csv` | 3,840,312 | 23 | 424.58 |
| `installments_payments.csv` | 13,605,401 | 8 | 723.12 |
| `previous_application.csv` | 1,670,214 | 37 | 404.97 |
| `sample_submission.csv` | 48,744 | 2 | 0.54 |

## Main Training Table

`application_train.csv`

- Rows: 307,511
- Columns: 122
- Duplicate rows: 0

## Early Data Quality Notes

The main application table has several columns with high missingness, especially building and property-related fields such as:

- `COMMONAREA_MEDI`
- `COMMONAREA_AVG`
- `COMMONAREA_MODE`
- `NONLIVINGAPARTMENTS_MODE`
- `NONLIVINGAPARTMENTS_AVG`
- `NONLIVINGAPARTMENTS_MEDI`

These columns will need careful handling during cleaning and feature engineering.

