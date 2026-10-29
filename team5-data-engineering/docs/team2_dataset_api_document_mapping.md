# Team 2 Dataset Profiling API Document Mapping

**Owner:** Sandeep — Data/API Integration  
**Date:** 29 October 2026  
**Status:** Working notes — pending confirmation from Team 2 and Team 1

## 1. Purpose

Map Team 2's document, **“Dataset Profiling API — SQL & Backend Perspective,”** against Team 5's existing dataset API contract comparison and lifecycle notes. This mapping separates statements in the shared document from verbally reported details and unresolved decisions. Proposed examples are not treated as an approved API contract.

## 2. Team 2 Document: Key Details

| Area | What the shared document says | Current interpretation / action |
|---|---|---|
| Proposed endpoint | `POST /api/v1/datasets/profile` | Proposed only; Team 2 must confirm the actual endpoint and method. |
| Request identifier | Example request uses `dataset_reference.dataset_id` | Confirm the final request shape and whether the identifier is required. |
| Example request | `{ "dataset_reference": { "dataset_id": "dataset_001" } }` | Illustrative example, not a finalized payload. |
| Metadata lookup | Example `DatasetMetadata` table includes `DatasetID`, `DatasetName`, `FilePath`, `FileFormat`, and `CreatedDate` | Confirm actual table/schema, identifier uniqueness, and who owns lookup. |
| File access | A file path stored in SQL Server does not itself make a file readable as a SQL table | Backend needs an agreed file-reading or ingestion mechanism; confirm how Team 1 receives data. |
| Statuses | `success`, `warning`, `failed` | Team 2 verbally described these statuses too; exact meanings and fields still need approval. |
| Warning/error details | Structured objects with a code, message, and optional affected field | Confirm exact response schema, error-code catalogue, severity, and HTTP status mapping. |
| File size and formats in document | Proposed 50 MB; CSV, XLSX, JSON, and Parquet | Conflicts with Team 2's verbal clarification below. Must be resolved before changing the validator. |
| Verbal clarification from Team 2 | User reports Team 2 said CSV only and 10 MB | Treat as verbally communicated guidance, not a final written contract until Team 2 confirms it in writing. |
| Authentication and authorization | Not finalized in the available details | Confirm authentication, dataset access checks, and storage-reference authorization. |
| Test environment | No confirmed endpoint/test dataset available in current notes | Request endpoint, sample request/response, test dataset, and access instructions. |

## 3. Comparison with Team 5's Current Work

| Team 5 area | Current state | Required follow-up |
|---|---|---|
| CSV validation | Python prototype supports CSV; provisional 10 MB limit | Keep CSV/10 MB as provisional guidance until written confirmation; do not add formats based only on the proposal. |
| Dataset ID | Existing comparison lists `dataset_reference.dataset_id` as the draft identifier | Confirm whether this exact nesting is approved. |
| Storage reference | Existing notes list `location` as optional in an earlier draft | Clarify whether `location` remains in the contract, how it relates to `dataset_id`, and which component resolves it. |
| Validation outcomes | Local validator produces structured findings | Map findings to Team 2's final response fields after the schema is confirmed. |
| API statuses | `success`, `warning`, `failed` are described by Team 2 | Confirm whether these describe profiling overall, validation, or processing; avoid collapsing distinct outcomes. |
| Processing handoff | Team 1's receiving interface remains unconfirmed in current notes | Ask whether Team 1 expects a DataFrame, dataset ID, storage reference, or another payload. |
| Error handling | Safe structured errors are proposed | Confirm error codes and HTTP statuses; do not expose cell values, credentials, or internal storage paths. |
| Integration tests | No confirmed endpoint/schema to test against yet | Write/run contract tests once Team 2 shares the actual interface. |

## 4. Important Discrepancy: File Size and Formats

There are two different statements:

- **Shared document proposal:** maximum 50 MB; CSV, XLSX, JSON, and Parquet.
- **Verbal clarification reported from Team 2:** CSV only; maximum 10 MB.

**Decision needed:** Team 2 should confirm the currently approved formats and file-size limit in writing. Until then, Team 5 should not change the prototype to support more formats or raise the limit based only on the proposal.

## 5. Suggested End-to-End Flow (Not Yet Approved)

1. API receives the agreed dataset identifier and any approved source/reference fields.
2. Backend resolves the dataset identifier through the approved metadata lookup.
3. Backend verifies authorization and safely resolves the underlying file reference.
4. The agreed validation component checks readability, CSV structure, required columns, and configured rules.
5. A hard validation failure stops processing; warning behavior follows agreed severity rules.
6. If accepted, the dataset is handed to Team 1 using the confirmed interface.
7. Validation and processing outcomes are recorded distinctly if the contract supports separate fields.
8. API returns the approved response schema without exposing sensitive data or internal storage paths.

This is a proposed integration flow for discussion, not a claim that the endpoint or pipeline is deployed.

## 6. Example Scenarios to Agree Across Teams

### A. Success
- Dataset ID resolves to an accessible CSV.
- CSV passes validation.
- Team 1 receives the dataset through the agreed handoff.
- Processing succeeds.
- API returns the approved success response.

### B. Validation failure
- Dataset resolves, but the CSV is malformed or a required column is missing.
- Validation returns a structured, safe finding.
- Processing does not start.
- API returns the agreed failure status and error code.

### C. Warning
- Dataset passes hard validation but contains a data-quality issue classified as a warning.
- Team leads must decide whether processing continues.
- The warning remains visible in the agreed response/result record.

### D. Processing failure
- Dataset passes validation, but Team 1's processing operation fails.
- Validation success must not be overwritten or misreported as a validation failure.
- Processing failure is returned using the approved status and error schema.

## 7. Questions to Send to Team 2

1. Is `POST /api/v1/datasets/profile` the actual endpoint, or only a proposal? Please share the final path, method, and environment.
2. Please share the approved request and response schemas, including required/optional fields and one success, warning, and failure example.
3. Please confirm in writing: is the current limit 10 MB with CSV only, or 50 MB with CSV/XLSX/JSON/Parquet?
4. Is `dataset_reference.dataset_id` the final request field? How is it resolved to metadata and a file reference?
5. What are the exact meanings of `success`, `warning`, and `failed`? Does `failed` refer to validation, profiling, or processing?
6. Please share final error codes, severity rules, and HTTP status mapping.
7. What authentication is required, and which component validates dataset access and storage references?
8. Can you provide a test dataset and instructions for testing the endpoint?

## 8. Questions to Send to Team 1

1. What exact input does the processing service receive: a DataFrame, dataset ID, storage reference, file path, or API payload?
2. What response/status fields does the service return?
3. How should processing failure be represented separately from validation failure?
4. Are there constraints on file location, file format, or access permissions?
5. Is there a sample payload or interface document for integration tests?

## 9. Current Decision Log

| Item | Current status | Owner / next action |
|---|---|---|
| Actual endpoint and environment | Open | Team 2 to confirm |
| Approved request/response schema | Open | Team 2 to share |
| File size and supported formats | Conflicting information | Team 2 to confirm in writing |
| Dataset ID lookup and metadata schema | Open | Team 2 / database owner to confirm |
| Authentication and storage authorization | Open | Relevant backend/team lead to assign |
| Status meanings and error mapping | Open | Team 2 and relevant team leads to agree |
| Processing handoff | Open | Team 1 to confirm |
| Test dataset and integration access | Open | Team 2 / Team 1 to provide |
| Contract and end-to-end tests | Blocked on interface confirmation | Team 5 to implement after confirmation |

## 10. Work Completed and Remaining

**Completed**
- Existing contract comparison and lifecycle notes reviewed.
- Team 2's proposed endpoint and status terms captured.
- The discrepancy between the document's proposed 50 MB/multiple-format scope and the verbally reported CSV-only/10 MB guidance recorded.
- Success, validation-failure, warning, and processing-failure scenarios outlined.

**Remaining**
- Obtain written confirmation of endpoint, request/response schemas, formats, size limit, statuses, errors, and authentication.
- Obtain Team 1's processing interface.
- Update existing contract comparison and lifecycle documents based on confirmed decisions.
- Add contract/integration tests once the interface is available.
- Re-run unit tests and `git diff --check` after local changes.

## 11. Source and Confidence Notes

- **From Team 2's shared document:** proposed endpoint, example request, example metadata table, proposed statuses, structured errors, and proposed 50 MB/four-format scope.
- **Reported verbally by the user from the Team 2 discussion:** statuses `success`, `warning`, `failed`; CSV only; 10 MB limit; endpoint details/docs expected later.
- **Not yet confirmed:** production endpoint, final schemas, authentication, final format/size rules, exact status/error mapping, and Team 1's handoff.
