"""
Supply Chain Data Generator - Suppliers Module

This module generates sample data for supplier-related tables:
- Suppliers: Master supplier data with backup relationships  
- ProductSuppliers: Product-supplier mappings with pricing and terms

Uses configuration from suppliers.json and existing product catalog.
Calculates realistic wholesale costs based on retail pricing patterns.
"""

import pandas as pd
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import os


class SupplierDataGenerator:
    
    def __init__(self, base_path=None):
        """Initialize the supplier data generator.
        
        Args:
            base_path (str): Base path to the data_generator directory
        """
        if base_path is None:
            self.base_path = Path(__file__).parent
        else:
            self.base_path = Path(base_path)
            
        self.input_path = self.base_path / "input"
        self.output_path = self.base_path / "output"
        
        # Create output directories
        self.suppliers_output = self.output_path / "suppliers"
        self.suppliers_output.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        self.suppliers_config = self._load_suppliers_config()
        self.products_data = self._load_products_data()
        
        print(f"✅ Supplier generator initialized")
        print(f"📁 Input: {self.input_path}")
        print(f"📁 Output: {self.suppliers_output}")
        
    def _load_suppliers_config(self):
        """Load supplier configuration from JSON file."""
        config_file = self.input_path / "suppliers.json"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Suppliers config file not found: {config_file}")
            
        with open(config_file, 'r') as f:
            config = json.load(f)
            
        print(f"📋 Loaded {len(config['suppliers'])} suppliers from config")
        return config
        
    def _load_products_data(self):
        """Load product data for supplier mappings."""
        products = {}
        
        # Load combined products if available, otherwise individual category files
        combined_file = self.input_path / "Product_Samples_Combined.csv"
        if combined_file.exists():
            df = pd.read_csv(combined_file)
            products['all'] = df
            print(f"📦 Loaded {len(df)} products from combined file")
        else:
            # Load individual category files
            for category in ['Camping', 'Kitchen', 'Ski']:
                file_path = self.input_path / f"Product_Samples_{category}.csv"
                if file_path.exists():
                    df = pd.read_csv(file_path)
                    products[category.lower()] = df
                    print(f"📦 Loaded {len(df)} {category} products")
                    
        if not products:
            raise FileNotFoundError("No product data files found in input directory")
            
        return products
        
    def generate_suppliers_table(self):
        """Generate the Suppliers table data."""
        
        suppliers_data = []
        
        for supplier in self.suppliers_config['suppliers']:
            # Add timestamp
            created_date = datetime.now() - timedelta(days=random.randint(30, 365))
            
            supplier_record = {
                'SupplierID': supplier['SupplierID'],
                'SupplierName': supplier['SupplierName'],
                'SupplierType': supplier['SupplierType'],
                'Status': supplier['Status'],
                'ProductCategory': supplier['ProductCategory'], 
                'PrimarySupplierID': supplier['PrimarySupplierID'],
                'LeadTimeDays': supplier['LeadTimeDays'],
                'ReliabilityScore': supplier['ReliabilityScore'],
                'Location': supplier['Location'],
                'ContactEmail': supplier['ContactEmail'],
                'CreatedBy': supplier['CreatedBy'],
                'CreatedDate': created_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            suppliers_data.append(supplier_record)
            
        df_suppliers = pd.DataFrame(suppliers_data)
        
        # Save to CSV
        output_file = self.suppliers_output / "Suppliers.csv"
        df_suppliers.to_csv(output_file, index=False)
        
        print(f"✅ Generated {len(df_suppliers)} supplier records")
        print(f"💾 Saved to: {output_file}")
        
        return df_suppliers
        
    def generate_product_suppliers_table(self):
        """Generate the ProductSuppliers mapping table."""
        
        product_supplier_data = []
        product_supplier_id = 1
        
        # Get all products from loaded data
        all_products = []
        for category, df in self.products_data.items():
            if category != 'all':  # Skip if we have combined data
                for _, product in df.iterrows():
                    all_products.append({
                        'ProductID': product.get('ProductID', product_supplier_id * 100),
                        'ProductName': product.get('ProductName', product.get('Name', f'Product {product_supplier_id}')),
                        'ProductCategory': category.title(),
                        'RetailPrice': product.get('Price', random.uniform(25, 500))
                    })
            else:  # Using combined data
                for _, product in df.iterrows():
                    all_products.append({
                        'ProductID': product.get('ProductID', product_supplier_id * 100),
                        'ProductName': product.get('ProductName', product.get('Name', f'Product {product_supplier_id}')),
                        'ProductCategory': product.get('Category', 'General'),
                        'RetailPrice': product.get('Price', random.uniform(25, 500))
                    })
                break  # Only process combined data once
                
        print(f"📦 Processing {len(all_products)} products for supplier mapping")
        
        # Create mappings for each product
        for product in all_products:
            category = product['ProductCategory'].lower()
            
            # Find suppliers for this product category
            category_suppliers = []
            for supplier in self.suppliers_config['suppliers']:
                supplier_category = supplier['ProductCategory'].lower()
                if supplier_category == 'multi' or supplier_category == category:
                    category_suppliers.append(supplier)
                    
            # Create primary supplier mapping
            primary_suppliers = [s for s in category_suppliers if s['SupplierType'] == 'Primary']
            if primary_suppliers:
                primary_supplier = primary_suppliers[0]  # Take first primary for category
                
                # Calculate wholesale cost (60-80% of retail)
                retail_price = float(product['RetailPrice'])
                wholesale_cost = retail_price * random.uniform(0.60, 0.80)
                
                # Generate supplier product code
                supplier_code = f"{primary_supplier['SupplierName'][:3].upper()}-{product['ProductID']}"
                
                record = {
                    'ProductSupplierID': product_supplier_id,
                    'ProductID': product['ProductID'],
                    'ProductName': product['ProductName'],
                    'ProductCategory': product['ProductCategory'],
                    'SupplierID': primary_supplier['SupplierID'],
                    'SupplierName': primary_supplier['SupplierName'],
                    'SupplierProductCode': supplier_code,
                    'WholesaleCost': round(wholesale_cost, 2),
                    'MinOrderQuantity': random.choice([1, 5, 10, 25, 50]),
                    'MaxOrderQuantity': random.choice([None, 1000, 5000, 10000]),
                    'LeadTimeDays': primary_supplier['LeadTimeDays'] + random.randint(-3, 3),
                    'Status': 'Active',
                    'CreatedBy': 'system',
                    'CreatedDate': (datetime.now() - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d %H:%M:%S')
                }
                
                product_supplier_data.append(record)
                product_supplier_id += 1
                
            # Also create backup supplier mappings (15% chance per backup supplier)
            backup_suppliers = [s for s in category_suppliers if s['SupplierType'] == 'Backup']
            for backup_supplier in backup_suppliers:
                if random.random() < 0.15:  # 15% chance
                    
                    # Backup suppliers typically cost more
                    retail_price = float(product['RetailPrice'])
                    wholesale_cost = retail_price * random.uniform(0.65, 0.85)
                    
                    supplier_code = f"{backup_supplier['SupplierName'][:3].upper()}-{product['ProductID']}"
                    
                    record = {
                        'ProductSupplierID': product_supplier_id,
                        'ProductID': product['ProductID'],
                        'ProductName': product['ProductName'],
                        'ProductCategory': product['ProductCategory'],
                        'SupplierID': backup_supplier['SupplierID'],
                        'SupplierName': backup_supplier['SupplierName'],
                        'SupplierProductCode': supplier_code,
                        'WholesaleCost': round(wholesale_cost, 2),
                        'MinOrderQuantity': random.choice([1, 10, 25, 50]),
                        'MaxOrderQuantity': random.choice([None, 500, 2000, 5000]),
                        'LeadTimeDays': backup_supplier['LeadTimeDays'] + random.randint(-5, 5),
                        'Status': 'Active',
                        'CreatedBy': 'system',
                        'CreatedDate': (datetime.now() - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    product_supplier_data.append(record)
                    product_supplier_id += 1
                    
        df_product_suppliers = pd.DataFrame(product_supplier_data)
        
        # Save to CSV
        output_file = self.suppliers_output / "ProductSuppliers.csv"
        df_product_suppliers.to_csv(output_file, index=False)
        
        print(f"✅ Generated {len(df_product_suppliers)} product-supplier mappings")
        print(f"💾 Saved to: {output_file}")
        
        return df_product_suppliers
        
    def generate_supply_chain_events_sample(self, num_events=10):
        """Generate sample supply chain events for testing."""
        
        events_data = []
        
        # Sample disruption scenarios
        event_templates = [
            {
                'DisruptionType': 'Weather',
                'EventName': 'Winter Storm Alpha',
                'Description': 'Major winter storm affecting transportation networks',
                'Severity': 'High',
                'GeographicArea': 'Northwestern USA',
                'IndustryImpact': 'Logistics'
            },
            {
                'DisruptionType': 'Supplier',
                'EventName': 'Factory Maintenance', 
                'Description': 'Scheduled maintenance at key supplier facility',
                'Severity': 'Medium',
                'GeographicArea': 'Regional',
                'IndustryImpact': 'Manufacturing'
            },
            {
                'DisruptionType': 'Economic',
                'EventName': 'Raw Material Shortage',
                'Description': 'Global shortage of key manufacturing materials',
                'Severity': 'Critical', 
                'GeographicArea': 'Global',
                'IndustryImpact': 'Manufacturing'
            }
        ]
        
        for i in range(num_events):
            template = random.choice(event_templates)
            start_date = datetime.now() - timedelta(days=random.randint(1, 90))
            
            # Some events are resolved, some ongoing
            if random.random() < 0.7:  # 70% resolved
                end_date = start_date + timedelta(days=random.randint(1, 30))
                status = 'Resolved'
                actual_duration = (end_date - start_date).days
            else:
                end_date = None
                status = random.choice(['Active', 'Monitoring'])
                actual_duration = None
                
            event = {
                'EventID': i + 1,
                'DisruptionType': template['DisruptionType'],
                'EventName': f"{template['EventName']} - {i+1}",
                'Description': template['Description'],
                'Severity': template['Severity'],
                'Status': status,
                'StartDate': start_date.strftime('%Y-%m-%d'),
                'EndDate': end_date.strftime('%Y-%m-%d') if end_date else None,
                'GeographicArea': template['GeographicArea'],
                'IndustryImpact': template['IndustryImpact'],
                'PredictedDuration': random.randint(3, 21),
                'ActualDuration': actual_duration,
                'AlertLevel': random.choice(['Yellow', 'Orange', 'Red']),
                'ReportedBy': 'Supply Chain Monitor',
                'CreatedBy': 'system',
                'CreatedDate': start_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            events_data.append(event)
            
        df_events = pd.DataFrame(events_data)
        
        # Save to CSV
        output_file = self.suppliers_output / "SupplyChainEvents.csv"
        df_events.to_csv(output_file, index=False)
        
        print(f"✅ Generated {len(df_events)} sample supply chain events")
        print(f"💾 Saved to: {output_file}")
        
        return df_events
        
    def generate_all_supplier_data(self, num_events=10):
        """Generate all supplier-related data tables."""
        
        print("\n🏭 Starting Supplier Data Generation...")
        print("=" * 50)
        
        # Generate each table
        df_suppliers = self.generate_suppliers_table()
        df_product_suppliers = self.generate_product_suppliers_table()
        df_events = self.generate_supply_chain_events_sample(num_events)
        
        print("\n📊 Generation Summary:")
        print(f"   Suppliers: {len(df_suppliers)} records")
        print(f"   ProductSuppliers: {len(df_product_suppliers)} records")
        print(f"   SupplyChainEvents: {len(df_events)} records")
        
        print(f"\n💾 All files saved to: {self.suppliers_output}")
        
        return {
            'suppliers': df_suppliers,
            'product_suppliers': df_product_suppliers, 
            'supply_chain_events': df_events
        }


def main():
    """Main function to run supplier data generation."""
    
    try:
        # Initialize generator
        generator = SupplierDataGenerator()
        
        # Generate all data
        results = generator.generate_all_supplier_data(num_events=15)
        
        print("\n🎉 Supplier data generation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {str(e)}")
        raise


if __name__ == "__main__":
    main()