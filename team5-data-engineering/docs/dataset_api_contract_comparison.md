# Dataset API Contract Comparison

**Owner:** Sandeep — Data/API Integration
**Date:** 28 October 2026
**Status:** Draft — pending team confirmation

## 1. Objective

Compare the dataset metadata and validation contract with Team 2's API request and response models and Team 1's processing interface.

## 2. Contract Comparison

| Area | Current Understanding | Confirmation Required |
|---|---|---|
| Dataset identifier | `dataset_reference.dataset_id` is required in Team 2's draft | Confirm how the identifier is resolved |
| Source type | Draft supports `source_type="file"` | Confirm supported source types |
| Storage reference | `location` is optional in the draft | Confirm how the storage reference is resolved and authorized |
| Data handoff | Profiling function can accept a DataFrame | Confirm how Team 1 receives the dataset |
| Validation outcomes | Local validator produces structured outcomes | Agree on status mapping |
| Profiling statuses | Draft defines `success`, `warning`, and `failed` | Confirm final status definitions |
| Error response | Structured errors are proposed | Confirm error codes and response schema |
| File formats | Current validator supports CSV | Confirm whether additional formats are in scope |
| File size | Current prototype default is 10 MB | Confirm whether the proposed 50 MB limit is approved |
| Security | Storage references must be handled safely | Confirm ownership of authorization and path validation |

## 3. Example Scenarios

### Scenario A — Successful Processing

**Input:** A valid CSV containing all required columns and valid data types.

**Expected behavior:**
- Validation succeeds.
- The correct authorized dataset is passed to processing.
- Processing completes successfully.
- The final outcome follows the agreed contract.

### Scenario B — Validation Failure

**Input:** A malformed CSV or a CSV missing a required column.

**Expected behavior:**
- Validation rejects the input.
- Processing does not run on the rejected dataset.
- A structured, actionable validation error is returned.
- Sensitive values and internal storage paths are not exposed.

### Scenario C — Processing Failure

**Input:** A valid CSV passes validation, but a downstream processing operation fails.

**Expected behavior:**
- Validation success remains recorded separately.
- Processing is marked as failed.
- A safe error is returned.
- The dataset is not reported as fully processed.

## 4. Open Interface Questions

1. Is Team 2's latest contract approved or still a draft?
2. How is `dataset_id` resolved to the underlying dataset?
3. How does Team 1 receive the dataset: a DataFrame, a storage reference, or an API response?
4. Which component owns dataset authorization and storage-path validation?
5. What are the agreed definitions of validation success, warning, validation failure, and processing failure?
6. Are the proposed 50 MB limit and additional file formats approved?
7. What are the final response fields and error codes?

## 5. Decisions and Dependencies

| Question | Responsible Team | Decision | Status |
|---|---|---|---|
| Dataset ID resolution | To be confirmed | Pending | Open |
| Storage reference and authorization | To be confirmed | Pending | Open |
| Status and error mapping | Relevant team leads | Pending | Open |
| File format and size requirements | Team 2 / relevant lead | Pending | Open |
| Processing handoff | Team 1 / Team 2 | Pending | Open |

## 6. Testing Evidence

- Existing CSV validator unit tests: 16 tests passed in the last confirmed run.
- Contract integration tests: Pending confirmation of the final interface.
- End-to-end integration: Not yet verified.

## 7. Limitations

This document records the currently available draft information. Proposed requirements and interface assumptions must not be treated as approved until confirmed by the relevant team leads.

## 8. Proposed Dataset Identifier and Processing Flow

The following flow is a proposed integration model. The actual handoff between Team 2 and Team 1 must be confirmed.

1. **Dataset submission:** The API receives a dataset identifier and source information.
2. **Dataset resolution:** The responsible backend component resolves the dataset ID to an authorized dataset reference.
3. **Input validation:** The validation component checks the file structure, required columns, and configured data-quality rules.
4. **Validation decision:** The system determines whether the dataset is accepted, rejected, or accepted with warnings according to the agreed rules.
5. **Processing handoff:** Only an accepted dataset is passed to Team 1's processing service using the agreed interface.
6. **Processing result:** The processing service reports success or failure separately from the validation result.
7. **Metadata update:** The agreed metadata store or API records the relevant validation and processing outcomes.

### Integration Questions

- Which component resolves `dataset_id`?
- Does the processing service receive a DataFrame, a storage reference, or another payload?
- How is dataset ownership and access authorization checked?
- Where are validation and processing statuses persisted?
- How are processing failures reported without overwriting the original validation outcome?

## 9. Proposed Status Mapping

The following mapping is a proposal for team review, not an approved shared contract.

| Situation | Validation Outcome | Processing Outcome | Expected Behavior |
|---|---|---|---|
| Valid dataset; processing succeeds | Success | Success | Report successful completion |
| Dataset has warnings and is accepted under agreed rules | Warning | Pending, then success or failure | Preserve warnings and record processing separately |
| Required column missing | Failed | Not started | Return validation findings and stop processing |
| CSV is malformed or unreadable | Failed | Not started | Return a safe validation error |
| Validation succeeds but processing fails | Success | Failed | Preserve validation success and report processing failure |
| Dataset access is denied | Access failure to be defined | Not started | Reject access without exposing internal paths |

### Status Decisions Required

1. Confirm whether `warning` is an accepted validation outcome or a general profiling status.
2. Confirm whether validation failure uses `failed` or a distinct status.
3. Define how access-denied and missing-dataset errors are represented.
4. Confirm whether validation and processing statuses are separate fields.
5. Agree on the final status names and error codes across teams.

## 10. Example Integration Scenarios

**Note:** The examples below are illustrative test scenarios, not finalized API payloads. Field names and response schemas must be confirmed with Team 1 and Team 2.

### Scenario A — Successful Validation and Processing

**Test input:** A readable CSV containing the required columns and valid values.

**Example input description:**

```json
{
  "dataset_id": "example-dataset-001",
  "source_type": "file"
}
```

**Expected behavior:**
1. Resolve the dataset ID using the approved dataset lookup mechanism.
2. Verify the caller's authorization to access the dataset.
3. Validate the CSV successfully.
4. Pass the accepted dataset to the processing service.
5. Record successful processing separately from validation.

**Expected outcome:** Validation succeeds, processing succeeds, and the dataset is reported as successfully processed.

### Scenario B — Validation Failure

**Test input:** A CSV is missing a required column, such as `employee_id`.

**Example finding:**

```json
{
  "rule": "missing_required_column",
  "status": "failed",
  "summary": "A required column is missing.",
  "actionable_message": "Include the required employee_id column and retry."
}
```

**Expected behavior:**
1. Validation identifies the missing column.
2. The dataset is rejected according to the agreed validation rules.
3. Processing is not started.
4. The caller receives a safe, actionable validation error.

**Expected outcome:** Validation fails and processing remains not started.

### Scenario C — Processing Failure After Successful Validation

**Test input:** A valid CSV passes validation, but a downstream processing operation fails.

**Illustrative outcome:**

```json
{
  "validation_status": "success",
  "processing_status": "failed",
  "error": {
    "code": "PROCESSING_FAILED",
    "message": "The dataset could not be processed. Please retry or contact support."
  }
}
```

**Expected behavior:**
1. Validation success is retained.
2. The processing service reports the failure.
3. The error response does not expose sensitive data, credentials, or internal storage paths.
4. The dataset is not marked as successfully processed.

**Expected outcome:** Validation succeeds, processing fails, and both outcomes remain distinguishable.

**Contract dependency:** The example field names and error code above are illustrative and must not be treated as approved API fields or codes.

## 11. Verification Checklist

- [ ] Compare request fields with Team 2's latest approved request model.
- [ ] Compare response fields with Team 2's latest approved response model.
- [ ] Confirm the dataset identifier and storage-reference resolution flow.
- [ ] Confirm the processing handoff with Team 1.
- [ ] Agree on validation and processing status definitions.
- [ ] Confirm error codes and warning behavior.
- [ ] Run contract tests after the interface is confirmed.
- [ ] Record team-lead decisions and update this document.