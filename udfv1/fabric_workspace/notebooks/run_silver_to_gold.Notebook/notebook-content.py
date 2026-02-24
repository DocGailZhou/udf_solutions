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

# # Data Processing from silver to gold 

# MARKDOWN ********************

# ## Prepare Clean Envronment for gold Lakehouse 

# CELL ********************

# %run truncate_all_tables_gold

# CELL ********************

# %run drop_all_tables_gold

# MARKDOWN ********************

# ## Create Schema and Tables in gold 

# CELL ********************

%run model_finance_gold

# CELL ********************

%run model_shared_gold

# CELL ********************

%run model_salesfabric_gold

# CELL ********************

%run model_salesadb_gold

# MARKDOWN ********************

# ## Silver to gold - finance tables 

# CELL ********************

%run silver_to_gold_finance_account

# CELL ********************

%run silver_to_gold_finance_invoice

# CELL ********************

%run silver_to_gold_finance_payment

# MARKDOWN ********************

# ## Silver to gold - salesfabric tables 

# CELL ********************

%run silver_to_gold_salesfabric_order

# CELL ********************

%run silver_to_gold_salesfabric_orderLine

# CELL ********************

%run silver_to_gold_salesfabric_orderPayment

# MARKDOWN ********************

# ## Silver to gold - salesadb tables 

# CELL ********************

%run silver_to_gold_salesadb_order

# CELL ********************

%run silver_to_gold_salesadb_orderLine

# CELL ********************

%run silver_to_gold_salesadb_orderPayment

# MARKDOWN ********************

# ## Silver to gold - shared (customer and product) tables

# CELL ********************

%run silver_to_gold_shared_customer

# CELL ********************

%run silver_to_gold_shared_customerAccount

# CELL ********************

%run silver_to_gold_shared_customerRelationshipType

# CELL ********************

%run silver_to_gold_shared_customerTradeName

# CELL ********************

%run silver_to_gold_shared_customerTradeName

# CELL ********************

%run silver_to_gold_shared_location

# CELL ********************

%run silver_to_gold_shared_product

# CELL ********************

%run silver_to_gold_shared_productCategory

# MARKDOWN ********************

