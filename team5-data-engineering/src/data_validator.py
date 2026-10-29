
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


def validate_csv(
    file_path,
    required_columns=None,
    expected_types=None,
    max_file_size_mb=10,  # Temporary prototype default
):
    
    """Validate CSV structure and basic data quality."""

    result = {
        "file": Path(file_path).name,
        "status": "PASS",
        "rules": [],
        "row_count": 0,
        "column_count": 0,
        "empty_columns": [],
        "missing_value_count": 0,
        "duplicate_row_count": 0,
        "invalid_type_count": 0,
        "findings": [],
        "api_status": "success",
    }

    def add_rule(name, status, summary, message):
        if status == "WARNING" and result["api_status"] == "success":
            result["api_status"] = "warning"

        result["rules"].append({
            "code": name.upper(),
            "rule": name,
            "rule_name": name,
            "status": status,
            "summary": summary,
            "actionable_message": message,
            "message": message,  # Backward compatibility
        })

    def fail(name, summary, message):
        result["status"] = "FAIL"
        result["api_status"] = "failed"

        add_rule(name, "FAIL", summary, message)

    
    def add_finding(name, status, summary, message, **details):
        if status == "WARNING" and result["api_status"] == "success":
            result["api_status"] = "warning"

        finding = {
            "code": name.upper(),
            "rule": name,
            "rule_name": name,
            "status": status,
            "summary": summary,
            "message": message,
            "actionable_message": message,
        }

        # Include the affected field when a column is available.
        if details.get("column"):
            finding["field"] = details["column"]

        # Preserve existing details such as row and column.
        finding.update(details)

        result["findings"].append(finding)

    path = Path(file_path)

    if not path.is_file():
        fail(
            "file_exists",
            "CSV file was not found.",
            "Check the file path and ensure the CSV exists."
        )
        return result

    try:
        if path.stat().st_size == 0:
            fail(
                "non_empty_file",
                "CSV file is empty.",
                "Provide a CSV containing a header and data rows."
            )
            return result
        max_file_size_bytes = max_file_size_mb * 1024 * 1024

        if path.stat().st_size > max_file_size_bytes:
            fail(
                "file_size_limit",
                "CSV file exceeds the configured size limit.",
                f"Upload a CSV smaller than or equal to "
                f"{max_file_size_mb} MB."
            )
            return result
        with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file,strict=True)
            columns = reader.fieldnames

            if not columns or not any(c and c.strip() for c in columns):
                fail(
                    "valid_header",
                    "CSV header is missing or invalid.",
                    "Add a valid header row with column names."
                )
                return result

            if any(not c or not c.strip() for c in columns):
                fail(
                    "valid_header",
                    "CSV contains an empty column name.",
                    "Give every column a non-empty name."
                )
                return result

            if len(set(columns)) != len(columns):
                fail(
                    "unique_column_names",
                    "CSV contains duplicate column names.",
                    "Rename duplicate columns so every name is unique."
                )
                return result

            result["column_count"] = len(columns)
            add_rule(
                "valid_header", "PASS",
                "CSV header is valid.",
                "No action required."
            )

            expected_types = expected_types or {}
            supported_types = {"integer", "number","string"}

            unsupported = {
                c: t for c, t in expected_types.items()
                if t not in supported_types
            }
            if unsupported:
                fail(
                    "expected_types",
                    "Unsupported data type configuration.",
                    f"Use only integer, number, or string. Invalid settings: {unsupported}"
                )
                return result

            unknown_columns = [
                c for c in expected_types if c not in columns
            ]
            if unknown_columns:
                fail(
                    "expected_type_columns",
                    "Type rules reference missing columns.",
                    "Correct the type configuration for: "
                    + ", ".join(unknown_columns)
                )
                return result

            missing_columns = [
                c for c in (required_columns or []) if c not in columns
            ]
            if missing_columns:
                fail(
                    "required_columns",
                    "Required columns are missing.",
                    "Add these required columns: " + ", ".join(missing_columns)
                )
            else:
                add_rule(
                    "required_columns", "PASS",
                    "All required columns are present.",
                    "No action required."
                )

            seen_rows = set()
            missing_count = 0
            duplicate_count = 0
            invalid_count = 0
            blank_counts = {column: 0 for column in columns}

            for row_number, row in enumerate(reader, start=2):
                if None in row:
                    fail(
                        "consistent_column_count",
                        f"Row {row_number} has extra values.",
                        "Correct the row so its number of values matches the header."
                    )
                    return result

                values = [row.get(column) for column in columns]

                if any(value is None for value in values):
                    fail(
                        "consistent_column_count",
                        f"Row {row_number} has fewer values than the header.",
                        "Provide a value or an empty field for every column."
                    )
                    return result

                result["row_count"] += 1

                for column, value in zip(columns, values):
                    if not value.strip():
                        missing_count += 1
                        blank_counts[column] += 1

                row_key = tuple(value.strip() for value in values)
                if row_key in seen_rows:
                    duplicate_count += 1
                else:
                    seen_rows.add(row_key)

                for column, expected_type in expected_types.items():
                    value = row[column].strip()
                    if not value:
                        continue

                    
                    try:
                        if expected_type == "string":
                            # CSV values are strings; reject empty values here
                            if not value.strip():
                                raise ValueError("Value must not be empty.")

                        elif expected_type in {"integer", "number"}:
                            number = Decimal(value)

                            if not number.is_finite():
                                raise ValueError("Value must be finite.")

                            if (
                                expected_type == "integer"
                                and number != number.to_integral_value()
                            ):
                                raise ValueError("Value must be an integer.")

                    except (InvalidOperation, ValueError):
                        invalid_count += 1
                        message = (
                            f"Row {row_number}, column '{column}' contains an invalid value. "
                            f"Expected type: {expected_type}. Please correct the value."
                        )
                        add_finding(
                            "data_types", "WARNING",
                            "Value does not match the expected data type.",
                            message,
                            row=row_number,
                            column=column,
                        )

            result["missing_value_count"] = missing_count
            result["duplicate_row_count"] = duplicate_count
            result["invalid_type_count"] = invalid_count

            if result["row_count"] == 0:
                fail(
                    "data_rows_present",
                    "CSV has a header but no data rows.",
                    "Add at least one data row."
                )
                return result

            add_rule(
                "data_rows_present", "PASS",
                f"Found {result['row_count']} data rows.",
                "No action required."
            )

            empty_columns = [
                column for column, count in blank_counts.items()
                if count == result["row_count"]
            ]
            result["empty_columns"] = empty_columns

            if empty_columns:
                message = (
                    "Populate these columns or confirm that empty columns "
                    "are allowed: " + ", ".join(empty_columns)
                )
                add_rule(
                    "empty_columns", "WARNING",
                    f"Found {len(empty_columns)} columns with no non-empty values.",
                    message
                )
                add_finding(
                    "empty_columns", "WARNING",
                    "Column contains no non-empty values.",
                    message,
                    columns=empty_columns,
                )
            else:
                add_rule(
                    "empty_columns", "PASS",
                    "Every column contains at least one non-empty value.",
                    "No action required."
                )

            if missing_count:
                add_rule(
                    "missing_values", "WARNING",
                    f"Found {missing_count} blank or whitespace-only cells.",
                    "Review missing values and confirm which fields are mandatory."
                )

                for column, count in blank_counts.items():
                    if count > 0:
                        add_finding(
                            "missing_values", "WARNING",
                            f"Found {count} missing value(s) in column '{column}'.",
                            f"Review the missing values in column '{column}'.",
                            column=column,
                            count=count
                        )
            else:
                add_rule(
                    "missing_values", "PASS",
                    "No missing values found.",
                    "No action required."
                )

            if duplicate_count:
                add_rule(
                    "duplicate_rows", "WARNING",
                    f"Found {duplicate_count} duplicate rows.",
                    "Review duplicate records and remove them only if the business rules require it."
                )

                add_finding(
                    "duplicate_rows", "WARNING",
                    f"Found {duplicate_count} duplicate rows.",
                    "Review the duplicate records and remove them only if required.",
                    count=duplicate_count
                )
            else:
                add_rule(
                    "duplicate_rows", "PASS",
                    "No duplicate rows found.",
                    "No action required."
                )

            if invalid_count:
                add_rule(
                    "data_types", "WARNING",
                    f"Found {invalid_count} values with invalid types.",
                    "Correct the flagged values or confirm the expected column types."
                )
            elif expected_types:
                add_rule(
                    "data_types", "PASS",
                    "All non-empty values match configured data types.",
                    "No action required."
                )

    except (OSError, UnicodeError, csv.Error):
        fail(
        "csv_readable",
        "CSV could not be read.",
        "Check that the file is accessible, correctly encoded, "
        "and follows the required CSV format."
    )

    return result
