# Sample Data Generation Summary

**Generated**: 2026-02-25 16:36:02  
**Date Range**: 2020-01-01 to 2026-02-25  
**Duration**: 2248 days

## 📊 Generation Overview

### **Total Summary**
- **Orders**: 50,894
- **Order Lines**: 130,562
- **Sales Payments**: 50,894
- **Invoices**: 50,894
- **Finance Payments**: 50,894
- **Customer Accounts**: 1,539
- **Total Sales Value**: $62,695,344.66

### **Domain Performance**

| Domain | Orders | Total Sales | Avg Order Value |
|--------|--------|-------------|----------------|
| 🏕️ Camping | 40,114 | $39,950,352.22 | $995.92 |
| 🍳 Kitchen | 9,307 | $20,376,378.56 | $2189.36 |
| ⛷️ Ski | 1,473 | $2,368,613.88 | $1608.02 |


## 🎯 Key Metrics

### **Business Intelligence Ready**
- **Comprehensive Dataset**: 2248 days of realistic business data
- **Multi-Domain Coverage**: 3 product categories with seasonal patterns
- **Customer Hierarchy**: 513 customers across Individual, Business, and Government segments
- **Financial Completeness**: Full order-to-payment lifecycle with invoicing

### **Data Volume**
- **Average Orders per Day**: 22.6
- **Average Order Value**: $1231.88
- **Order Line Items**: 2.6 items per order average
- **Customer Coverage**: 1539 accounts across all domains

## 📁 Output Structure

### **Sales Data (per domain)**
- `Order_Samples_[Domain].csv` - Main order records with totals and customer info
- `OrderLine_Samples_[Domain].csv` - Individual product line items with quantities
- `OrderPayment_[Domain].csv` - Payment method and transaction details

### **Finance Data (per domain)**
- `Invoice_Samples_[Domain].csv` - Invoice records (generated day after order)
- `Payment_Samples_[Domain].csv` - Payment records (immediate for eCommerce)
- `Account_Samples_[Domain].csv` - Customer account balances (zero for eCommerce)

### **Reference Data (shared)**
- Customer master data, product catalogs, and lookup tables
- Located in: `../../infra/data/shared/`

## 🚀 Infrastructure Deployment

**Automatically deployed to**: `../../infra/data/`

- ✅ All 3 domain datasets with proper folder structure
- ✅ Complete reference data in shared folder
- ✅ This summary documentation
- ✅ Ready for immediate use in analytics, BI, and ML workflows

## 🔍 Data Quality

### **Schema Compliance**
- 100% Microsoft Fabric Delta Lake compatible
- Proper foreign key relationships maintained
- No deprecated fields (e.g., PaymentNumber removed)
- All CreatedBy fields populated with "SampleGen"

### **Business Realism**
- Seasonal purchasing patterns (camping in spring, ski in winter)
- Customer segment-based order frequencies
- Realistic product pricing and quantities
- Proper order status distributions
