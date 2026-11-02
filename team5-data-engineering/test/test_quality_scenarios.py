
import unittest
from pathlib import Path

from src.data_validator import validate_csv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATA_DIR = PROJECT_ROOT / "data" / "test_samples"

EXPECTED_TYPES = {
    "customer_id": "integer",
    "name": "string",
    "age": "integer"
}

REQUIRED_COLUMNS = ["customer_id", "name", "age"]


class TestQualityScenarios(unittest.TestCase):

    def test_missing_values(self):
        file_path = TEST_DATA_DIR / "customers_missing.csv"

        result = validate_csv(
            file_path,
            required_columns=REQUIRED_COLUMNS,
            expected_types=EXPECTED_TYPES
        )

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["api_status"], "warning")
        self.assertEqual(result["missing_value_count"], 2)

        findings = {
            finding["column"]: finding["count"]
            for finding in result["findings"]
            if finding["rule"] == "missing_values"
        }

        self.assertEqual(findings, {"name": 1, "age": 1})

    def test_duplicate_rows(self):
        file_path = TEST_DATA_DIR / "customers_duplicates.csv"

        result = validate_csv(
            file_path,
            required_columns=REQUIRED_COLUMNS,
            expected_types=EXPECTED_TYPES
        )

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["api_status"], "warning")
        self.assertEqual(result["duplicate_row_count"], 1)

        duplicate_findings = [
            finding for finding in result["findings"]
            if finding["rule"] == "duplicate_rows"
        ]

        self.assertEqual(len(duplicate_findings), 1)
        self.assertEqual(duplicate_findings[0]["count"], 1)

    def test_invalid_data_types(self):
        file_path = TEST_DATA_DIR / "customers_invalid_types.csv"

        result = validate_csv(
            file_path,
            required_columns=REQUIRED_COLUMNS,
            expected_types=EXPECTED_TYPES
        )

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["api_status"], "warning")
        self.assertEqual(result["invalid_type_count"], 2)

        invalid_findings = [
            finding for finding in result["findings"]
            if finding["rule"] == "data_types"
        ]

        actual_errors = [
            (finding["row"], finding["column"])
            for finding in invalid_findings
        ]

        self.assertEqual(
            actual_errors,
            [(3, "customer_id"), (4, "age")]
        )


if __name__ == "__main__":
    unittest.main()
