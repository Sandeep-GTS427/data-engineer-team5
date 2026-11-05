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

## 10. FastAPI Dataset Validation Integration Evidence

The FastAPI endpoint `POST /api/v1/datasets/profile` was tested using Swagger UI and separately registered PostgreSQL dataset metadata.

### 10.1 Valid Dataset

| Field | Result |
|---|---|
| Dataset ID | customers_001 |
| Dataset rows | 3 |
| Dataset columns | 3 |
| Validation status | PASS |
| API status | success |

All seven validation rules passed.

### 10.2 Invalid Data Type Configuration

| Field | Result |
|---|---|
| Dataset ID | customers_001 |
| Configured age type | date |
| Supported types | integer, number, string |
| API status | failed |
| Error code | EXPECTED_TYPES |

The API correctly rejected the unsupported expected-type configuration.

### 10.3 Invalid Data Value

Test dataset: api_invalid_001

| Field | Result |
|---|---|
| Invalid column | age |
| Invalid value | unknown |
| Expected type | integer |
| Total rows | 3 |
| Invalid type count | 1 |
| API status | warning |

The validator correctly identified the invalid value at row 3 in the age column.

### 10.4 Missing-Value Detection

Test dataset: api_missing_001

| Field | Result |
|---|---|
| Total rows | 3 |
| Total columns | 3 |
| Missing column | name |
| Missing value count | 1 |
| API status | warning |

The API correctly identified one missing value in the name column.

### 10.5 Duplicate-Row Detection

Test dataset: api_duplicates_001

| Field | Result |
|---|---|
| Total rows | 3 |
| Total columns | 3 |
| Duplicate row count | 1 |
| API status | warning |

The validator correctly detected one duplicate row and returned a warning without automatically deleting records.

### 10.6 API Health Verification

Endpoint: GET /health

Result:
- Status: success
- Message: Team 5 Data Engineering API is running.

### 10.7 Unknown Dataset ID Handling

Test scenario: Dataset ID does not exist in PostgreSQL metadata.

Request dataset ID: `non_existing_999`

| Field | Result |
|---|---|
| Expected HTTP status | 404 |
| Actual HTTP status | 404 |
| Response message | Dataset not found. |
| Result | PASS |

The API correctly returned HTTP 404 when the requested dataset ID was not found in the metadata table. CSV validation was not started.

### 10.8 Integration Test Summary

| Test Scenario | Observed Result |
|---|---|
| Valid dataset | Success |
| Unsupported type configuration | Rejected |
| Invalid data value | Warning |
| Missing value | Warning |
| Duplicate row | Warning |
| API health | Success |
| Unknown dataset ID | HTTP 404 |

Note: The API currently performs CSV validation through the profile endpoint. The standalone data profiler is not yet integrated into this endpoint.

## 11. Updated Conclusion

In addition to the four standalone profiling datasets, the FastAPI validation endpoint was tested with valid data, invalid type configuration, invalid data values, missing values, duplicate rows, and an unknown dataset ID.

The API correctly returned success, failure, warning, or HTTP 404 outcomes according to the tested scenarios. The API health endpoint was also verified successfully.

All 33 automated regression tests passed.

Large-dataset performance, profiler API integration, transformation implementation, and downstream AI/ML handoff remain pending verification.