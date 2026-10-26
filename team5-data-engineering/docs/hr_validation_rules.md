# HR Data Validation Rules

## 1. Purpose

This document defines the HR data validation rules investigated during SQL analysis. Final rule severity must be aligned with the agreed project requirements.

## 2. Validation Rules

| Rule ID | Validation Rule | Expected Behavior | Current Status |
|---|---|---|---|
| HR-001 | Employee ID uniqueness | Each BusinessEntityID must be unique in HumanResources.Employee. | PASS |
| HR-002 | Required employee fields | NationalIDNumber, LoginID, JobTitle, BirthDate, and HireDate must not be NULL. | PASS |
| HR-003 | Birth date and hire date | BirthDate must not be later than HireDate. | PASS |
| HR-004 | Future birth date | BirthDate must not be in the future. | PASS |
| HR-005 | Future hire date | HireDate must not be in the future. | PASS |
| HR-006 | Organization hierarchy | Missing hierarchy values must follow the agreed hierarchy rules. | REVIEW |
| HR-007 | Department history dates | EndDate must not be earlier than StartDate when EndDate is present. | PASS |
| HR-008 | Employee references | Non-NULL employee references must match an existing employee. | PASS |
| HR-009 | Department references | DepartmentID in department history must match an existing department. | PASS |
| HR-010 | Shift references | ShiftID in department history must match an existing shift. | PASS |
| HR-011 | Pay rates | Pay rates must be greater than zero, if required by the business rule. | PASS |
| HR-012 | Candidate employee link | A non-NULL employee link must reference an existing employee. | PASS |
| HR-013 | Department history EndDate | NULL EndDate values must be handled according to the history rules. | REVIEW |
| HR-014 | Duplicate department and shift values | The tested field combinations should not be duplicated if required by the business rules. | PASS |
| HR-015 | Same-department assignment overlap | Investigate overlapping date ranges for the same employee and department. | PASS |

## 3. Outcome Classification

### PASS
The executed check found no violations of the tested rule.

### FAIL
The input violates a confirmed mandatory business rule and should not proceed without correction or rejection.

### WARNING / REVIEW
The result requires further inspection, clarification, or business-rule confirmation. It should not automatically be treated as a failure.

### NOT TESTED
The rule has not yet been implemented or executed.

## 4. Validation Behavior

- Do not modify source data during validation.
- Do not automatically replace NULL values.
- Distinguish mandatory validation failures from quality warnings.
- Return actionable messages that identify the affected rule and explain the issue.
- Record expected and actual outcomes when testing with synthetic datasets.
- Confirm rule severity with the project requirements before finalizing the validation prototype.

## 5. Outstanding Decisions

1. Confirm whether the CEO can have NULL organization hierarchy values.
2. Confirm how open-ended department history records should be handled.
3. Confirm whether candidates without employee links are acceptable.
4. Align rule severity and output format with the agreed project/API contract.

## 6. Scope

These rules reflect the SQL checks investigated so far. They are not a complete or approved specification for the entire DataFlow project. Additional rules and test cases may be required by the team requirements.