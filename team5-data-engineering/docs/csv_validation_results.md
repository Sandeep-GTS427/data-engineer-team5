## 3. Automated Test Results

The following command was executed from the project root:

```powershell
python -m unittest discover -s test -v
```

**Result: PASS — 13 tests passed.**

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

**Execution summary:** 13 tests ran successfully with zero failures.

The empty-column test verified that a column containing only blank values is identified and reported as a warning. The structured-outcome test verified the presence of the rule name, status, summary, and actionable message.

These results confirm the tested behaviors only. Final severity rules and integration requirements remain subject to project-contract review.
