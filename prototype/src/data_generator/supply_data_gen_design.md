# Supply Chain Data Generation Design Document

## Overview

This document defines the approach for generating supply chain data that integrates with existing sales data and supports inventory management and supplier relationship tracking for the eCommerce business.

## Data Dependencies

### Input Data Sources

**Existing Sales Data (Primary Driver):**
- `C:\Repos\Explore\udf_solutions\prototype\src\data_generator\output\camping\sales`
- `C:\Repos\Explore\udf_solutions\prototype\src\data_generator\output\kitchen\sales`  
- `C:\Repos\Explore\udf_solutions\prototype\src\data_generator\output\ski\sales`

**Reference Data (Supporting):**
- `C:\Repos\Explore\udf_solutions\prototype\src\data_generator\input\Product_Samples_*.csv`
- `C:\Repos\Explore\udf_solutions\prototype\src\data_generator\input\ProductCategory_Samples_*.csv`
- `C:\Repos\Explore\udf_solutions\prototype\src\data_generator\input\Customer_Samples.csv`

**Supply Chain Configuration:**
- `C:\Repos\Explore\udf_solutions\prototype\src\data_generator\input\suppliers.json` - Master supplier configuration with backup relationships

**Exclusions:**
- Finance data will NOT be used for supply chain generation

## Target Schema Generation

### model_suppliers.ipynb (3 Tables)
1. **Suppliers** - Supplier master data with backup relationships  
2. **ProductSuppliers** - Product-supplier mappings with pricing/terms
3. **SupplyChainEvents** - Disruption events and impact tracking

### model_inventory.ipynb (4 Tables)
1. **Inventory** - Current stock levels by product/location
2. **InventoryTransactions** - Stock movement audit trail
3. **PurchaseOrders** - Purchase order headers
4. **PurchaseOrderItems** - Purchase order line items

## Business Logic Design

### Supplier Configuration

**Primary Suppliers (by Category):**
- Contoso Camping Equipment → Camping products (Active)
- Contoso Kitchen → Kitchen products (Active)  
- Contoso Ski Equipment → Ski products (Active)

**Backup Suppliers:**
- Worldwide Importers → Backup for ALL categories (Camping, Kitchen, Ski)
- Fabrikam → Backup for Ski products ONLY

**Supplier Attributes:**
- Lead times: 7-21 days (Primary), 14-35 days (Backup)
- Reliability scores: 85-95 (Primary), 70-85 (Backup)
- Locations: Mix of domestic and international
- Status: Active, Disrupted, Inactive

### Data Generation Strategy

#### Phase 1: Supplier Foundation
1. **Load Supplier Configuration**: Read supplier definitions from `suppliers.json` including:
   - 5 base suppliers (3 primary Contoso brands + 2 backup suppliers)
   - Backup relationships and hierarchy
   - Business parameters (lead times, reliability scores, locations)
2. **Generate Suppliers Table**: Populate from JSON configuration with timestamps
3. **Create Product-Supplier Mappings**: Link products to appropriate suppliers by category
4. **Define Wholesale Costs**: Calculate 60-80% of retail prices from sales data
5. **Set Order Parameters**: Minimum/maximum order quantities based on product characteristics

#### Phase 2: Inventory Management  
1. **Current Inventory Levels:**
   - Analyze sales velocity from historical data
   - Calculate safety stock levels (2-4 weeks of average sales)
   - Generate realistic stock levels with some products low/out of stock

2. **Purchase Orders:**
   - Generate orders based on inventory reorder points
   - Link to suppliers from Phase 1
   - Include both regular replenishment and emergency orders

3. **Inventory Transactions:**
   - Generate inbound receipts from purchase orders
   - Generate outbound shipments matching sales data patterns
   - Include adjustments for damaged goods, returns, etc.

#### Phase 3: Supply Chain Events
1. **Disruption Events:**
   - Weather impacts (seasonal patterns)
   - Supplier-specific issues (quality, capacity)
   - Transport delays (shipping, customs)
   - Economic factors (material shortages, price increases)

2. **Impact Modeling:**
   - Link events to affected suppliers/products
   - Generate realistic delay and cost impacts
   - Create mitigation actions and recovery timelines

## Technical Implementation Plan

### Data Generation Flow

```
Sales Data (Historical) 
    ↓
Product Analysis (volumes, patterns)
    ↓
Supplier Assignment (category-based)
    ↓
Inventory Calculation (safety stocks)
    ↓
Purchase Order Generation (reorder logic)
    ↓
Transaction History (receipts, shipments)
    ↓
Disruption Events (realistic scenarios)
```

### File Structure
```
data_generator/
├── generate_suppliers.py       # Supplier master data
├── generate_inventory.py       # Inventory tables  
├── generate_supply_events.py   # Disruption events
├── main_generate_supplychain.py # Orchestrator
└── output/
    ├── suppliers/              # Supplier CSV files
    └── inventory/              # Inventory CSV files
```

### Integration Points

**With Existing Sales Data:**
- Product IDs must match existing product catalog
- Sales velocities drive inventory calculations  
- Order patterns influence purchase order timing

**With Reference Data:**
- Use product samples for supplier assignments
- Leverage product categories for supplier specialization
- Maintain consistency with existing data patterns

**Date Alignment:**
- Supply chain events should align with sales date ranges
- Inventory snapshots should reflect realistic stock levels
- Purchase orders should precede sales spikes appropriately

## Success Criteria

1. **Data Consistency:** All foreign keys resolve correctly to existing products
2. **Business Logic:** Inventory levels support observed sales patterns  
3. **Realism:** Supplier relationships reflect actual industry practices
4. **Completeness:** All 7 supply chain tables populated with meaningful data
5. **Integration:** Supply chain data enhances sales/inventory analysis capabilities

## Next Steps

1. Review and validate this design approach
2. Implement Phase 1 (Suppliers) first for validation
3. Test data quality and business logic correctness  
4. Proceed to Phase 2 (Inventory) and Phase 3 (Events)
5. Create main orchestrator to generate complete supply chain dataset

---

*Document Version: 1.0*  
*Created: March 2, 2026*
*Author: Supply Chain Data Generation Team*