# GTS Platform — Team 5: Data Engineering
## Databricks PySpark Automated Multi-Format ETL Pipeline & Medallion Architecture

**Prepared by:** Sandeep Lande – Data Engineering Lead  
**Date:** November 23, 2026  
**Platform:** Databricks Serverless (Apache Spark 4.2.0)  
**Catalog & Volume:** `workspace.default.humanresource`

---

## 1. Executive Summary

To scale the GTS Data Quality & Ingestion engine for enterprise big-data workloads, Team 5 designed and implemented an automated **Medallion Architecture (Bronze → Silver → Gold)** pipeline using **PySpark on Databricks**.

This implementation addresses a core business requirement:
* Automatically ingesting multi-format raw dumps (**Excel `.xlsx`**, **CSV `.csv`**, and **JSON `.json`**).
* Repairing schema anomalies and known edge cases (such as the CEO Ken Sánchez literal `'NULL'` string hierarchy values and ANSI float casting conflicts).
* Outputting certified, standardized single `.csv` files into the Databricks Volume alongside high-performance **Delta Lake** tables ready for downstream AI/AutoML consumption (Team 1 Preprocessing and Team 4 Model Training).

---

## 2. Architecture: Medallion Design

```
+-----------------------------------------------------------------------------------+
|                            BRONZE LAYER (Raw Landing)                             |
|  - Ingests .xlsx, .csv, and .json directly from Databricks Volumes               |
|  - Preserves raw values, handles malformed inputs without failing                 |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        SILVER LAYER (Cleansing & Quality Gate)                     |
|  - Auto-repairs CEO Ken Sánchez 'NULL' strings -> root '/' and Level 0           |
|  - Eliminates '1.0' string-float ANSI cast errors via safe integer coercion       |
|  - Formats date strings to standard ISO (YYYY-MM-DD)                             |
|  - Generates categorical 'SalariedCategory' to prevent IQR outlier false alarms   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        GOLD LAYER (Certified Master Output)                       |
|  - Exports single clean .csv to Volume: /Volumes/.../Result_From_<Format>.csv    |
|  - Registers certified Delta Lake table: team5_gold_employee_master               |
|  - Enables high-speed Spark SQL queries and ACID transactional updates           |
+-----------------------------------------------------------------------------------+
```

---

## 3. Key Technical Challenges & Resolutions

| Challenge | Root Cause | Team 5 Engineering Resolution |
|---|---|---|
| **Excel Binary vs CSV Conflict** | Reading `.xlsx` with `spark.read.format("csv")` treated the zip archive header `PK...[Content_Types].xml` as column names. | Integrated notebook-scoped `openpyxl` with `pandas.read_excel()` to parse binary Excel sheets directly before Spark conversion. |
| **`CAST_INVALID_INPUT` on `'1.0'`** | Excel numeric cells with missing values read into pandas as floats (`1.0`, `2.0`). Spark 4.0 ANSI mode forbids casting string floats directly to integer/bigint. | Implemented pre-ingestion numeric coercion (`pd.to_numeric(..., errors='coerce').fillna(0).astype(int)`), eliminating all decimal strings. |
| **CEO Hierarchy `'NULL'` String** | In AdventureWorks, CEO Ken Sánchez (`BusinessEntityID = 1`) contains literal string `'NULL'` in `OrganizationNode` and `OrganizationLevel`. | Auto-repaired `'NULL'` to root path `'/'` and integer `0` (the official AdventureWorks root hierarchy rank). |
| **Multi-Format Ingestion** | Need to accept `.xlsx`, `.csv`, and `.json` files transparently without changing pipeline code. | Built `process_any_file_to_csv()`, which auto-detects file extensions and applies consistent cleansing across all formats. |

---

## 4. Live Verification Results

The pipeline was executed and verified live on Databricks Serverless (Apache Spark 4.2.0):

```text
📁 Created sample test CSV: /Volumes/workspace/default/humanresource/test_employee.csv
📁 Created sample test JSON: /Volumes/workspace/default/humanresource/test_employee.json

📥 INGESTING: /Volumes/workspace/default/humanresource/test_employee.csv
✅ Generated Clean CSV: /Volumes/workspace/default/humanresource/Result_From_CSV.csv (2 rows)

📥 INGESTING: /Volumes/workspace/default/humanresource/test_employee.json
✅ Generated Clean CSV: /Volumes/workspace/default/humanresource/Result_From_JSON.csv (1 rows)

🎉 Output from CSV:
+----------------+-----------------------------+----------------+-----------------+----------------+
|BusinessEntityID|JobTitle                     |OrganizationNode|OrganizationLevel|SalariedCategory|
+----------------+-----------------------------+----------------+-----------------+----------------+
|1               |Chief Executive Officer      |/               |0                |Salaried        |
|2               |Vice President of Engineering|/1/1/           |1                |Salaried        |
+----------------+-----------------------------+----------------+-----------------+----------------+

🎉 Output from JSON:
+----------------+-----------------------------+----------------+-----------------+----------------+
|BusinessEntityID|JobTitle                     |OrganizationNode|OrganizationLevel|SalariedCategory|
+----------------+-----------------------------+----------------+-----------------+----------------+
|3               |Engineering Manager          |/1/1/1/         |2                |Salaried        |
+----------------+-----------------------------+----------------+-----------------+----------------+
```

---

## 5. Artifact Deliverables

1. **Databricks Notebook Export:** `team5-data-engineering/notebooks/Team5_Databricks_PySpark_ETL_Pipeline.py`
2. **Test Datasets:**
   * `team5-data-engineering/data/test_sample_employee.csv`
   * `team5-data-engineering/data/test_sample_employee.json`
3. **Comprehensive Word Report:** `Team5_Week4_Databricks_PySpark_Implementation_Report.docx`
4. **Master Cleaned Datasets:**
   * `HumanResources_Employee_Cleaned.xlsx`
   * `HumanResources_Master_Cleaned.xlsx`
   * `HumanResources_Employee_Cleaned.csv`
