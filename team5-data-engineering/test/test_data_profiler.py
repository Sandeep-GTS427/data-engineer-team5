import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.data_profiler import profile_csv


class TestDataProfiler(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.csv_path = Path(self.temp_dir.name) / "customers.csv"

        self.csv_path.write_text(
            "customer_id,name,age\n"
            "1,Alice,25\n"
            "2,Bob,30\n"
            "3,Charlie,28\n",
            encoding="utf-8"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_dataset_dimensions(self):
        result = profile_csv(self.csv_path)

        self.assertEqual(result["row_count"], 3)
        self.assertEqual(result["column_count"], 3)

    def test_column_names(self):
        result = profile_csv(self.csv_path)

        names = [
            column["name"]
            for column in result["columns"]
        ]

        self.assertEqual(
            names,
            ["customer_id", "name", "age"]
        )

    def test_integer_column_statistics(self):
        result = profile_csv(self.csv_path)

        customer_id = result["columns"][0]

        self.assertEqual(customer_id["data_type"], "integer")
        self.assertEqual(customer_id["null_count"], 0)
        self.assertEqual(customer_id["distinct_count"], 3)
        self.assertEqual(customer_id["min"], 1)
        self.assertEqual(customer_id["max"], 3)

    def test_string_column_statistics(self):
        result = profile_csv(self.csv_path)

        name = result["columns"][1]

        self.assertEqual(name["data_type"], "string")
        self.assertEqual(name["distinct_count"], 3)
        self.assertIsNone(name["min"])
        self.assertIsNone(name["max"])

    def test_missing_values(self):
        self.csv_path.write_text(
            "customer_id,name,age\n"
            "1,Alice,25\n"
            "2,,30\n"
            "3,Charlie,\n",
            encoding="utf-8"
        )

        result = profile_csv(self.csv_path)

        name = result["columns"][1]
        age = result["columns"][2]

        self.assertEqual(name["null_count"], 1)
        self.assertAlmostEqual(name["null_pct"], 1 / 3, places=4)
        self.assertEqual(age["null_count"], 1)

    def test_duplicate_values(self):
        self.csv_path.write_text(
            "customer_id,city\n"
            "1,Bengaluru\n"
            "2,Bengaluru\n"
            "3,Mysuru\n",
            encoding="utf-8"
        )

        result = profile_csv(self.csv_path)

        city = result["columns"][1]

        self.assertEqual(city["distinct_count"], 2)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            profile_csv(
                Path(self.temp_dir.name) / "missing.csv"
            )

    def test_empty_file(self):
        self.csv_path.write_text("", encoding="utf-8")

        with self.assertRaises(ValueError):
            profile_csv(self.csv_path)

    def test_malformed_row(self):
        self.csv_path.write_text(
            "customer_id,name\n"
            "1,Alice\n"
            "2,Bob,Extra\n",
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            profile_csv(self.csv_path)


if __name__ == "__main__":
    unittest.main()