"""
Supply Chain Data Generator - Inventory Module

This module generates sample data for inventory-related tables:
- Inventory: Current stock levels and warehouse locations
- InventoryTransactions: Stock movement audit trail
- PurchaseOrders: Purchase order headers
- PurchaseOrderItems: Purchase order line items

Uses existing sales data to calculate realistic inventory levels and purchase patterns.
Integrates with supplier data for purchase order generation.
"""

import pandas as pd
import json
import random
from datetime import datetime, timedelta, date
from pathlib import Path
import os
import glob
from collections import defaultdict


class InventoryDataGenerator:
    
    def __init__(self, base_path=None, start_date=None, end_date=None):
        """Initialize the inventory data generator.
        
        Args:
            base_path (str): Base path to the data_generator directory
            start_date (str): Start date for analysis (YYYY-MM-DD)
            end_date (str): End date for analysis (YYYY-MM-DD)
        """
        if base_path is None:
            self.base_path = Path(__file__).parent
        else:
            self.base_path = Path(base_path)
            
        self.input_path = self.base_path / "input"
        self.output_path = self.base_path / "output"
        
        # Set date range for analysis
        if start_date and end_date:
            self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            self.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            # Default to recent period
            self.end_date = date.today()
            self.start_date = self.end_date - timedelta(days=365)
            
        # Create output directories
        self.inventory_output = self.output_path / "inventory"
        self.inventory_output.mkdir(parents=True, exist_ok=True)
        
        # Load data
        self.sales_data = self._load_sales_data()
        self.suppliers_data = self._load_suppliers_data()
        self.products_data = self._load_products_data()
        
        print(f"✅ Inventory generator initialized")
        print(f"📁 Input: {self.input_path}")
        print(f"📁 Output: {self.inventory_output}")
        print(f"📅 Date range: {self.start_date} to {self.end_date}")
        
    def _load_sales_data(self):
        """Load sales data from all categories to analyze demand patterns."""
        sales_data = []
        
        # Load sales data from each category
        for category in ['camping', 'kitchen', 'ski']:
            sales_path = self.output_path / category / "sales"
            if sales_path.exists():
                # Load OrderLine files (have ProductId and Quantity)
                orderline_files = list(sales_path.glob("*OrderLine*.csv"))
                order_files = list(sales_path.glob("*Order_Samples*.csv"))
                
                for orderline_file in orderline_files:
                    if orderline_file.stat().st_size > 0:  # Skip empty files
                        try:
                            # Load order lines
                            df_orderlines = pd.read_csv(orderline_file)
                            
                            # Load corresponding order file for dates
                            order_file = None
                            for order_f in order_files:
                                if category.title() in order_f.name:
                                    order_file = order_f
                                    break
                                    
                            if order_file and order_file.exists():
                                df_orders = pd.read_csv(order_file)
                                
                                # Join orderlines with orders to get dates
                                df_combined = df_orderlines.merge(
                                    df_orders[['OrderId', 'OrderDate']], 
                                    on='OrderId', 
                                    how='left'
                                )
                                df_combined['Category'] = category.title()
                                sales_data.append(df_combined)
                                print(f"📊 Loaded {len(df_combined)} {category} sales line items")
                            else:
                                # Use orderlines without dates
                                df_orderlines['Category'] = category.title()
                                sales_data.append(df_orderlines)
                                print(f"📊 Loaded {len(df_orderlines)} {category} orderlines (no dates)")
                                
                        except Exception as e:
                            print(f"⚠️  Error loading {orderline_file}: {e}")
                            
        if sales_data:
            combined_sales = pd.concat(sales_data, ignore_index=True)
            print(f"📈 Total sales line items: {len(combined_sales)}")
            return combined_sales
        else:
            print("⚠️  No sales data found - will use default patterns")
            return pd.DataFrame()
            
    def _load_suppliers_data(self):
        """Load generated supplier data."""
        suppliers_path = self.output_path / "suppliers"
        
        suppliers_data = {}
        
        # Load suppliers
        suppliers_file = suppliers_path / "Suppliers.csv"
        if suppliers_file.exists():
            suppliers_data['suppliers'] = pd.read_csv(suppliers_file)
            print(f"🏭 Loaded {len(suppliers_data['suppliers'])} suppliers")
            
        # Load product-supplier mappings
        product_suppliers_file = suppliers_path / "ProductSuppliers.csv"
        if product_suppliers_file.exists():
            suppliers_data['product_suppliers'] = pd.read_csv(product_suppliers_file)
            print(f"🔗 Loaded {len(suppliers_data['product_suppliers'])} product-supplier mappings")
            
        return suppliers_data
        
    def _load_products_data(self):
        """Load product data."""
        combined_file = self.input_path / "Product_Samples_Combined.csv"
        if combined_file.exists():
            df = pd.read_csv(combined_file)
            print(f"📦 Loaded {len(df)} products from combined file")
            return df
        else:
            print("⚠️  No product data found")
            return pd.DataFrame()
            
    def _analyze_sales_velocity(self):
        """Analyze sales velocity to determine inventory needs."""
        if self.sales_data.empty:
            # Return default patterns if no sales data
            return {
                'default_monthly_sales': 50,
                'default_safety_stock': 100,
                'seasonal_multiplier': 1.0
            }
            
        # Convert order date to datetime if needed
        if 'OrderDate' in self.sales_data.columns:
            self.sales_data['OrderDate'] = pd.to_datetime(self.sales_data['OrderDate'])
        elif 'Order Date' in self.sales_data.columns:
            self.sales_data['OrderDate'] = pd.to_datetime(self.sales_data['Order Date'])
            
        # Analyze by product
        velocity_analysis = {}
        
        # Group by ProductId and calculate monthly sales
        if 'ProductId' in self.sales_data.columns and 'Quantity' in self.sales_data.columns:
            product_sales = self.sales_data.groupby('ProductId').agg({
                'Quantity': 'sum',
                'OrderDate': ['min', 'max', 'count']
            }).reset_index()
            
            product_sales.columns = ['ProductId', 'TotalQuantity', 'FirstSale', 'LastSale', 'OrderCount']
            
            for _, row in product_sales.iterrows():
                product_id = row['ProductId']
                total_qty = row['TotalQuantity']
                
                # Calculate monthly average
                if pd.notna(row['FirstSale']) and pd.notna(row['LastSale']):
                    days_active = max((row['LastSale'] - row['FirstSale']).days, 30)
                    monthly_sales = (total_qty / days_active) * 30
                else:
                    monthly_sales = total_qty / 12  # Assume 1 year if no dates
                
                velocity_analysis[product_id] = {
                    'monthly_sales': max(monthly_sales, 1),  # At least 1 per month
                    'total_sales': total_qty,
                    'order_count': row['OrderCount']
                }
                
        print(f"📊 Analyzed velocity for {len(velocity_analysis)} products")
        return velocity_analysis
        
    def generate_inventory_table(self):
        """Generate current inventory levels based on sales patterns."""
        
        inventory_data = []
        inventory_id = 1
        
        # Analyze sales velocity
        velocity_data = self._analyze_sales_velocity()
        
        # Warehouse locations
        warehouse_locations = ['Main', 'Backup', 'Regional']
        warehouse_weights = [0.7, 0.2, 0.1]  # Main gets most inventory
        
        # Process each product
        for _, product in self.products_data.iterrows():
            product_id = product.get('ProductID', inventory_id * 100)
            product_name = product.get('ProductName', product.get('Name', f'Product {product_id}'))
            category = product.get('Category', 'General')
            
            # Get velocity data for this product or use defaults
            if product_id in velocity_data:
                monthly_sales = velocity_data[product_id]['monthly_sales']
            else:
                monthly_sales = random.uniform(5, 50)  # Default range
                
            # Calculate inventory levels
            # Safety stock = 2-4 weeks of average sales
            safety_stock = int(monthly_sales * random.uniform(0.5, 1.0))
            reorder_point = int(safety_stock * random.uniform(1.2, 2.0))
            max_stock = int(monthly_sales * random.uniform(3, 6))  # 3-6 months supply
            
            # Current stock varies around reorder point
            current_stock = int(random.uniform(safety_stock * 0.5, max_stock * 1.2))
            
            # Some products are low/out of stock (10% chance)
            if random.random() < 0.1:
                current_stock = random.randint(0, safety_stock)
                
            # Reserved stock (for pending orders)
            reserved_stock = min(int(current_stock * random.uniform(0.1, 0.3)), current_stock)
            available_stock = current_stock - reserved_stock
            
            # Determine status
            if current_stock == 0:
                status = 'OutOfStock'
            elif current_stock <= safety_stock:
                status = 'LowStock'
            elif current_stock >= max_stock:
                status = 'Excess'
            else:
                status = 'Active'
                
            # Average cost (if we have supplier data)
            avg_cost = 0.0
            if 'product_suppliers' in self.suppliers_data:
                supplier_costs = self.suppliers_data['product_suppliers'][
                    self.suppliers_data['product_suppliers']['ProductID'] == product_id
                ]['WholesaleCost']
                if not supplier_costs.empty:
                    avg_cost = supplier_costs.mean()
                    
            if avg_cost == 0.0:
                # Estimate from retail price if available
                retail_price = product.get('Price', random.uniform(25, 500))
                avg_cost = float(retail_price) * random.uniform(0.65, 0.75)
                
            # Create record for main warehouse (most products)
            main_warehouse = random.choices(warehouse_locations, weights=warehouse_weights)[0]
            
            record = {
                'InventoryID': inventory_id,
                'ProductID': product_id,
                'ProductName': product_name,
                'ProductCategory': category,
                'WarehouseLocation': main_warehouse,
                'CurrentStock': current_stock,
                'ReservedStock': reserved_stock,
                'AvailableStock': available_stock,
                'SafetyStockLevel': safety_stock,
                'ReorderPoint': reorder_point,
                'MaxStockLevel': max_stock,
                'LastUpdated': (datetime.now() - timedelta(hours=random.randint(1, 48))).strftime('%Y-%m-%d %H:%M:%S'),
                'AverageCost': round(avg_cost, 2),
                'Status': status,
                'CreatedBy': 'system',
                'CreatedDate': (datetime.now() - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            inventory_data.append(record)
            inventory_id += 1
            
            # Some products also exist in backup warehouses (30% chance)
            if random.random() < 0.3 and main_warehouse != 'Backup':
                backup_stock = int(current_stock * random.uniform(0.2, 0.5))
                
                backup_record = record.copy()
                backup_record.update({
                    'InventoryID': inventory_id,
                    'WarehouseLocation': 'Backup',
                    'CurrentStock': backup_stock,
                    'ReservedStock': 0,
                    'AvailableStock': backup_stock,
                    'Status': 'Active' if backup_stock > 0 else 'OutOfStock'
                })
                
                inventory_data.append(backup_record)
                inventory_id += 1
                
        df_inventory = pd.DataFrame(inventory_data)
        
        # Save to CSV
        output_file = self.inventory_output / "Inventory.csv"
        df_inventory.to_csv(output_file, index=False)
        
        print(f"✅ Generated {len(df_inventory)} inventory records")
        print(f"💾 Saved to: {output_file}")
        
        return df_inventory
        
    def generate_purchase_orders_table(self, inventory_df, num_orders=20):
        """Generate purchase orders based on inventory levels."""
        
        po_data = []
        po_id = 1
        
        # Get supplier info
        if 'suppliers' not in self.suppliers_data:
            print("⚠️  No supplier data available for purchase orders")
            return pd.DataFrame()
            
        suppliers_df = self.suppliers_data['suppliers']
        
        # Generate orders over past 90 days
        for i in range(num_orders):
            order_date = datetime.now() - timedelta(days=random.randint(1, 90))
            
            # Select random supplier
            supplier = suppliers_df.sample(1).iloc[0]
            
            # Expected delivery based on supplier lead time
            lead_time = int(supplier['LeadTimeDays']) + random.randint(-2, 5)  # Some variation
            expected_delivery = order_date + timedelta(days=lead_time)
            
            # Some orders are delivered, some in progress
            if order_date < datetime.now() - timedelta(days=lead_time):
                # Should be delivered by now
                if random.random() < 0.9:  # 90% delivered on time
                    actual_delivery = expected_delivery + timedelta(days=random.randint(0, 3))
                    status = 'Delivered'
                else:
                    # Delayed
                    if random.random() < 0.7:
                        actual_delivery = expected_delivery + timedelta(days=random.randint(4, 14))
                        status = 'Delivered'
                    else:
                        actual_delivery = None
                        status = 'InTransit'
            else:
                # Still in progress
                actual_delivery = None
                status = random.choice(['Sent', 'Confirmed', 'InTransit'])
                
            # Order priority
            priority_weights = [0.6, 0.25, 0.12, 0.03]  # Low, Medium, High, Emergency
            priority = random.choices(['Low', 'Medium', 'High', 'Emergency'], weights=priority_weights)[0]
            
            record = {
                'PurchaseOrderID': po_id,
                'PurchaseOrderNumber': f"PO-{order_date.year}-{po_id:04d}",
                'SupplierID': supplier['SupplierID'],
                'SupplierName': supplier['SupplierName'],
                'OrderDate': order_date.strftime('%Y-%m-%d'),
                'ExpectedDeliveryDate': expected_delivery.strftime('%Y-%m-%d'),
                'ActualDeliveryDate': actual_delivery.strftime('%Y-%m-%d') if actual_delivery else None,
                'Status': status,
                'TotalOrderValue': 0.0,  # Will calculate from line items
                'DeliveryLocation': random.choice(['Main Warehouse', 'Backup Warehouse', 'Regional DC']),
                'OrderedBy': random.choice(['buyer1', 'buyer2', 'supply_manager']),
                'Priority': priority,
                'Notes': f"Order for {supplier['ProductCategory']} products" if supplier['ProductCategory'] != 'Multi' else "Multi-category order",
                'CreatedBy': 'system',
                'CreatedDate': order_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            po_data.append(record)
            po_id += 1
            
        df_purchase_orders = pd.DataFrame(po_data)
        
        # Save to CSV
        output_file = self.inventory_output / "PurchaseOrders.csv"
        df_purchase_orders.to_csv(output_file, index=False)
        
        print(f"✅ Generated {len(df_purchase_orders)} purchase orders")
        print(f"💾 Saved to: {output_file}")
        
        return df_purchase_orders
        
    def generate_purchase_order_items_table(self, po_df):
        """Generate purchase order line items."""
        
        if po_df.empty:
            return pd.DataFrame()
            
        po_items_data = []
        po_item_id = 1
        
        # Get product-supplier mappings
        if 'product_suppliers' not in self.suppliers_data:
            print("⚠️  No product-supplier mappings available")
            return pd.DataFrame()
            
        product_suppliers_df = self.suppliers_data['product_suppliers']
        
        for _, po in po_df.iterrows():
            supplier_id = po['SupplierID']
            po_id = po['PurchaseOrderID']
            po_number = po['PurchaseOrderNumber']
            po_status = po['Status']
            
            # Get products for this supplier
            supplier_products = product_suppliers_df[
                product_suppliers_df['SupplierID'] == supplier_id
            ]
            
            if supplier_products.empty:
                continue
                
            # Each PO has 1-5 line items
            num_items = random.randint(1, 5)
            sample_size = min(num_items, len(supplier_products))
            selected_products = supplier_products.sample(n=sample_size)
            
            po_total = 0.0
            
            for _, product in selected_products.iterrows():
                # Order quantity based on min/max order quantities
                min_qty = product.get('MinOrderQuantity', 10)
                max_qty = product.get('MaxOrderQuantity', 1000)
                if pd.isna(max_qty):
                    max_qty = min_qty * 10
                    
                quantity_ordered = random.randint(int(min_qty), int(min(max_qty, min_qty * 5)))
                
                unit_cost = product['WholesaleCost']
                line_total = quantity_ordered * unit_cost
                po_total += line_total
                
                # Quantity received depends on PO status
                if po_status == 'Delivered':
                    # Usually receive full quantity, sometimes partial
                    if random.random() < 0.9:
                        quantity_received = quantity_ordered
                        item_status = 'Received'
                        received_date = po.get('ActualDeliveryDate')
                    else:
                        quantity_received = random.randint(int(quantity_ordered * 0.7), quantity_ordered - 1)
                        item_status = 'Backordered'
                        received_date = po.get('ActualDeliveryDate')
                elif po_status in ['InTransit', 'Shipped']:
                    quantity_received = None
                    item_status = 'Shipped'
                    received_date = None
                else:
                    quantity_received = None
                    item_status = 'Pending'
                    received_date = None
                    
                record = {
                    'PurchaseOrderItemID': po_item_id,
                    'PurchaseOrderID': po_id,
                    'PurchaseOrderNumber': po_number,
                    'ProductID': product['ProductID'],
                    'ProductName': product['ProductName'],
                    'ProductCategory': product['ProductCategory'],
                    'QuantityOrdered': quantity_ordered,
                    'QuantityReceived': quantity_received,
                    'UnitCost': unit_cost,
                    'LineTotal': round(line_total, 2),
                    'Status': item_status,
                    'ExpectedDate': po['ExpectedDeliveryDate'],
                    'ReceivedDate': received_date,
                    'Notes': f"Supplier SKU: {product.get('SupplierProductCode', 'N/A')}",
                    'CreatedBy': 'system',
                    'CreatedDate': po['CreatedDate']
                }
                
                po_items_data.append(record)
                po_item_id += 1
                
            # Update PO total (would normally be calculated in real system)
            po_df.loc[po_df['PurchaseOrderID'] == po_id, 'TotalOrderValue'] = round(po_total, 2)
            
        df_po_items = pd.DataFrame(po_items_data)
        
        # Save to CSV
        output_file = self.inventory_output / "PurchaseOrderItems.csv"
        df_po_items.to_csv(output_file, index=False)
        
        print(f"✅ Generated {len(df_po_items)} purchase order line items")
        print(f"💾 Saved to: {output_file}")
        
        # Also re-save updated PO file with totals
        po_output_file = self.inventory_output / "PurchaseOrders.csv"
        po_df.to_csv(po_output_file, index=False)
        
        return df_po_items
        
    def generate_inventory_transactions_table(self, inventory_df, po_items_df, num_transactions=100):
        """Generate comprehensive inventory transaction history across full timeline."""
        
        transactions_data = []
        transaction_id = 1
        
        # Calculate realistic transaction count based on sales data and timeline
        days_in_range = (self.end_date - self.start_date).days
        
        # If we have sales data, base transactions on that volume
        if not self.sales_data.empty:
            sales_volume = len(self.sales_data)
            # Inventory transactions should be 2-3x sales volume (receipts, adjustments, transfers)
            calculated_transactions = min(sales_volume * 2, days_in_range * 15)  # Cap at 15 per day max
            actual_transactions = max(num_transactions, calculated_transactions)
            print(f"📈 Scaling inventory transactions based on {sales_volume:,} sales records")
            print(f"🔄 Generating {actual_transactions:,} transactions across {days_in_range} days")
        else:
            # Fallback: reasonable daily transaction rate
            actual_transactions = max(num_transactions, days_in_range * 5)  # 5 per day minimum
            print(f"📅 Generating {actual_transactions:,} transactions across {days_in_range} days")
        
        # Generate transactions evenly spread across the full date range
        for i in range(actual_transactions):
            # Spread transactions across entire date range, not just 90 days
            days_back = random.randint(0, days_in_range)
            transaction_date = self.end_date - timedelta(days=days_back)
            
            # Select random inventory record
            if inventory_df.empty:
                break
                
            inventory_record = inventory_df.sample(1).iloc[0]
            
            # Transaction types with weights
            transaction_types = ['Receipt', 'Sale', 'Adjustment', 'Transfer', 'Damage', 'Return']
            type_weights = [0.25, 0.45, 0.1, 0.1, 0.05, 0.05]
            
            transaction_type = random.choices(transaction_types, weights=type_weights)[0]
            
            # Generate transaction details based on type
            if transaction_type == 'Receipt':
                # Incoming from purchase orders
                quantity = random.randint(10, 200)
                unit_cost = inventory_record['AverageCost'] * random.uniform(0.95, 1.05)
                reason_code = 'Purchase Order Receipt'
                reference_number = f"PO-{random.randint(1000, 9999)}"
                
            elif transaction_type == 'Sale':
                # Outgoing to customers
                quantity = -random.randint(1, 50)
                unit_cost = inventory_record['AverageCost']
                reason_code = 'Customer Sale'
                reference_number = f"SO-{random.randint(10000, 99999)}"
                
            elif transaction_type == 'Adjustment':
                # Inventory corrections
                quantity = random.randint(-20, 20)
                unit_cost = inventory_record['AverageCost']
                reason_code = random.choice(['Cycle Count', 'Physical Count', 'System Correction'])
                reference_number = f"ADJ-{transaction_id}"
                
            elif transaction_type == 'Transfer':
                # Between warehouses
                quantity = -random.randint(5, 50)  # Outgoing from this location
                unit_cost = inventory_record['AverageCost']
                reason_code = 'Warehouse Transfer'
                reference_number = f"TRF-{random.randint(1000, 9999)}"
                
            elif transaction_type == 'Damage':
                # Damaged goods
                quantity = -random.randint(1, 10)
                unit_cost = inventory_record['AverageCost']
                reason_code = random.choice(['Shipping Damage', 'Warehouse Damage', 'Quality Issue'])
                reference_number = f"DMG-{transaction_id}"
                
            elif transaction_type == 'Return':
                # Customer returns
                quantity = random.randint(1, 5)
                unit_cost = inventory_record['AverageCost'] * 0.8  # Returns at lower value
                reason_code = 'Customer Return'
                reference_number = f"RET-{random.randint(10000, 99999)}"
                
            # Calculate before/after stock levels
            current_stock = inventory_record['CurrentStock']
            stock_before = random.randint(max(0, current_stock - 100), current_stock + 100)
            stock_after = stock_before + quantity
            
            total_value = quantity * unit_cost
            
            record = {
                'TransactionID': transaction_id,
                'ProductID': inventory_record['ProductID'],
                'ProductName': inventory_record['ProductName'],
                'ProductCategory': inventory_record['ProductCategory'],
                'WarehouseLocation': inventory_record['WarehouseLocation'],
                'TransactionType': transaction_type,
                'TransactionDate': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
                'Quantity': quantity,
                'UnitCost': round(unit_cost, 2),
                'TotalValue': round(total_value, 2),
                'ReferenceNumber': reference_number,
                'ReasonCode': reason_code,
                'StockBefore': stock_before,
                'StockAfter': stock_after,
                'ProcessedBy': random.choice(['warehouse1', 'warehouse2', 'system']),
                'Notes': f"Transaction processed for {inventory_record['WarehouseLocation']} location",
                'CreatedBy': 'system',
                'CreatedDate': transaction_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            transactions_data.append(record)
            transaction_id += 1
            
        df_transactions = pd.DataFrame(transactions_data)
        
        # Save to CSV
        output_file = self.inventory_output / "InventoryTransactions.csv"
        df_transactions.to_csv(output_file, index=False)
        
        print(f"✅ Generated {len(df_transactions)} inventory transactions")
        print(f"💾 Saved to: {output_file}")
        
        return df_transactions
        
    def generate_all_inventory_data(self, num_orders=25, num_transactions=150):
        """Generate all inventory-related data tables."""
        
        print("\n📦 Starting Inventory Data Generation...")
        print("=" * 50)
        
        # Generate each table
        df_inventory = self.generate_inventory_table()
        df_purchase_orders = self.generate_purchase_orders_table(df_inventory, num_orders)
        df_po_items = self.generate_purchase_order_items_table(df_purchase_orders)
        df_transactions = self.generate_inventory_transactions_table(df_inventory, df_po_items, num_transactions)
        
        print("\n📊 Generation Summary:")
        print(f"   Inventory: {len(df_inventory)} records")
        print(f"   PurchaseOrders: {len(df_purchase_orders)} records")
        print(f"   PurchaseOrderItems: {len(df_po_items)} records")
        print(f"   InventoryTransactions: {len(df_transactions)} records")
        
        print(f"\n💾 All files saved to: {self.inventory_output}")
        
        return {
            'inventory': df_inventory,
            'purchase_orders': df_purchase_orders,
            'purchase_order_items': df_po_items,
            'inventory_transactions': df_transactions
        }


def main():
    """Main function to run inventory data generation."""
    
    try:
        # Initialize generator
        generator = InventoryDataGenerator(
            start_date='2025-01-01',
            end_date='2026-03-02'
        )
        
        # Generate all data
        results = generator.generate_all_inventory_data(
            num_orders=30,
            num_transactions=200
        )
        
        print("\n🎉 Inventory data generation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {str(e)}")
        raise


if __name__ == "__main__":
    main()