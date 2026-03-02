"""
Product Category Generation Utility

This utility creates ProductCategory CSV files for different platforms by extracting 
unique categories from product data and formatting them according to the schema.

Features:
1. Extracts unique categories from Product_Samples_Combined.csv
2. Generates ProductCategory_Samples_Fabric.csv
3. Generates ProductCategory_Samples_ADB.csv (updates existing)
4. Generates ProductCategory_Samples_Snow.csv
5. Follows the standard ProductCategory schema format

Usage:
    python create_category_from_product.py
"""

import pandas as pd
import os
import sys
from pathlib import Path

# Configuration
INPUT_DIR = "../input"
OUTPUT_DIR = "../input"

# File configuration
PRODUCT_COMBINED_FILE = "Product_Samples_Combined.csv"
OUTPUT_FILES = {
    "camping": "ProductCategory_Samples_Camping.csv",
    "kitchen": "ProductCategory_Samples_Kitchen.csv", 
    "ski": "ProductCategory_Samples_Ski.csv"
}

# Brand mappings
BRAND_MAPPINGS = {
    "Contoso Camping": {
        "platform": "camping",
        "parent_id": "Parent_1",
        "logo_url": "https://contoso.com/camping-logo.png",
        "description_suffix": "for outdoor camping and adventure activities."
    },
    "Contoso Kitchen": {
        "platform": "kitchen",
        "parent_id": "Parent_2", 
        "logo_url": "https://contoso.com/kitchen-logo.png",
        "description_suffix": "for home and business kitchens."
    },
    "Contoso Ski Sportswear": {
        "platform": "ski",
        "parent_id": "Parent_3",
        "logo_url": "https://contoso.com/ski-logo.png",
        "description_suffix": "for winter sports and cold weather activities."
    }
}


def get_file_path(filename, directory=INPUT_DIR):
    """Get the full path for a file in the specified directory."""
    script_dir = Path(__file__).parent
    return script_dir / directory / filename


def load_product_data():
    """Load the combined product data."""
    product_file = get_file_path(PRODUCT_COMBINED_FILE)
    
    if not product_file.exists():
        print(f"❌ Product file not found: {product_file}")
        print("   Please run consolidate_product_domain_input.py first")
        return None
    
    try:
        df = pd.read_csv(product_file)
        print(f"✅ Loaded {len(df)} products from combined file")
        return df
    except Exception as e:
        print(f"❌ Error loading product file: {e}")
        return None


def extract_categories_by_brand(df):
    """Extract unique categories grouped by brand."""
    categories_by_brand = {}
    
    for brand in BRAND_MAPPINGS.keys():
        brand_products = df[df['BrandName'] == brand]
        
        if len(brand_products) > 0:
            # Get unique categories for this brand
            unique_categories = brand_products[['ProductCategoryID', 'CategoryName']].drop_duplicates()
            unique_categories = unique_categories.sort_values('ProductCategoryID')
            
            categories_by_brand[brand] = unique_categories
            print(f"   {brand}: {len(unique_categories)} unique categories")
        
    return categories_by_brand


def create_category_dataframe(categories, brand_name):
    """Create a ProductCategory DataFrame for a specific brand."""
    brand_info = BRAND_MAPPINGS[brand_name]
    
    category_data = []
    
    for _, row in categories.iterrows():
        category_record = {
            'CategoryID': row['ProductCategoryID'],
            'ParentCategoryId': brand_info['parent_id'],
            'CategoryName': row['CategoryName'],
            'CategoryDescription': f"{row['CategoryName']} {brand_info['description_suffix']}",
            'BrandName': brand_name,
            'BrandLogoUrl': brand_info['logo_url'],
            'IsActive': True
        }
        category_data.append(category_record)
    
    return pd.DataFrame(category_data)


def write_category_file(df, platform, brand_name):
    """Write a category DataFrame to the appropriate output file."""
    output_file = OUTPUT_FILES[platform]
    output_path = get_file_path(output_file, OUTPUT_DIR)
    
    try:
        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the CSV file
        df.to_csv(output_path, index=False)
        
        print(f"   ✅ {output_file} created with {len(df)} categories")
        print(f"      📁 Location: {output_path}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error writing {output_file}: {e}")
        return False


def generate_category_files(categories_by_brand):
    """Generate all ProductCategory files."""
    print("\n🎯 Generating ProductCategory Files")
    print("=" * 50)
    
    success_count = 0
    
    for brand_name, categories in categories_by_brand.items():
        platform = BRAND_MAPPINGS[brand_name]['platform']
        
        print(f"\n📂 Processing {brand_name} ({platform})...")
        
        # Create category DataFrame
        category_df = create_category_dataframe(categories, brand_name)
        
        # Write to file
        if write_category_file(category_df, platform, brand_name):
            success_count += 1
    
    return success_count == len(categories_by_brand)


def validate_output_files():
    """Validate that all output files were created successfully."""
    print("\n🔍 Validating Output Files")
    print("=" * 30)
    
    all_valid = True
    
    for platform, filename in OUTPUT_FILES.items():
        file_path = get_file_path(filename, OUTPUT_DIR)
        
        if file_path.exists():
            try:
                df = pd.read_csv(file_path)
                print(f"   ✅ {filename}: {len(df)} categories")
            except Exception as e:
                print(f"   ❌ {filename}: Error reading file - {e}")
                all_valid = False
        else:
            print(f"   ❌ {filename}: File not found")
            all_valid = False
    
    return all_valid


def main():
    """Main category generation orchestrator."""
    print("🏷️  Product Category Generation Utility")
    print("=" * 60)
    
    # Load product data
    print("📂 Loading Product Data...")
    product_df = load_product_data()
    if product_df is None:
        sys.exit(1)
    
    # Extract categories by brand
    print("\n🎯 Extracting Categories by Brand...")
    categories_by_brand = extract_categories_by_brand(product_df)
    
    if not categories_by_brand:
        print("❌ No categories found!")
        sys.exit(1)
    
    # Generate category files
    success = generate_category_files(categories_by_brand)
    
    if not success:
        print("\n❌ Some files failed to generate!")
        sys.exit(1)
    
    # Validate output
    validation_success = validate_output_files()
    
    # Final summary
    print("\n" + "=" * 60)
    if validation_success:
        print("🎉 All ProductCategory files generated successfully!")
        
        # Show file locations
        print("\n📁 Generated Files:")
        for platform, filename in OUTPUT_FILES.items():
            file_path = get_file_path(filename, OUTPUT_DIR)
            print(f"   {filename}: {file_path}")
            
        print(f"\n📂 Files available in: {get_file_path('', OUTPUT_DIR)}")
        print("\nℹ️  These files are now ready for use with your consolidation utility")
        
    else:
        print("❌ Some validation checks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()