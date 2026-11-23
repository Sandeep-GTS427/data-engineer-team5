# Databricks notebook source
# MAGIC %md
# MAGIC # GTS Platform — Team 5: Data Engineering
# MAGIC ## Automated Multi-Format PySpark ETL Pipeline (Medallion Architecture)
# MAGIC **Author:** Sandeep Lande (Data Engineering Lead)  
# MAGIC **Date:** November 23, 2026  
# MAGIC **Platform:** Databricks Serverless (Apache Spark 4.2.0)  
# MAGIC **Catalog:** `workspace.default.humanresource`

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Environment & Cluster Health Check

# COMMAND ----------

print(f"Apache Spark Version: {spark.version}")
print("Databricks PySpark Serverless Cluster is active and ready for Team 5!")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Install Required Dependencies (Notebook-Scoped)

# COMMAND ----------

# MAGIC %pip install openpyxl

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Universal Multi-Format Pipeline Function
# MAGIC Handles incoming `.xlsx`, `.csv`, and `.json` files seamlessly:
# MAGIC - **Bronze Layer:** Ingests raw data as-is from Databricks Volumes.
# MAGIC - **Silver Layer:** Cleanses string `'NULL'`s, auto-repairs CEO hierarchy, enforces pure integer casting (handling `'1.0'` float decimals), standardizes ISO dates, and maps `SalariedCategory`.
# MAGIC - **Gold Layer:** Exports a single clean `.csv` to the Volume and writes to certified Delta Lake table.

# COMMAND ----------

import os
import json
import pandas as pd
from pyspark.sql.functions import col, when, lit, trim, to_date

def process_any_file_to_csv(input_file_path, output_csv_path, delta_table_name="team5_gold_employee_master"):
    """
    Universal Team 5 ETL Pipeline:
    - Accepts: .xlsx, .csv, or .json
    - Cleans: Fixes CEO 'NULL' strings, formats dates, repairs types
    - Outputs: A clean, single .csv file in the Volume + saves to Delta table
    """
    print(f"\n==================================================")
    print(f"📥 1. INGESTING FILE: {input_file_path}")
    print(f"==================================================")
    
    # Auto-detect file extension
    ext = os.path.splitext(input_file_path)[1].lower()
    
    if ext in [".xlsx", ".xls"]:
        print("Detected format: EXCEL (.xlsx)")
        pdf = pd.read_excel(input_file_path)
    elif ext == ".csv":
        print("Detected format: CSV (.csv)")
        pdf = pd.read_csv(input_file_path)
    elif ext == ".json":
        print("Detected format: JSON (.json)")
        pdf = pd.read_json(input_file_path)
    else:
        raise ValueError(f"Unsupported file format '{ext}'. Must be .xlsx, .csv, or .json")
        
    print(f"Raw rows ingested: {len(pdf)}")

    # --------------------------------------------------------------------------
    # 🥈 2. TEAM 5 DATA CLEANSING & VALIDATION (SILVER LAYER)
    # --------------------------------------------------------------------------
    print("Applying Team 5 automated cleansing & validation...")
    
    # A. Auto-repair CEO Ken Sánchez 'NULL' strings -> root '/' and integer 0
    if "OrganizationNode" in pdf.columns:
        pdf["OrganizationNode"] = pdf["OrganizationNode"].replace(["NULL", "null", None], "/").fillna("/")
    if "OrganizationLevel" in pdf.columns:
        pdf["OrganizationLevel"] = pd.to_numeric(
            pdf["OrganizationLevel"].replace(["NULL", "null", None], 0), errors="coerce"
        ).fillna(0).astype(int)
        
    # B. Ensure numeric columns are clean integers (eliminates the '1.0' float issue)
    int_cols = ["BusinessEntityID", "SalariedFlag", "VacationHours", "SickLeaveHours", "CurrentFlag"]
    for c in int_cols:
        if c in pdf.columns:
            pdf[c] = pd.to_numeric(pdf[c], errors="coerce").fillna(0).astype(int)
            
    # C. Standardize date strings (YYYY-MM-DD)
    for d_col in ["BirthDate", "HireDate"]:
        if d_col in pdf.columns:
            pdf[d_col] = pd.to_datetime(pdf[d_col], errors="coerce").dt.strftime("%Y-%m-%d")

    # --------------------------------------------------------------------------
    # 🥇 3. EXPORT CLEAN CSV DIRECTLY TO VOLUME & REGISTER TO DELTA (GOLD LAYER)
    # --------------------------------------------------------------------------
    print(f"💾 Saving single clean CSV to Volume: {output_csv_path}")
    pdf.to_csv(output_csv_path, index=False)
    
    # Register with PySpark for high-performance SQL querying
    df_spark = spark.createDataFrame(pdf)
    if "SalariedFlag" in df_spark.columns:
        df_spark = df_spark.withColumn(
            "SalariedCategory",
            when(col("SalariedFlag") == 1, lit("Salaried")).otherwise(lit("Hourly"))
        )
    df_spark.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(delta_table_name)
    
    print(f"🎯 SUCCESS! Clean file generated at: {output_csv_path}")
    print(f"🎯 Certified Delta Table updated: '{delta_table_name}' with {len(pdf)} rows.")
    return output_csv_path

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Production Execution on Full HR Employee Dataset (290 Rows)

# COMMAND ----------

volume_dir = "/Volumes/workspace/default/humanresource"
raw_excel_path = f"{volume_dir}/HumanResources.Employee.xlsx"
cleaned_csv_path = f"{volume_dir}/HumanResources_Employee_CLEANED_FINAL.csv"

# Execute on actual volume file if present
if os.path.exists(raw_excel_path):
    process_any_file_to_csv(raw_excel_path, cleaned_csv_path)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5. Multi-Format Verification (CSV & JSON Test Suite)

# COMMAND ----------

test_csv = f"{volume_dir}/test_employee.csv"
test_json = f"{volume_dir}/test_employee.json"

# Create sample CSV
csv_text = """BusinessEntityID,NationalIDNumber,LoginID,OrganizationNode,OrganizationLevel,JobTitle,BirthDate,MaritalStatus,Gender,HireDate,SalariedFlag,VacationHours,SickLeaveHours,CurrentFlag
1,295847284,adventure-works\\ken0,NULL,NULL,Chief Executive Officer,1969-01-29,S,M,2009-01-14,1,99,69,1
2,245797967,adventure-works\\terri0,/1/1/,1,Vice President of Engineering,1971-08-01,S,F,2008-01-31,1,1,20,1
"""
with open(test_csv, "w") as f:
    f.write(csv_text)

# Create sample JSON
json_records = [
    {
        "BusinessEntityID": 3,
        "NationalIDNumber": 509647174,
        "LoginID": "adventure-works\\roberto0",
        "OrganizationNode": "/1/1/1/",
        "OrganizationLevel": "2",
        "JobTitle": "Engineering Manager",
        "BirthDate": "1974-11-12",
        "MaritalStatus": "M",
        "Gender": "M",
        "HireDate": "2007-11-11",
        "SalariedFlag": 1,
        "VacationHours": 2,
        "SickLeaveHours": 21,
        "CurrentFlag": 1
    }
]
with open(test_json, "w") as f:
    json.dump(json_records, f, indent=2)

# Process both
process_any_file_to_csv(test_csv, f"{volume_dir}/Result_From_CSV.csv")
process_any_file_to_csv(test_json, f"{volume_dir}/Result_From_JSON.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 6. Query Gold Delta Master Table with Spark SQL

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     BusinessEntityID, 
# MAGIC     JobTitle, 
# MAGIC     OrganizationNode, 
# MAGIC     OrganizationLevel, 
# MAGIC     SalariedCategory, 
# MAGIC     VacationHours, 
# MAGIC     HireDate 
# MAGIC FROM team5_gold_employee_master 
# MAGIC ORDER BY BusinessEntityID ASC 
# MAGIC LIMIT 10;
