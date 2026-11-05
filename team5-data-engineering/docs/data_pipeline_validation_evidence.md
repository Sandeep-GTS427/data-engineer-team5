# Data Pipeline Validation Evidence

**Project:** Data Science Intelligence & Automated Machine Learning Engine
**Team:** Team 5 – Data Engineering
**Date:** November 5, 2026
**Prepared by:** Sandeep – Data Engineering Lead

## 1. Objective

Record evidence from manual verification of the CSV data profiler and its failure-handling behavior.

## 2. Profiling Test Datasets

| Dataset | Rows | Columns | Verification Result |
|---|---:|---:|---|
| profiling_duplicates.csv | 5 | 2 | Distinct-value statistics generated |
| profiling_missing_values.csv | 4 | 5 | Missing values correctly identified |
| profiling_mixed_data.csv | 4 | 2 | Mixed data type correctly identified |
| profiling_mixed_types.csv | 4 | 7 | Supported data types correctly detected |

## 3. Missing-Value Verification

For profiling_missing_values.csv:

| Column | Missing Values | Missing Percentage |
|---|---:|---:|
| name | 1 | 25% |
| age | 1 | 25% |
| salary | 1 | 25% |
| is_active | 1 | 25% |

The profiler returned null_pct as 0.25 for each of these columns.

## 4. Data-Type Verification

The profiling_mixed_types.csv dataset successfully identified:

- customer_id: integer
- name: string
- age: integer
- salary: decimal
- is_active: boolean
- joining_date: date
- last_login: timestamp

The profiling_mixed_data.csv dataset correctly identified the age column as mixed.

## 5. Duplicate-Related Statistics

For profiling_duplicates.csv:

- customer_id distinct count: 5
- city distinct count: 3

Note: These are column-level distinct-value counts, not duplicate-row counts.

## 6. Failure-Handling Evidence

| Test Scenario | Expected Behavior | Actual Result | Status |
|---|---|---|---|
| Empty CSV | Reject empty file | ValueError | Passed |
| Missing CSV file | Report missing file | FileNotFoundError | Passed |
| Malformed row with fewer values | Reject incorrect row width | Expected 3, found 2 | Passed |
| Malformed row with extra values | Reject incorrect row width | Expected 3, found 4 | Passed |

## 7. Automated Test Evidence

Command executed:

python -m unittest discover -s test -v

Result:
- Total automated tests: 33
- Passed: 33
- Failed: 0
- Errors: 0

## 8. Limitations and Pending Integration

- Large-dataset performance has not yet been measured.
- The profiler is currently a standalone module and is not integrated into the FastAPI profiling endpoint.
- Transformation and downstream AI/ML handoff require further implementation and integration verification.

## 9. Conclusion

The four profiling datasets and four failure-handling scenarios were successfully verified. The automated regression suite also passed all 33 tests.

This document records the observed test evidence and does not claim that pending integration activities are complete.
