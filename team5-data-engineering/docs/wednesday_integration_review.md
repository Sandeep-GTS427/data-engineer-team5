# Wednesday Integration Review – Team 5 Data Engineering

**Date:** November 4, 2026  
**Team:** Team 5 – Data Engineering  
**Role:** Data Engineering Lead  
**Status:** Integration review and sample execution completed

## 1. Overview

This document records the integration review and sample execution performed by Team 5 as part of Week 3 activities.

The objective was to review the existing data engineering implementation, verify PostgreSQL metadata retrieval, execute the dataset validation API, test standalone CSV profiling, and compare the results.

The review was performed without modifying the existing validation module or API response structure.

## 2. Existing Project Architecture

The current implementation consists of the following components:

| Component | Responsibility |
|---|---|
| FastAPI | Exposes dataset validation endpoint |
| PostgreSQL | Stores dataset metadata |
| data_validator.py | Validates CSV datasets |
| data_profiler.py | Generates dataset and column-level statistics |
| main.py | Handles API requests and metadata retrieval |

### Current API Workflow

1. Receive dataset identifier through the API request.
2. Retrieve dataset metadata from PostgreSQL.
3. Obtain the CSV file path and format.
4. Verify that the dataset format is supported.
5. Execute CSV validation.
6. Return structured validation results.

## 3. PostgreSQL Metadata Verification

The existing API uses PostgreSQL to retrieve dataset metadata from the `dataset_metadata` table.

The following dataset was successfully retrieved:

| Field | Value |
|---|---|
| Dataset ID | customers_001 |
| Dataset Name | Customers Dataset |
| File Name | customers.csv |
| File Format | CSV |

**Result:** PostgreSQL metadata lookup completed successfully.

## 4. API Validation Execution

The existing FastAPI endpoint was tested using Swagger UI.

**Endpoint:**

`POST /api/v1/datasets/profile`

**Request:**

```json
{
  "dataset_reference": {
    "dataset_id": "customers_001"
  },
  "expected_types": {}
}
```

### Actual Execution Results

| Validation Check | Result |
|---|---|
| Valid header | PASS |
| Required columns | PASS |
| Data rows present | PASS |
| Empty columns | PASS |
| Missing values | PASS |
| Duplicate rows | PASS |

### Dataset Statistics

| Metric | Result |
|---|---:|
| Row count | 3 |
| Column count | 3 |
| Missing value count | 0 |
| Duplicate row count | 0 |
| Invalid type count | 0 |
| API status | success |

**Result:** The API successfully retrieved dataset metadata and executed CSV validation.

## 5. Standalone CSV Profiling Execution

The standalone profiling module was tested using the same dataset.

**Module:** `src/data_profiler.py`

**Dataset:** `data/customers.csv`

**Execution command:**

```bash
python -c "from src.data_profiler import profile_csv; import json; print(json.dumps(profile_csv('data/customers.csv'), indent=4))"
```

### Actual Profiling Results

| Column | Data Type | Null Count | Null Percentage | Distinct Count | Minimum | Maximum |
|---|---|---:|---:|---:|---:|---:|
| customer_id | integer | 0 | 0% | 3 | 1 | 3 |
| name | string | 0 | 0% | 3 | N/A | N/A |
| age | integer | 0 | 0% | 3 | 25 | 30 |

Dataset statistics:

- Total rows: 3
- Total columns: 3
- All columns successfully identified.
- No missing values detected.

**Result:** Standalone CSV profiling executed successfully.

## 6. Validation and Profiling Comparison

Both modules were executed against the same CSV dataset.

| Metric | Validation API | Standalone Profiler |
|---|---:|---:|
| Row count | 3 | 3 |
| Column count | 3 | 3 |
| Missing values | 0 | 0 |
| Duplicate rows | 0 | Not measured |
| Column data types | Validation checks | Detected |
| Distinct values | Not reported | 3 per column |

### Observations

1. Both modules reported matching row and column counts.
2. Both modules reported no missing values.
3. The validation module checked duplicate rows.
4. The profiling module calculated column-level distinct counts.
5. The profiling module identified integer and string data types correctly.

Note: Duplicate-row count and distinct-value count are different measurements.

## 7. Current Integration Status

| Component | Current Status |
|---|---|
| PostgreSQL metadata lookup | Implemented and verified |
| CSV validation module | Implemented and verified |
| CSV profiling module | Implemented and tested independently |
| FastAPI validation endpoint | Implemented and verified |
| Profiling through FastAPI | Not yet integrated |
| Transformation pipeline | Pending requirements confirmation |
| Team 1 dataset handoff | Pending confirmation |
| AWS storage integration | Pending infrastructure details |

## 8. Integration Gaps and Dependencies

### Team 1 – AI/ML Team

Pending confirmations:

- Expected profiling output structure.
- Dataset preprocessing requirements.
- Feature engineering requirements.
- Processed dataset handoff format.

### Team 2 – Backend and Ingestion Team

Pending confirmations:

- Common company GitHub repository.
- Finalized API contract.
- API request and response structure.
- Dataset ingestion and persistence integration.

### Database Engineer

Pending confirmations:

- Required metadata fields.
- Profiling result persistence.
- Transformation history requirements.

### AWS Engineer

Pending confirmations:

- Dataset storage location.
- AWS access and integration requirements.
- Storage and deployment configuration.

## 9. Automated Regression Testing

The complete automated test suite was executed using:

```bash
python -m unittest discover -s test -v
```

### Test Results

| Test Module | Passed |
|---|---:|
| test_data_profiler.py | 9 |
| test_data_validator.py | 21 |
| test_quality_scenarios.py | 3 |
| **Total** | **33** |

**Final Result: 33 tests passed, 0 failures.**

## 10. Conclusion

The Wednesday integration review confirmed that the existing PostgreSQL metadata lookup and FastAPI validation workflow are functioning successfully.

The standalone CSV profiling module also generated the expected dataset-level and column-level statistics when executed against the same dataset.

The validation and profiling modules currently operate as separate components.

Further API integration, dataset handoff, database persistence changes, and AWS integration will proceed after the required technical contracts and responsibilities are confirmed by the respective teams.

The existing implementation and all 33 automated tests remain successful.