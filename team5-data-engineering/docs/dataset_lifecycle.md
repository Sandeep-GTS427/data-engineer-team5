# Dataset Lifecycle and Safe Processing

## 1. Purpose

Define how uploaded datasets move through raw input, validation, and processing while preventing invalid inputs from being processed unintentionally.

## 2. Lifecycle Stages

### Stage 1: Raw Input
- Receive the uploaded dataset.
- Preserve the original input without silently modifying it.
- Check the configured file-size limit and supported format.
- Do not expose internal storage paths or sensitive data in user-facing responses.

### Stage 2: Validation
- Validate file readability, structure, required columns, and configured data-quality rules.
- Reject structurally invalid inputs with safe, actionable error messages.
- Report data-quality warnings separately from hard failures.
- Record the validation outcome and relevant findings.

### Stage 3: Validated Dataset
- Allow processing only after the dataset satisfies the agreed acceptance rules.
- Keep validation results distinguishable from the original uploaded file.
- Do not treat a dataset with warnings as accepted or rejected until the project's severity rules define that behavior.

### Stage 4: Processed Output
- Create processed output only after successful validation and processing.
- Keep processed output distinguishable from raw input and validated data.
- Record processing status and relevant metadata when the metadata contract is confirmed.

## 3. Proposed Upload Contract

Team 2 has proposed the following requirements, pending final confirmation:

- Maximum file size: 50 MB per file.
- Supported formats: CSV, XLSX, JSON, and Parquet.
- The backend independently validates uploaded files.
- Invalid files receive structured error responses.

The current Python prototype validates CSV only and has a provisional 10 MB default. The prototype must be aligned with the final contract before production integration.

## 4. Open Decisions

- Confirm the final file-size limit and supported formats with Team 2.
- Confirm which validation findings cause rejection versus warnings.
- Confirm dataset metadata fields and lifecycle status names.
- Confirm storage references and access-control expectations.
- Confirm how validation and processing results are represented in the API.
- Confirm retention and cleanup expectations for raw files and failed uploads.

## 5. Current Implementation Status

The CSV validation prototype has automated tests for file handling, CSV structure, data quality, file-size limits, malformed quoting, invalid encoding, and structured findings.

A complete upload-to-processing pipeline, storage lifecycle, API integration, and support for XLSX, JSON, and Parquet are not established by these tests and require separate implementation and verification.
