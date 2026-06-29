# Data Audit Summary

## Kaggle Home Credit Files

All expected Kaggle Home Credit files are available locally in:

```text
data/raw/kaggle_home_credit/
```

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

