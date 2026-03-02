# Schema and Tables Overview

This document provides a comprehensive overview of all database schemas and tables created by the notebooks in the schema folder.

## Summary Statistics

- **Total Notebooks**: 6
- **Total Schemas**: 5
- **Total Tables**: 20

---

## Detailed Table Inventory

| Notebook File | Schema Name | Table Name | Description |
|---------------|-------------|------------|-------------|
| model_customer.ipynb | customer | Customer | Core customer information and demographics |
| model_customer.ipynb | customer | CustomerTradeName | Business trade names for customers |
| model_customer.ipynb | customer | CustomerRelationshipType | Customer relationship classifications |
| model_customer.ipynb | customer | Location | Geographic location data |
| model_customer.ipynb | customer | CustomerAccount | Customer account management |
| model_product.ipynb | product | Product | Product catalog and specifications |
| model_product.ipynb | product | ProductCategory | Product categorization (Camping, Kitchen, Ski) |
| model_sales.ipynb | sales | Order | Sales order headers |
| model_sales.ipynb | sales | OrderLine | Sales order line items |
| model_sales.ipynb | sales | OrderPayment | Payment transaction details |
| model_finance.ipynb | finance | invoice | Financial invoicing records |
| model_finance.ipynb | finance | account | Financial account management |
| model_finance.ipynb | finance | payment | Financial payment processing |
| model_inventory.ipynb | supplychain | Inventory | Current inventory levels and locations |
| model_inventory.ipynb | supplychain | InventoryTransactions | Inventory movement audit trail |
| model_inventory.ipynb | supplychain | PurchaseOrders | Purchase order headers |
| model_inventory.ipynb | supplychain | PurchaseOrderItems | Purchase order line items |
| model_suppliers.ipynb | supplychain | Suppliers | Supplier master data |
| model_suppliers.ipynb | supplychain | ProductSuppliers | Product-supplier relationship mapping |
| model_suppliers.ipynb | supplychain | SupplyChainEvents | Disruption events and impacts |

---

## Schema Distribution

| Schema Name | Number of Tables | Notebooks |
|-------------|-------------------|-----------|
| customer | 5 | model_customer.ipynb |
| product | 2 | model_product.ipynb |
| sales | 3 | model_sales.ipynb |
| finance | 3 | model_finance.ipynb |
| supplychain | 7 | model_inventory.ipynb, model_suppliers.ipynb |

---

## Business Domain Coverage

### Core Business Operations
- **Customer Management**: 5 tables for customer data, relationships, and accounts
- **Product Catalog**: 2 tables for products and categories
- **Sales Processing**: 3 tables for orders, line items, and payments
- **Financial Operations**: 3 tables for invoicing, accounts, and payments

### Supply Chain Management
- **Inventory Control**: 2 tables for stock levels and transactions
- **Procurement**: 2 tables for purchase orders and line items
- **Supplier Management**: 2 tables for suppliers and product relationships  
- **Risk Management**: 1 table for disruptions and impacts

---

## Integration Points

The schema design supports cross-domain integration through foreign key relationships:

- **Product** tables link to **Sales**, **Inventory**, and **Suppliers**
- **Customer** tables link to **Sales** and **Finance**
- **Supplier** information feeds **Purchase Orders**
- **Disruption** events impact **Inventory** planning accuracy

---

*Generated on: March 2, 2026*
*Source: C:\Repos\Explore\udf_solutions\prototype\src\fabric\notebooks\schema\*