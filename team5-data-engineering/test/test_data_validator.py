
import csv
import tempfile
import unittest
from pathlib import Path

from src.data_validator import validate_csv


class TestValidateCSV(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.temp_path = Path(self.temp_dir.name)

    def create_csv(self, filename, content):
        file_path = self.temp_path / filename
        file_path.write_text(content, encoding="utf-8")
        return file_path

    def test_valid_csv(self):
        file_path = self.create_csv(
            "valid.csv",
            "customer_id,name\n1,Asha\n2,Ravi\n"
        )
        result = validate_csv(
            file_path,
            required_columns=["customer_id", "name"]
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["row_count"], 2)

    def test_missing_file(self):
        file_path = self.temp_path / "missing.csv"
        result = validate_csv(file_path)
        self.assertEqual(result["status"], "FAIL")

    def test_empty_file(self):
        file_path = self.create_csv("empty.csv", "")
        result = validate_csv(file_path)
        self.assertEqual(result["status"], "FAIL")

    def test_header_only_file(self):
        file_path = self.create_csv(
            "header_only.csv",
            "customer_id,name\n"
        )
        result = validate_csv(file_path)
        self.assertEqual(result["status"], "FAIL")

    def test_missing_required_column(self):
        file_path = self.create_csv(
            "missing_column.csv",
            "customer_id\n1\n"
        )
        result = validate_csv(
            file_path,
            required_columns=["customer_id", "name"]
        )
        self.assertEqual(result["status"], "FAIL")

    def test_extra_value_in_row(self):
        file_path = self.create_csv(
            "extra_value.csv",
            "customer_id,name\n1,Asha,extra\n"
        )
        result = validate_csv(file_path)
        self.assertEqual(result["status"], "FAIL")

    
    def test_missing_values(self):
        file_path = self.create_csv(
            "missing_values.csv",
            "customer_id,name\n1,Asha\n2,   \n"
        )

        result = validate_csv(file_path)

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["missing_value_count"], 1)

        warning = next(
            rule for rule in result["rules"]
            if rule["rule"] == "missing_values"
        )
        self.assertEqual(warning["status"], "WARNING")

    def test_duplicate_rows(self):
        file_path = self.create_csv(
            "duplicate_rows.csv",
            "customer_id,name\n1,Asha\n1,Asha\n2,Ravi\n"
        )

        result = validate_csv(file_path)

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["duplicate_row_count"], 1)

        warning = next(
            rule for rule in result["rules"]
            if rule["rule"] == "duplicate_rows"
        )
        self.assertEqual(warning["status"], "WARNING")
    
    def test_valid_data_types(self):
        file_path = self.create_csv(
            "valid_types.csv",
            "age,purchase_amount\n25,199.50\n30,250\n"
        )

        result = validate_csv(
            file_path,
            expected_types={
                "age": "integer",
                "purchase_amount": "number"
            }
        )

        self.assertEqual(result["invalid_type_count"], 0)
        self.assertEqual(result["status"], "PASS")

    def test_invalid_data_types(self):
        file_path = self.create_csv(
            "invalid_types.csv",
            "age,purchase_amount\nabc,199.50\ntwenty,xyz\n"
        )

        result = validate_csv(
            file_path,
            expected_types={
                "age": "integer",
                "purchase_amount": "number"
            }
        )

        self.assertEqual(result["invalid_type_count"], 3)
        self.assertEqual(result["status"], "PASS")

        type_rule = next(
            rule for rule in result["rules"]
            if rule["rule"] == "data_types"
        )
        self.assertEqual(type_rule["status"], "WARNING")

    
    def test_invalid_type_finding_details(self):
        file_path = self.create_csv(
            "invalid_details.csv",
            "name,age\nAlice,25\nBob,abc\n"
        )

        result = validate_csv(
            file_path,
            required_columns=["name", "age"],
            expected_types={"age": "integer"}
        )

        self.assertEqual(result["invalid_type_count"], 1)
        self.assertEqual(len(result["findings"]), 1)
        self.assertEqual(result["findings"][0]["rule"], "data_types")
        self.assertEqual(result["findings"][0]["row"], 3)
        self.assertEqual(result["findings"][0]["column"], "age")
        self.assertEqual(result["findings"][0]["value"], "abc")


if __name__ == "__main__":
    unittest.main()
