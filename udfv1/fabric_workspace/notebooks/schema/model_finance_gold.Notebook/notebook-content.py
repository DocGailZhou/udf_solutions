# Fabric notebook source

# METADATA ********************

# META {
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "c9316786-187e-4975-91dc-d829d83f16fe",
# META       "default_lakehouse_name": "maag_gold",
# META       "default_lakehouse_workspace_id": "48a335c3-cd4e-4e4f-a63f-3a5461e94d68",
# META       "known_lakehouses": [
# META         {
# META           "id": "c9316786-187e-4975-91dc-d829d83f16fe"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Data Model for Finance (finance)
#  
# ## Overview
# This notebook creates Finance domain tables that integrate with shared master data from the Sales domain.
#  
# ## Schema Structure
# - **Finance Domain Tables (3 tables)**:
#     - Account: Tracks financial accounts for customers 
#         - Samples Ready:Account_Sample_Fabric.csv
#     - Invoice: Bills sent to customers, links to Sales Order
#         - Samples Ready: Invoice_Samples_ADB.csv, Invoice_Samples_Fabric.csv
#     - Payment: Money received from customers, links to Invoice
#         - Samples Ready: Payment_Samples_ADB.csv, Payment_Samples_Fabric.csv
# - **Integration**:
#     - CustomerId: FK to shared Customer table
#     - OrderId: FK to shared Order table (Invoice)
#     - InvoiceId: FK to Invoice table (Payment)
#  
# ---

# CELL ********************

################################################################################################
# Schema Configuration - MODIFY THIS VALUE
################################################################################################

# Schema Configuration
SCHEMA_NAME = "finance"
spark.sql(f"CREATE DATABASE IF NOT EXISTS {SCHEMA_NAME}")
print(f"✅ {SCHEMA_NAME} schema ready!")

# CELL ********************

################################################################################################
# FINANCE DOMAIN TABLES
################################################################################################

# 1. Create Invoice table (Bills sent to customers - Links to Sales Order)
TABLE_NAME = "invoice"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    InvoiceId STRING,
    InvoiceNumber STRING,
    CustomerId STRING,        -- FK to shared Customer table
    OrderId STRING,           -- FK to shared Order table  
    InvoiceDate DATE,
    DueDate DATE,
    SubTotal DECIMAL(18,2),
    TaxAmount DECIMAL(18,2),
    TotalAmount DECIMAL(18,2),
    InvoiceStatus STRING,
    CreatedBy STRING
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")

# 2. Create Account table (Tracks financial accounts for customers)
TABLE_NAME = "account"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    AccountId STRING,
    AccountNumber STRING,
    CustomerId STRING,        -- FK to shared Customer table
    AccountType STRING,       -- e.g., Receivable, Payable, Credit, Cash
    AccountStatus STRING,     -- e.g., Active, Closed, Suspended
    CreatedDate DATE,
    ClosedDate DATE,
    Balance DECIMAL(18,2),
    Currency STRING,
    Description STRING,
    CreatedBy STRING
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")


# 3. Create Payment table (Money received from customers)
TABLE_NAME = "payment"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
    PaymentId STRING,
    InvoiceId STRING,         -- FK to Invoice table
    CustomerId STRING,        -- FK to shared Customer table
    PaymentDate DATE,
    PaymentAmount DECIMAL(18,2),
    PaymentMethod STRING,
    PaymentStatus STRING,
    CreatedBy STRING
)
USING DELTA
"""
spark.sql(create_table_sql)
print(f"✅ {SCHEMA_NAME}.{TABLE_NAME} table created!")

print(f"\n✅ All Finance Domain tables created successfully!")
