# Supply Chain Data Generation Guide

**Enterprise Supply Chain & Inventory Management with Analytics Dashboard**

Generates comprehensive supply chain data with sales integration and professional 4-chart analytics visualization.

## 🎯 What It Does

- **📦 Supplier Management** → 5 suppliers with procurement events  
- **📊 Inventory Intelligence** → Sales-driven inventory levels and purchase orders
- **📈 Analytics Dashboard** → Professional 4-chart PNG visualization

**Output**: 8 CSV files + analytics dashboard (supply_chain_data.png) + summary report

**Optional**: Use `--copydata` to copy all generated data to `../../infra/data/` for infrastructure deployment.

## Input Data

- **suppliers.json**: 5 suppliers with lead times and relationships
- **Product_Samples_Combined.csv**: Product catalog for supplier mappings  
- **Sales Data**: Analyzes existing transactions for demand intelligence

## 🚀 Quick Start

```bash
# Custom timeline - with custom start date and end date (recommended)
python main_generate_supplychain.py --graph -s 2025-12-01 -e 2026-03-02 --num-orders 50 --num-transactions 800

# Complete supply chain data with a default start date 2025-01-01, and today's date as ending date
python main_generate_supplychain.py --graph

# Production scale
python main_generate_supplychain.py --graph --num-orders 50 --num-transactions 800

# Production scale with data copy to infra
python main_generate_supplychain.py --graph --copydata --num-orders 50 --num-transactions 800

# Basic generation with infrastructure copy
python main_generate_supplychain.py --copydata

# Development testing
python main_generate_supplychain.py --graph --num-orders 10 --num-transactions 50
```

**Note**: Use `--copydata` flag to copy generated data to `../../infra/data/` for infrastructure deployment.

## ⚙️ Default Behavior

**When no dates are specified**, the program automatically uses smart defaults:

| Setting | Default Value | Description |
|---------|---------------|-------------|
| **Start Date** | `2025-01-01` | Fixed starting point |
| **End Date** | **Today** (`2026-03-02`) | Automatically uses current date |
| **Timeline** | **425 days** | Complete business period coverage |
| **Transactions** | **Auto-scaled** | Analyzes 56,457+ sales records and scales to 6,375 transactions |

**Simple Command**: `python main_generate_supplychain.py --graph`
**Result**: Complete supply chain dataset spanning full business timeline with realistic patterns

## 📋 Command Options

| Option | Description | Values | Impact |
|--------|------------|--------|--------|
| `--graph` | Generate analytics dashboard | Always use | Creates 4-chart PNG |
| `--copydata` | Copy files to infra/data directory | Optional | Organizes files in infra/data/suppliers/ and infra/data/inventory/ + suppliers.json config |
| `--num-orders` | Purchase orders to generate | 10-15 (test), 25-35 (demo), 50+ (production) | Each order = 2-5 line items |
| `--num-transactions` | Inventory transactions | 50-100 (small), 150-300 (demo), 800+ (full) | Stock movements for analytics |
| `-s/--start-date` | Start date (YYYY-MM-DD) | `2025-01-01` | Timeline beginning |
| `-e/--end-date` | End date (YYYY-MM-DD) | `2026-03-02` | Timeline end |

## 📁 Output Files

```
output/
├── suppliers/     # Suppliers, ProductSuppliers, SupplyChainEvents  
├── inventory/     # Inventory, PurchaseOrders, PurchaseOrderItems, InventoryTransactions
├── supply_chain_data.png           # Analytics dashboard
└── sample_supplychain_data_summary.md   # Business report
```

**With --copydata option**:
```
infra/data/
├── suppliers/     # Organized supplier files + suppliers.json config
├── inventory/     # Organized inventory files
└── sample_supplychain_data_summary.md   # Business report
```

## 🏭 Suppliers

| Supplier | Type | Lead Time | Reliability |
|----------|------|-----------|-------------|
| Contoso Outdoor/Kitchen/Alpine | Primary | 7-14 days | 90-95% |
| Worldwide Importers | Backup | 21 days | 88% |
| Fabrikam Supply Co | Backup | 28 days | 85% |

## 📊 Data Output

**Supplier Management** (3 CSV files + config): Suppliers, ProductSuppliers, SupplyChainEvents + suppliers.json
**Inventory Management** (4 files): InventoryLevels, PurchaseOrders, PurchaseOrderLines, InventoryTransactions  
**Analytics**: 4-chart dashboard with warehouse capacity, supplier performance, inventory health

## 🎯 Use Cases

- **Supply Chain Analytics**: Supplier performance, inventory optimization, lead time analysis
- **Business Intelligence**: Cost analysis, demand forecasting, supplier management
- **Data Engineering**: Fabric lakehouse testing, ETL development, system integration

## 🎯 Best Practices

1. Always use `--graph` for analytics dashboard
2. Start with small datasets before scaling up  
3. Review dashboard for realistic metrics (≥80% supplier reliability)
4. Use generated PNG for presentations



