# Supply Chain Data Generation Guide

A comprehensive utility for generating realistic supply chain and inventory management data integrated with existing sales operations. Extends the successful customer/product/sales/finance system with intelligent procurement and inventory intelligence.

## 🎯 What It Does

Generates realistic supply chain data for business operations:
- **📦 Supplier Management** → Master data, relationships, and procurement events  
- **📊 Inventory Intelligence** → Sales-driven inventory levels and purchase orders
- **🔄 Integration Layer** → Seamless connection with existing 56,457+ sales transactions

The system produces **7 CSV files**: Suppliers, ProductSuppliers, SupplyChainEvents (Supplier Management) + InventoryLevels, PurchaseOrders, PurchaseOrderLines, InventoryTransactions (Inventory Management).

**Key Feature**: Sales-driven inventory intelligence analyzes real sales velocity to generate realistic inventory levels, safety stock calculations, and automated purchase order generation.

## Input Data & Configuration

### **Data Sources**
- **suppliers.json** *(input/)*: 5 suppliers with contact details, lead times, and backup relationships
- **Product_Samples_Combined.csv** *(input/)*: Product catalog for supplier mappings and cost calculations  
- **Sales Data** *(output/)*: Analyzes 56,457+ existing transactions for demand intelligence

**Key Integration**: System automatically analyzes existing sales patterns to generate realistic inventory levels and procurement decisions.

## 🚀 Quick Start

```bash
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Generate complete supply chain data (recommended)
python main_generate_supplychain.py

# Generate data for specific date range
python main_generate_supplychain.py -s 2025-01-01 -e 2026-03-02

# Generate only supplier data (no inventory)
python main_generate_supplychain.py --suppliers-only

# Custom generation with specific parameters
python main_generate_supplychain.py -s 2025-01-01 -e 2026-03-02 --num-orders 25 --num-transactions 150

# Quick validation run
python main_generate_supplychain.py -s 2025-01-01 -e 2025-01-31 --num-orders 10 --num-transactions 50
```

**Default**: When no dates are specified, automatically generates data from 2025-01-01 to today's execution date.  
**Sales Integration**: Automatically analyzes existing sales data to drive realistic inventory calculations and purchasing patterns.

## 📋 Command Options

### **Main Orchestrator (`main_generate_supplychain.py`)**
| Option | Description | Example |
|--------|------------|---------|
| `-s`, `--start-date` | Start date (YYYY-MM-DD) | `-s 2025-01-01` |
| `-e`, `--end-date` | End date (YYYY-MM-DD) | `-e 2026-03-02` |
| `--suppliers-only` | Generate only supplier data (skip inventory) | |
| `--num-orders` | Number of purchase orders to generate | `--num-orders 25` |
| `--num-transactions` | Number of inventory transactions | `--num-transactions 150` |

### **Individual Generators**
Run individual generators for specific customization:
```bash
python generate_suppliers.py -s 2025-01-01 -e 2025-12-31
python generate_inventory.py -s 2025-01-01 -e 2025-12-31 --num-orders 20 --num-transactions 100
```

## 📁 Output Structure

```
output/sample_supplychain/
├── suppliers/                        # 3 files: Suppliers, ProductSuppliers, SupplyChainEvents
└── inventory/                        # 4 files: InventoryLevels, PurchaseOrders, PurchaseOrderLines, InventoryTransactions
sample_supplychain_data_summary.md    # Automated business intelligence report
```

## 🏭 Supplier Configuration

**5 Suppliers**: 3 Primary (domain-specific) + 2 Backup (multi-domain)

| Supplier | Type | Lead Time | Reliability | Coverage |
|----------|------|-----------|-------------|----------|
| **Contoso Outdoor/Kitchen/Alpine** | Primary | 7-14 days | 90-95% | Category-specific |
| **Worldwide Importers** | Backup | 21 days | 88% | Cross-domain |
| **Fabrikam Supply Co** | Backup | 28 days | 85% | Cross-domain |

**Configuration**: JSON-driven with contact details, payment terms, and backup relationships.

## 📊 Data Models & Relationships

### **Supplier Management Tables (3)**

1. **Supplier_Samples.csv**: Master supplier data
   - Supplier details, contact information, terms
   - Reliability scoring and lead time management
   - Geographic distribution and payment terms

2. **ProductSupplier_Samples.csv**: Product-supplier relationships  
   - Wholesale cost calculations (60-80% of retail prices)
   - Primary vs backup supplier assignments (85% vs 15% split)
   - Cost tier optimization by supplier reliability

3. **SupplyChainEvent_Samples.csv**: Supply chain activity tracking
   - Procurement events, delivery confirmations
   - Quality audits and supplier performance tracking
   - Event timestamp and status management

### **Inventory Management Tables (4)**

1. **InventoryLevel_Samples.csv**: Current stock levels
   - **Sales velocity analysis**: Analyzes actual sales data to calculate realistic inventory
   - **Safety stock calculations**: Based on lead times and demand variability
   - Stock status tracking (In Stock, Low Stock, Out of Stock)

2. **PurchaseOrder_Samples.csv**: Purchase order headers
   - Supplier integration with lead time consideration
   - Order status progression and approval workflows
   - Total amount calculations with tax considerations

3. **PurchaseOrderLine_Samples.csv**: Purchase order line items
   - Product-specific quantities and pricing
   - Expected delivery date calculations
   - Line-level status tracking and received quantities

4. **InventoryTransaction_Samples.csv**: Inventory movement audit trail
   - **Sales integration**: Tracks actual sales consumption
   - **Procurement receipts**: Records supplier deliveries
   - Real-time inventory level adjustments

## 🔄 Sales-Driven Intelligence

**Automatic Integration**: Analyzes existing sales data (56,457+ transactions) to calculate:
- **Demand Velocity**: Average daily sales per product
- **Safety Stock**: Lead time × daily demand × safety factor  
- **Reorder Points**: Automated replenishment triggers
- **Purchase Timing**: Economic order quantities with seasonal patterns

**Business Logic**: Wholesale costs (60-80% retail), realistic lead times (7-28 days), backup supplier activation (15% usage)

## � Business Analytics

**Key Metrics**: 
- Supply chain costs (60-80% wholesale margin), lead time optimization (7-28 days)
- Inventory turnover analysis, safety stock calculations, backup supplier usage (15%)
- Real-time performance tracking with reliability scoring (85-95%)

**Domain Coverage**: Camping (~$45K inventory), Kitchen (~$32K), Ski (~$67K)

## 🛠️ Examples & Usage

```bash
# Complete supply chain generation (recommended)
python main_generate_supplychain.py

# Suppliers only (quick setup)
python main_generate_supplychain.py --suppliers-only

# Production scale with custom parameters  
python main_generate_supplychain.py -s 2025-01-01 -e 2025-12-31 --num-orders 50 --num-transactions 300

# Development testing
python main_generate_supplychain.py -s 2025-01-01 -e 2025-01-31 --num-orders 10 --num-transactions 50
```



## 🔧 Microsoft Fabric Integration

**Ready-to-Deploy Notebooks**:
- **model_suppliers.ipynb**: Creates all supplier tables (Suppliers, ProductSuppliers, SupplyChainEvents)
- **model_inventory.ipynb**: Creates all inventory tables (InventoryLevels, PurchaseOrders, PurchaseOrderLines, InventoryTransactions)

**Schema Compliance**: 100% Microsoft Fabric Delta Lake compatible with optimized data types and foreign key relationships.

## 🎯 Key Features

- **Sales-Driven Intelligence**: Automatic analysis of existing sales data for realistic inventory calculations
- **JSON Configuration**: Easy supplier management with configurable relationships and backup strategies  
- **Dynamic Reporting**: Automated summary generation with real-time statistics and business intelligence
- **Modular Design**: Suppliers-only mode for testing, full integration for production use

## ⚠️ Performance & Notes

**Timing**: Small datasets (1 month) ~15 seconds, Full year ~45-60 seconds, Multi-year ~2-3 minutes  
**Dependencies**: Requires existing sales data for inventory intelligence, Product catalog for supplier mappings  
**Validation**: Inventory levels always positive, purchase timing respects lead times, costs maintain retail margins

## 📈 Use Cases

### **Supply Chain Optimization**
- Supplier performance analysis and cost comparison
- Inventory level optimization and safety stock calculations
- Lead time analysis and backup supplier activation patterns
- Procurement cycle efficiency and order quantity optimization

### **Business Intelligence & Analytics**
- Supply chain cost analysis across multiple suppliers
- Inventory turnover analysis and carrying cost optimization
- Sales-driven demand forecasting and procurement planning
- Supplier relationship management and performance tracking

### **Data Engineering & Architecture**
- Microsoft Fabric lakehouse supply chain schema testing
- ETL pipeline development for procurement systems
- Real-time inventory management system development
- Data integration testing between sales and supply chain systems

### **Financial Analysis & Planning**
- Working capital analysis (inventory investment optimization)
- Supplier payment term analysis and cash flow planning
- Cost variance analysis across supplier tiers
- Purchase order commitment tracking and budget management

## 🎯 Best Practices

1. **Start with suppliers-only**: Use `--suppliers-only` flag for initial testing and validation
2. **Verify sales integration**: Ensure existing sales data is available for intelligent inventory calculations
3. **Test incrementally**: Start with small date ranges and low transaction counts before scaling
4. **Monitor sales connectivity**: Check summary report for sales integration status confirmation
5. **Validate business logic**: Review generated inventory levels against sales velocity patterns
6. **Use consolidated notebooks**: Deploy schema using single-execution notebook cells for Fabric efficiency
7. **Plan for scale**: Large datasets generate substantial procurement and inventory transaction volumes

## 🔗 Integration Points

### **Existing System Connections**
- **Product Catalog**: Integrates with Product_Samples_Combined.csv for supplier mappings
- **Sales Analysis**: Connects to Order*_Samples_*.csv files for demand intelligence
- **Customer Independent**: Supply chain operates without direct customer data dependencies
- **Finance Ready**: Purchase orders and inventory values ready for financial system integration

### **Future Extension Points**
- **Quality Management**: Supplier quality scoring and audit trail expansion
- **Multi-location Inventory**: Geographic distribution and transfer management
- **Advanced Forecasting**: Machine learning integration for demand prediction
- **Supplier Portal Integration**: API-ready data structure for supplier self-service

---

**Enterprise Ready**: This supply chain system generates comprehensive procurement and inventory data with intelligent sales integration, suitable for Microsoft Fabric, Azure Databricks, and enterprise ERP environments. All data maintains referential integrity with existing customer/product/sales systems and realistic supply chain business patterns.