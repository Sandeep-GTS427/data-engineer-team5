import csv
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


def is_missing(value):
    """Treat empty and whitespace-only cells as missing."""
    return value is None or value.strip() == ""


def detect_value_type(value):
    """Detect the basic type of one non-empty CSV value."""
    value = value.strip()

    # Boolean
    if value.lower() in {"true", "false"}:
        return "boolean"

    # Integer
    try:
        int(value)
        return "integer"
    except ValueError:
        pass

    # Decimal
    try:
        number = Decimal(value)
        if number.is_finite():
            return "decimal"
    except InvalidOperation:
        pass

    # Date
    try:
        date.fromisoformat(value)
        return "date"
    except ValueError:
        pass

    # Timestamp
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return "timestamp"
    except ValueError:
        pass
    
    return "string"

def determine_column_type(values):
    """Determine the overall data type of a column."""
    detected_types = {
        detect_value_type(value)
        for value in values
        if not is_missing(value)
    }

    if not detected_types:
        return "unknown"

    # Integer and decimal values can share a decimal type.
    if detected_types.issubset({"integer", "decimal"}):
        return (
            "integer"
            if detected_types == {"integer"}
            else "decimal"
        )

    # Date and timestamp values can share a timestamp type.
    if detected_types.issubset({"date", "timestamp"}):
        return (
            "date"
            if detected_types == {"date"}
            else "timestamp"
        )

    if len(detected_types) == 1:
        return next(iter(detected_types))

    return "mixed"


def convert_numeric_value(value):
    """Convert a numeric string into a JSON-friendly number."""
    number = Decimal(value.strip())

    if number == number.to_integral_value():
        return int(number)

    return float(number)


def get_column_min_max(values, data_type):
    """Calculate minimum and maximum for supported column types."""
    non_missing_values = [
        value.strip()
        for value in values
        if not is_missing(value)
    ]

    if not non_missing_values:
        return None, None

    if data_type in {"integer", "decimal"}:
        numbers = [
            convert_numeric_value(value)
            for value in non_missing_values
        ]
        return min(numbers), max(numbers)

    if data_type in {"date", "timestamp"}:
        parsed_values = []

        for value in non_missing_values:
            if data_type == "date":
                parsed_values.append(date.fromisoformat(value))
            else:
                parsed_values.append(
                    datetime.fromisoformat(
                        value.replace("Z", "+00:00")
                    )
                )

        return (
            min(parsed_values).isoformat(),
            max(parsed_values).isoformat()
        )

    return None, None


def profile_csv(file_path):
    """
    Generate dataset-level and column-level profiling statistics.

    Returns:
        Dictionary containing row count, column count and column statistics.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path.name}")

    columns_data = {}

    try:
        with path.open(
            mode="r",
            encoding="utf-8-sig",
            newline=""
        ) as csv_file:

            reader = csv.reader(csv_file, strict=True)

            headers = next(reader, None)

            if not headers:
                raise ValueError("CSV file is empty or has no header.")

            if any(not header.strip() for header in headers):
                raise ValueError("CSV contains an empty column name.")

            if len(headers) != len(set(headers)):
                raise ValueError("CSV contains duplicate column names.")

            columns_data = {header: [] for header in headers}

            row_count = 0

            for row in reader:

                if len(row) != len(headers):
                    raise ValueError(
                        f"Malformed CSV row at line {reader.line_num}: "
                        f"expected {len(headers)} values, found {len(row)}."
                    )

                row_count += 1

                for index, header in enumerate(headers):
                    columns_data[header].append(row[index])

    except csv.Error as error:
        raise ValueError(f"Unable to parse CSV file: {error}") from error

    column_profiles = []

    for column_name, values in columns_data.items():

        non_missing_values = [
            value.strip()
            for value in values
            if not is_missing(value)
        ]

        null_count = len(values) - len(non_missing_values)

        null_pct = (
            null_count / row_count
            if row_count > 0
            else 0.0
        )

        data_type = determine_column_type(non_missing_values)

        minimum, maximum = get_column_min_max(
            non_missing_values,
            data_type
        )

        column_profiles.append({
            "name": column_name,
            "data_type": data_type,
            "null_count": null_count,
            "null_pct": round(null_pct, 4),
            "distinct_count": len(set(non_missing_values)),
            "min": minimum,
            "max": maximum
        })

    return {
        "row_count": row_count,
        "column_count": len(columns_data),
        "columns": column_profiles
    }