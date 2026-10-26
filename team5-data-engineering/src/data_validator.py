
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


def validate_csv(file_path, required_columns=None, expected_types=None):
    """Validate CSV structure and basic data quality."""

    result = {
        "file": str(file_path),
        "status": "PASS",
        "rules": [],
        "row_count": 0,
        "column_count": 0,
        "empty_columns": [],
        "missing_value_count": 0,
        "duplicate_row_count": 0,
        "invalid_type_count": 0,
        "findings": [],
    }

    def add_rule(name, status, summary, message):
        result["rules"].append({
            "rule": name,
            "rule_name": name,
            "status": status,
            "summary": summary,
            "actionable_message": message,
            "message": message,  # Backward compatibility
        })

    def fail(name, summary, message):
        result["status"] = "FAIL"
        add_rule(name, "FAIL", summary, message)

    def add_finding(name, status, summary, message, **details):
        result["findings"].append({
            "rule": name,
            "rule_name": name,
            "status": status,
            "summary": summary,
            "actionable_message": message,
            "message": message,
            **details,
        })

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

        with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
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
            supported_types = {"integer", "number"}

            unsupported = {
                c: t for c, t in expected_types.items()
                if t not in supported_types
            }
            if unsupported:
                fail(
                    "expected_types",
                    "Unsupported data type configuration.",
                    f"Use only integer or number. Invalid settings: {unsupported}"
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
                            f"Row {row_number}, column '{column}': "
                            f"expected {expected_type}, received '{value}'."
                        )
                        add_finding(
                            "data_types", "WARNING",
                            "Value does not match the expected data type.",
                            message,
                            row=row_number,
                            column=column,
                            value=value,
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

    except (OSError, UnicodeError, csv.Error) as error:
        fail(
            "csv_readable",
            "CSV could not be read.",
            f"Check file access and CSV formatting. Details: {error}"
        )

    return result
