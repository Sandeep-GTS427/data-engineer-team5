## 3. Automated Test Results

The following command was executed from the project root:

```powershell
python -m unittest discover -s test -v
```

**Result: PASS — 16 tests passed, 0 failures, 0 errors.**

| Test Case | Result |
|---|---|
| Valid CSV | PASS |
| Missing file | PASS |
| Empty file | PASS |
| Header-only file | PASS |
| Missing required column | PASS |
| Extra value in row | PASS |
| Missing values | PASS |
| Duplicate rows | PASS |
| Valid data types | PASS |
| Invalid data types | PASS |
| Invalid type finding details | PASS |
| Empty-column detection | PASS |
| Structured validation outcome | PASS |
| File exceeds size limit | PASS |
| Malformed CSV quoting | PASS |
| Invalid encoding | PASS |

**Execution summary:** 16 tests ran successfully with zero failures and zero errors.

The file-size test verifies that a file exceeding the configured limit is rejected. The malformed CSV quoting test verifies that malformed quoting is reported as a validation failure when strict CSV parsing is enabled. The invalid-encoding test verifies that invalid UTF-8 input is reported as a safe CSV read failure.

The validation findings avoid returning the invalid cell value, and CSV read errors use a general, actionable message rather than exposing raw exception details.

**Proposed upload requirements — pending confirmation from Team 2**

Team 2 has proposed a maximum upload size of 50 MB per file and support for CSV, XLSX, JSON, and Parquet. These specifications are not yet final.

The current prototype validates CSV files only and uses a configurable 10 MB default. The 10 MB value is provisional and must be reconciled with the confirmed upload contract before production integration. XLSX, JSON, and Parquet validation have not yet been implemented in this prototype.

These results confirm only the behaviors covered by the tests. Final severity rules, upload constraints, supported formats, API response schemas, and integration requirements remain subject to contract review.
