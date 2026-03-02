# Sales and Finance Data Generation Guide

A comprehensive utility for generating realistic sales and finance data across three business domains with automated infrastructure data deployment. The main purpose is to generate sales data. Finance data is generated based on actual sales data. 

## 🎯 What It Does

Generates realistic eCommerce data for three business domains:
- **🏕️ Camping Products** → Outdoor gear and equipment
- **🍳 Kitchen Products** → Home appliances and kitchenware  
- **⛷️ Ski Equipment** → Winter sports gear and accessories

Each domain produces **6 CSV files**: Orders, OrderLines, OrderPayments (Sales) + Invoices, Payments, Accounts (Finance).

**New**: Automatically copies all generated data to `../../infra/data/` for infrastructure deployment.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Default: Generate 6 years of data up to execution date (recommended)
python main_generate_sales.py

# 
python main_generate_sales.py  --enable-growth 

# Generate data for specific date range
python main_generate_sales.py -s 2025-01-01 -e 2026-01-19

# Generate all data for a single year
python main_generate_sales.py -s 2025-01-01 -e 2025-12-31

# Generate only camping data for specific period
python main_generate_sales.py -s 2024-06-01 -e 2024-12-31 --camping-only

# Generate data with business growth simulation
python main_generate_sales.py --enable-growth

# Generate growth data for specific period
python main_generate_sales.py -s 2025-01-01 -e 2025-12-31 --enable-growth

# Generate revenue trend graph
python main_generate_sales.py --graph

# Combine growth patterns with graphing
python main_generate_sales.py --enable-growth --graph
```

**Default**: When no dates are specified, automatically generates 6 years of data (from 6 years ago to today's execution date).  
**Note**: All generated data is automatically copied to `../../infra/data/` after successful generation.

## 📋 Command Options

### **Main Orchestrator (`main_generate_sales.py`)**
| Option | Description | Example |
|--------|------------|---------|
| `-s`, `--start-date` | Start date (YYYY-MM-DD) | `-s 2025-01-01` |
| `-e`, `--end-date` | End date (YYYY-MM-DD) | `-e 2025-12-31` || `--enable-growth` | Enable business growth patterns | || `--camping-only` | Generate only camping orders | |
| `--kitchen-only` | Generate only kitchen orders | |
| `--ski-only` | Generate only ski orders | |

### **Individual Generators**
Run individual domain generators for specific customization:
```bash
python generate_camping_orders.py -s 2025-01-01 -e 2025-12-31
python generate_kitchen_orders.py -s 2025-01-01 -e 2025-12-31  
python generate_ski_orders.py -s 2025-01-01 -e 2025-12-31
```

### **Domain Utilities**
```bash
# Generate ProductCategory files from Product data
python utils/create_category_from_product.py

# Consolidate all Product and ProductCategory files
python utils/consolidate_product_domain_input.py
```

## 📁 Output Structure

### **Local Output (src/data_simulator/output/)**
```
output/
├── camping/          # 🏕️ Camping Products
│   ├── sales/              # Order_Samples_Camping.csv, OrderLine_Samples_Camping.csv, OrderPayment_Camping.csv
│   └── finance/            # Invoice_Samples_Camping.csv, Payment_Samples_Camping.csv, Account_Samples_Camping.csv
├── kitchen/          # 🍳 Kitchen Products  
│   ├── sales/              # Order_Samples_Kitchen.csv, OrderLine_Samples_Kitchen.csv, OrderPayment_Kitchen.csv
│   └── finance/            # Invoice_Samples_Kitchen.csv, Payment_Samples_Kitchen.csv, Account_Samples_Kitchen.csv
├── ski/             # ⛷️ Ski Equipment
│   ├── sales/              # Order_Samples_Ski.csv, OrderLine_Samples_Ski.csv, OrderPayment_Ski.csv
│   └── finance/            # Invoice_Samples_Ski.csv, Payment_Samples_Ski.csv, Account_Samples_Ski.csv
└── sample_sales_data_summary.md   # 📊 Comprehensive data generation summary with statistics
```

### **Infrastructure Data Copy (../../infra/data/)**
**Automatically copied after generation:**
- **Input data** → `infra/data/shared/` (all customer, product, and reference data)
- **Output data** → `infra/data/sample_*/` (preserving folder structure)
- **Summary report** → `infra/data/sample_sales_data_summary.md` (comprehensive generation statistics)

### **Input Files**
```
input/
├── Product_Samples_Combined.csv          # All products consolidated
├── ProductCategory_Samples_Combined.csv  # All categories consolidated
├── Product_Samples_Camping.csv           # Individual domain files
├── Product_Samples_Kitchen.csv
├── Product_Samples_Ski.csv
├── ProductCategory_Samples_Camping.csv
├── ProductCategory_Samples_Kitchen.csv
├── ProductCategory_Samples_Ski.csv
├── Customer_Samples.csv                  # Customer master data (513 customers)
├── CustomerAccount_Samples.csv           # Customer account information
├── CustomerRelationshipType_Samples.csv  # Customer tier definitions
├── CustomerTradeName_Samples.csv         # Customer trade names
└── Location_Samples.csv                  # Customer location data
```

## 💰 Data Characteristics

### **Realistic Business Patterns**
- **Seasonal trends**: Tents in spring, ski gear in winter, kitchen appliances during holidays
- **Customer hierarchy**: Two-level system (CustomerTypeId > CustomerRelationshipTypeId)
- **Schema compliance**: 100% Microsoft Fabric Delta Lake compatible
- **Platform independence**: Domain-focused, not tied to specific cloud platforms

### **Customer Segment Hierarchy**

| Category | Tier Structure | Order Frequency (Camping/Kitchen/Ski) | Description |
|----------|---------------|----------------|-------------|
| **Individual** | Standard > Premium > VIP | 1-8 / 2-6 / 1-8 orders | Consumer progression (Kitchen boosted) |
| **Business** | SMB > Premier > Partner | 2-15 / 6-30 / 2-15 orders | Partner tier highest (Kitchen boosted) |
| **Government** | Federal > State > Local | 0-4 / 2-8 / 0-4 orders | Specialized procurement (Kitchen boosted) |

### **Average Order Values**
- **Camping**: ~$1,023 (moderate outdoor gear)
- **Kitchen**: ~$560 (boosted appliances, 2-4 products per order with 2x revenue multiplier)  
- **Ski**: ~$1,608 (premium equipment - highest value)

### **Customer Hierarchy Implementation**
The system uses a **two-level hierarchy** matching the database schema:
- `CustomerTypeId`: Individual | Business | Government  
- `CustomerRelationshipTypeId`: Specific tier within each type
- This structure allows easy addition of new customer types or relationship tiers

## � Business Growth Patterns

**NEW**: Enhanced with realistic business growth simulation when using `--enable-growth` flag.

### **Three-Phase Growth Simulation**

| Phase | Timeline | Pattern | Multiplier Range | Description |
|-------|----------|---------|------------------|-------------|
| **Phase 1** | 0-33% | Initial Growth | 1.0 → 1.2 (+20%) | Startup momentum, market entry |
| **Phase 2** | 33-67% | Market Decline | 1.2 → 0.9 (-25%) | Competition, market saturation |
| **Phase 3** | 67-100% | Accelerated Growth | 0.9 → 1.4 (+56%) | Innovation, market expansion |

### **Market Events & Seasonal Patterns**

| Event | Timing | Frequency Boost | Size Boost | Impact |
|-------|--------|----------------|------------|--------|
| **Black Friday Weekend** | Last Fri-Mon in Nov | 4.0× | 1.4× | Major shopping event |
| **Christmas Shopping** | Dec 1-25 | 1.2×-2.0× | 1.2× | Progressive weekly increases |
| **Memorial Day** | Last Mon in May | 1.5× | 1.3× | Outdoor season start |
| **Back-to-School** | Aug 15-31 | 1.3× | 1.2× | Kitchen equipment boost |
| **New Year Resolutions** | Jan 2-15 | 1.4× | 1.1× | Fitness/outdoor goals |
| **Post-Holiday Lull** | Jan 16-31 | 0.7× | 0.9× | Reduced activity |

### **Customer Tier Amplification**

**Higher tiers are more responsive** to growth and decline patterns:

| Customer Type | Tiers | Growth Amplifier | Notes |
|---------------|-------|-----------------|-------|
| **Individual** | Standard/Premium/VIP | 1.0×/1.3×/1.6× | Consumer progression |
| **Business** | SMB/Premier/Partner | 1.2×/1.5×/1.6× | Partner tier highest |
| **Government** | Federal/State/Local | 0.8×/0.7×/0.6× | Less responsive |

### **Growth Analytics**

**Camping and Kitchen generators** (both enhanced) provide detailed growth tracking:
- Phase progression monitoring
- Market event impact analysis  
- Customer tier response patterns
- Order frequency and size adjustments

**Ski generator**: Standard patterns (growth enhancement baseline for comparison)

## �🛠️ Examples

### **Production-Scale Testing**
```bash
# Recommended: Comprehensive 6-year dataset (auto-calculates dates to today)
python main_generate_sales.py

# Full year for analytics (example)
python main_generate_sales.py -s 2025-01-01 -e 2025-12-31
```

### **Domain-Specific Testing**
```bash
# Test camping seasonality (spring season)
python main_generate_sales.py -s 2025-03-01 -e 2025-05-31 --camping-only

# Kitchen holiday patterns  
python main_generate_sales.py -s 2024-11-01 -e 2024-12-31 --kitchen-only

# Ski peak season
python main_generate_sales.py -s 2024-12-01 -e 2025-02-28 --ski-only
```

### **Business Growth Testing**
```bash
# Test complete growth cycle with analytics
python main_generate_sales.py -s 2025-01-01 -e 2025-12-31 --enable-growth

# Growth patterns for camping only
python main_generate_sales.py -s 2025-01-01 -e 2025-12-31 --enable-growth --camping-only

# Test market events (Black Friday impact)
python main_generate_sales.py -s 2025-11-20 -e 2025-12-05 --enable-growth

# Compare growth vs standard patterns
python main_generate_sales.py -s 2025-01-01 -e 2025-06-30  # Standard
python main_generate_sales.py -s 2025-01-01 -e 2025-06-30 --enable-growth  # Growth
```

### **Revenue Trend Graphing**
```bash
# Generate and view revenue trends for all domains
python main_generate_sales.py --graph

# Graph specific domain with growth patterns
python main_generate_sales.py --enable-growth --graph --camping-only

# Generate comprehensive growth analysis with visualization
python main_generate_sales.py -s 2025-01-01 -e 2025-12-31 --enable-growth --graph
```

## 📊 Understanding the Output

### **Sales Files (per domain)**
- **Order_Samples_[Domain].csv**: Main orders with totals, customer, status
- **OrderLine_Samples_[Domain].csv**: Product line items with quantities  
- **OrderPayment_[Domain].csv**: Payment methods and amounts

### **Finance Files (per domain)**  
- **Invoice_Samples_[Domain].csv**: Invoices (generated day after order)
- **Payment_Samples_[Domain].csv**: Payments (immediate - eCommerce model)
- **Account_Samples_[Domain].csv**: Customer accounts (zero balance)

### **Key Relationships**
```
Customer → Order → OrderLine → Products
           ↓
        Invoice → Payment
           ↓
        Account (Receivables)
```

## 🔧 Domain Utilities

### **ProductCategory Generation**
```bash
# Extract categories from products and create platform-specific files
python utils/create_category_from_product.py
```
**Output**: ProductCategory_Samples_Camping.csv, ProductCategory_Samples_Kitchen.csv, ProductCategory_Samples_Ski.csv

### **File Consolidation**
```bash
# Combine all Product and ProductCategory files
python utils/consolidate_product_domain_input.py
```
**Output**: Product_Samples_Combined.csv, ProductCategory_Samples_Combined.csv

## 🎯 Key Features

### **Revenue Trend Visualization**
**NEW**: Generate interactive revenue trend graphs with `--graph` flag:
- **Monthly aggregation**: Clear trends without daily noise for multi-year analysis
- **Dual-panel graphs**: Individual domain trends + combined total revenue  
- **Business growth indicators**: Camping & Kitchen* show 3-phase growth pattern analysis
- **Visual distinction**: Solid lines (growth-enabled) vs dashed lines (standard)
- **Trend analysis**: Quadratic trend line and phase-by-phase statistics
- **High-resolution export**: PNG graphs saved to output folder
- **Requirements**: matplotlib, pandas, and numpy

### **Automated Infrastructure Deployment**
- **Automatic file copying**: All CSV files copied to `../../infra/data/` after generation
- **Input data**: Copied to `infra/data/shared/` (customers, products, reference data)
- **Output data**: Copied to `infra/data/sample_*/` (preserving folder structure)
- **Summary documentation**: Comprehensive summary with statistics copied to `infra/data/sample_sales_data_summary.md`
- **Overwrite protection**: Existing files are automatically overwritten

### **100% Schema Compliance**
- All CSV files match Microsoft Fabric Delta Lake schemas exactly
- CreatedBy field populated with "SampleGen"
- No deprecated fields (PaymentNumber removed)
- Proper foreign key relationships maintained

### **Platform Independence**  
- Directory structure: `sample_[domain]` (not platform-specific)
- File naming: `*_Samples_[Domain].csv` (consistent across all domains)
- Business logic separated from deployment platform

### **Hierarchical Customer System**
- **CustomerTypeId**: Individual | Business | Government
- **CustomerRelationshipTypeId**: Specific tier within type
- Extensible design for new customer types

## ⚠️ Important Notes

### **Data Consistency**
- **Same 513 customers** across all domains
- **Unique order numbering**: F100000+ (Camping), D200000+ (Kitchen), S300000+ (Ski)
- **Realistic FK relationships** between all tables

### **Performance**
- **Small datasets** (1 week): ~30 seconds + file copying
- **Large datasets** (1+ years): ~2-5 minutes + file copying
- **Generated volume**: Realistic business data with proper relationships

## 📈 Use Cases

### **Business Intelligence**
- Multi-domain revenue analysis and trends
- Customer segmentation across product categories
- Seasonal pattern analysis and forecasting

### **Data Engineering**
- Microsoft Fabric lakehouse testing
- ETL pipeline development and validation
- Delta Lake schema compliance testing

### **Analytics & Machine Learning**
- Customer lifetime value modeling
- Demand forecasting across seasons
- Cross-domain purchase behavior analysis

## 🎯 Best Practices

1. **Start with consolidated files**: Use `utils/` to generate and consolidate input files first
2. **Test incrementally**: Start with short date ranges before large datasets
3. **Use domain filters**: Generate single domains for focused testing
4. **Infrastructure ready**: Generated data is automatically copied to `infra/data/` for deployment
5. **Verify schema compliance**: All outputs are Microsoft Fabric ready
6. **Plan for scale**: Large date ranges generate substantial data volumes

---

**Enterprise Ready**: This system generates schema-compliant data with automated infrastructure deployment, suitable for Microsoft Fabric, Azure Databricks, and Snowflake environments. All data maintains referential integrity and realistic business patterns.
