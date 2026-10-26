# HR Data Quality Validation Results

## 1. Overview

**Database:** AdventureWorks2025  
**Schema:** HumanResources  
**Purpose:** Document SQL-based data quality checks performed on the HR tables.

## 2. Employee Validation

| Validation Check | Result | Status |
|---|---|---|
| Total employee records | 290 | PASS |
| Unique BusinessEntityID values | 290 | PASS |
| Missing NationalIDNumber | 0 | PASS |
| Missing LoginID | 0 | PASS |
| Missing JobTitle | 0 | PASS |
| Missing BirthDate | 0 | PASS |
| Missing HireDate | 0 | PASS |
| BirthDate after HireDate | 0 | PASS |
| Future BirthDate values | 0 | PASS |
| Future HireDate values | 0 | PASS |

## 3. Organization Hierarchy

| Check | Result |
|---|---|
| Employees with missing OrganizationNode | 1 |
| Employees with missing OrganizationLevel | 1 |
| Affected employee | BusinessEntityID 1 — Chief Executive Officer |
| Status | REVIEW |

The CEO record has NULL values for both organization hierarchy fields. All 289 employees with populated OrganizationLevel values also have populated OrganizationNode values.

The intended business rule must be confirmed before classifying this record as valid or invalid.

## 4. Department History and Relationships

| Validation Check | Result | Status |
|---|---|---|
| Department history records | 296 | INFORMATION |
| Records with NULL EndDate | 290 | REVIEW |
| EndDate earlier than StartDate | No matching rows | PASS |
| Overlapping assignments in the same department | No matching rows | PASS |
| Invalid employee references in department history | 0 | PASS |
| Invalid department references | 0 | PASS |
| Invalid shift references | 0 | PASS |

NULL EndDate values may represent ongoing assignments. Confirm the intended business rule before treating them as failures.

## 5. Employee Pay History

| Validation Check | Result | Status |
|---|---|---|
| Invalid employee references | 0 | PASS |
| Non-positive pay rates | 0 | PASS |

## 6. Job Candidates

| Validation Check | Result | Status |
|---|---|---|
| Total candidate records | 13 | INFORMATION |
| Candidates without an employee link | 11 | REVIEW |
| Invalid non-NULL employee references | 0 | PASS |

A candidate without an employee link may be valid. Confirm the expected relationship rules before classifying these records.

## 7. Department and Shift Duplicate Checks

- No duplicate DepartmentID values were found.
- No duplicate ShiftID values were found.
- No duplicate Department Name and GroupName combinations were found.
- No duplicate Shift Name, StartTime, and EndTime combinations were found.

These checks cover the specified fields; they do not establish that every complete row in every table is unique.

## 8. Summary and Follow-Up

The SQL checks completed so far found no violations in the tested employee identifiers, required fields, date rules, pay-rate rule, or selected foreign-key relationships.

Items requiring business-rule confirmation:

1. NULL organization hierarchy values for the CEO.
2. Department history records with NULL EndDate.
3. Job candidates without an employee link.

## 9. Scope and Limitations

These results document checks performed against the AdventureWorks2025 sample database. They do not establish that all project requirements have been implemented or that all data quality rules have been tested.

The results must be compared with the agreed Team 5 validation requirements before being treated as final acceptance evidence.