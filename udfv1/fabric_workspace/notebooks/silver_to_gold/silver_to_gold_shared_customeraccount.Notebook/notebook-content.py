# Fabric notebook source

# METADATA ********************

# META {
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "49a06e70-9384-4d50-abcf-1ebf6229b4ed",
# META       "default_lakehouse_name": "maag_gold",
# META       "default_lakehouse_workspace_id": "48a335c3-cd4e-4e4f-a63f-3a5461e94d68",
# META       "known_lakehouses": [
# META         {
# META           "id": "49a06e70-9384-4d50-abcf-1ebf6229b4ed"
# META         },
# META         {
# META           "id": "c9316786-187e-4975-91dc-d829d83f16fe"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Load Silver Table to Gold Table - shared.customeraccount
# 
# ## Overview
# Load CustomerAccount data from Silver lakehouse table to Gold lakehouse table.
# 
# ## Data Flow
# - **Source**: Silver Lakehouse shared.customeraccount
# - **Target**: Gold Lakehouse shared.customeraccount
# - **Process**: Read Silver table, apply transformations, load to Gold Delta table
# 
# ---

# CELL ********************

# Step 1 Import Libraries and Set up Source Path 

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, sum as spark_sum, current_timestamp
import os
import sempy.fabric as fabric

# Configuration - Silver to Gold data flow
# Get workspace ID dynamically at runtime (avoids issues with spaces in workspace names)
WORKSPACE_ID = fabric.get_notebook_workspace_id()

# Get lakehouse ID dynamically (avoids issues with lakehouse names)
lakehouse_properties = mssparkutils.lakehouse.get("maag_silver")
SOURCE_LAKEHOUSE_ID = lakehouse_properties.id

SOURCE_SCHEMA = "shared"
SOURCE_TABLE = "customeraccount"

# Source: Absolute path to Silver lakehouse table
SOURCE_TABLE_PATH = f"abfss://{WORKSPACE_ID}@onelake.dfs.fabric.microsoft.com/{SOURCE_LAKEHOUSE_ID}/Tables/{SOURCE_SCHEMA}/{SOURCE_TABLE}"

# Target: Gold lakehouse (attached as default)
TARGET_SCHEMA = "shared"
TARGET_TABLE = "customeraccount"
TARGET_FULL_PATH = f"{TARGET_SCHEMA}.{TARGET_TABLE}"

print(f"🔄 Loading CustomerAccount from Silver to Gold")
print(f"📂 Source: {SOURCE_TABLE_PATH}")
print(f"🎯 Target: {TARGET_FULL_PATH}")
print("="*50)

# Read from Silver lakehouse table
df = spark.read.format("delta").load(SOURCE_TABLE_PATH)

print(f"✅ Data loaded from Silver table")
print(f"📊 Records: {df.count()}")
print(f"📋 Columns: {df.columns}")

# Display sample data
print(f"\n📖 Sample data from Silver:")
df.show(10, truncate=False)

# CELL ********************

# Step 2: Apply Gold layer transformations and data quality

print(f"🔧 Applying Gold layer transformations...")

# Add audit columns for Gold layer
df_gold = df.withColumn("GoldLoadTimestamp", current_timestamp())

# Data quality checks for Gold layer
print(f"\n🔍 Gold layer data quality validation...")

# Check for duplicates
duplicate_count = df_gold.groupBy("CustomerAccountId").count().filter(col("count") > 1).count()
if duplicate_count > 0:
    print(f"⚠️ Found {duplicate_count} duplicate CustomerAccountIds")
else:
    print(f"✅ No duplicates found")

# Check for nulls in key fields
null_checks = df_gold.select(
    spark_sum(col("CustomerAccountId").isNull().cast("int")).alias("null_ids"),
    spark_sum(col("CustomerAccountName").isNull().cast("int")).alias("null_names")
).collect()[0]

if null_checks["null_ids"] > 0 or null_checks["null_names"] > 0:
    print(f"⚠️ Found nulls: IDs={null_checks['null_ids']}, Names={null_checks['null_names']}")
else:
    print(f"✅ No nulls in key fields")

print(f"\n📖 Sample Gold data:")
df_gold.show(10, truncate=False)

# CELL ********************

# Step 3: Load data to Gold table

print(f"💾 Loading data to Gold table: {TARGET_FULL_PATH}")

try:
    # Write to Gold Delta table (default lakehouse)
    df_gold.write \
      .format("delta") \
      .mode("overwrite") \
      .option("overwriteSchema", "true") \
      .saveAsTable(TARGET_FULL_PATH)

    print(f"✅ Data loaded successfully to Gold table")

    # Verify the load
    result_count = spark.sql(f"SELECT COUNT(*) as count FROM {TARGET_FULL_PATH}").collect()[0]["count"]
    print(f"📊 Records in Gold table: {result_count}")

    # Show sample of loaded Gold data
    print(f"\n📖 Sample from Gold table:")
    spark.sql(f"SELECT * FROM {TARGET_FULL_PATH} ORDER BY CustomerAccountId").show(10, truncate=False)

    print(f"🎉 Silver to Gold data load complete!")

except Exception as e:
    print(f"❌ Error loading data to Gold table: {str(e)}")
    raise
