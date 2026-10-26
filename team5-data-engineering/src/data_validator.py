
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
        "missing_value_count": 0,
        "duplicate_row_count": 0,
        "invalid_type_count": 0,
        "findings": [],
    }

    def add_rule(name, status, message):
        result["rules"].append({
            "rule": name,
            "status": status,
            "message": message,
        })

    def fail(name, message):
        result["status"] = "FAIL"
        add_rule(name, "FAIL", message)

    path = Path(file_path)

    # 1. Check file existence
    if not path.is_file():
        fail("file_exists", "The specified file does not exist.")
        return result

    # 2. Check for an empty file
    try:
        if path.stat().st_size == 0:
            fail("non_empty_file", "The CSV file is empty.")
            return result
    except OSError as error:
        fail("file_readable", f"Unable to access file: {error}")
        return result

    try:
        with path.open(
            "r", newline="", encoding="utf-8-sig"
        ) as csv_file:

            reader = csv.DictReader(csv_file)
            columns = reader.fieldnames

            # 3. Validate header
            if not columns or not any(
                column and column.strip() for column in columns
            ):
                fail("valid_header", "The CSV has no valid header.")
                return result

            if any(
                not column or not column.strip()
                for column in columns
            ):
                fail(
                    "valid_header",
                    "The CSV contains an empty column name."
                )
                return result

            if len(set(columns)) != len(columns):
                fail(
                    "unique_column_names",
                    "The CSV contains duplicate column names."
                )
                return result

            result["column_count"] = len(columns)
            add_rule("valid_header", "PASS", "Header is valid.")

            # 4. Validate type configuration
            expected_types = expected_types or {}
            supported_types = {"integer", "number"}

            unsupported_types = {
                column: kind
                for column, kind in expected_types.items()
                if kind not in supported_types
            }

            if unsupported_types:
                fail(
                    "expected_types",
                    f"Unsupported expected types: {unsupported_types}"
                )
                return result

            unknown_type_columns = [
                column for column in expected_types
                if column not in columns
            ]

            if unknown_type_columns:
                fail(
                    "expected_type_columns",
                    "Type rules refer to missing columns: "
                    + ", ".join(unknown_type_columns)
                )
                return result

            # 5. Check required columns
            missing_columns = [
                column for column in (required_columns or [])
                if column not in columns
            ]

            if missing_columns:
                fail(
                    "required_columns",
                    "Missing required columns: "
                    + ", ".join(missing_columns)
                )
            else:
                add_rule(
                    "required_columns",
                    "PASS",
                    "All required columns are present."
                )

            seen_rows = set()
            missing_count = 0
            duplicate_count = 0
            invalid_type_count = 0

            # 6. Validate data rows
            for row_number, row in enumerate(reader, start=2):

                if None in row:
                    fail(
                        "consistent_column_count",
                        f"Row {row_number} has more values than the header."
                    )
                    return result

                values = [row.get(column) for column in columns]

                if any(value is None for value in values):
                    fail(
                        "consistent_column_count",
                        f"Row {row_number} has fewer values than the header."
                    )
                    return result

                result["row_count"] += 1

                # 7. Count missing values
                missing_count += sum(
                    1 for value in values if not value.strip()
                )

                # 8. Detect duplicate complete rows
                row_key = tuple(value.strip() for value in values)

                if row_key in seen_rows:
                    duplicate_count += 1
                else:
                    seen_rows.add(row_key)

                # 9. Validate configured data types
                for column, expected_type in expected_types.items():
                    value = row[column].strip()

                    # Missing values are handled by the separate rule.
                    if not value:
                        continue

                    try:
                        number = Decimal(value)

                        if not number.is_finite():
                            raise ValueError("Number must be finite.")

                        if (
                            expected_type == "integer"
                            and number != number.to_integral_value()
                        ):
                            raise ValueError("Value must be an integer.")

                    except (InvalidOperation, ValueError):
                        invalid_type_count += 1

                        result["findings"].append({
                            "rule": "data_types",
                            "row": row_number,
                            "column": column,
                            "value": value,
                            "status": "WARNING",
                            "message": (
                                f"Expected {expected_type} "
                                f"but received '{value}'."
                            ),
                        })

            result["missing_value_count"] = missing_count
            result["duplicate_row_count"] = duplicate_count
            result["invalid_type_count"] = invalid_type_count

            # 10. Check for data rows
            if result["row_count"] == 0:
                fail(
                    "data_rows_present",
                    "The CSV has a header but no data rows."
                )
            else:
                add_rule(
                    "data_rows_present",
                    "PASS",
                    f"Found {result['row_count']} data rows."
                )

            # 11. Report missing values
            if missing_count:
                add_rule(
                    "missing_values",
                    "WARNING",
                    f"Found {missing_count} blank or whitespace-only cells."
                )
            else:
                add_rule(
                    "missing_values",
                    "PASS",
                    "No missing values found."
                )

            # 12. Report duplicate rows
            if duplicate_count:
                add_rule(
                    "duplicate_rows",
                    "WARNING",
                    f"Found {duplicate_count} duplicate rows."
                )
            else:
                add_rule(
                    "duplicate_rows",
                    "PASS",
                    "No duplicate rows found."
                )

            # 13. Report type validation
            if invalid_type_count:
                add_rule(
                    "data_types",
                    "WARNING",
                    f"Found {invalid_type_count} values with invalid types."
                )
            elif expected_types:
                add_rule(
                    "data_types",
                    "PASS",
                    "All non-empty values match configured data types."
                )

    except (OSError, UnicodeError, csv.Error) as error:
        fail("csv_readable", f"Unable to read CSV: {error}")

    return result
