"""
Product Domain Input Consolidation Utility

This utility consolidates product data from multiple CSV files into a single combined file.
It currently supports Product samples and can be extended for ProductCategory samples.

Features:
1. Consolidates Product_Samples_Camping.csv, Product_Samples_Kitchen.csv, Product_Samples_Ski.csv
2. Outputs to Product_Samples_Combined.csv
3. Extensible design for future ProductCategory consolidation
4. Maintains data integrity and original formatting

Usage:
    python consolidate_product_domain_input.py
"""

import pandas as pd
import os
import sys
from pathlib import Path

# Configuration
INPUT_DIR = "../input"
OUTPUT_DIR = "../input"  # Output to same directory for consistency

# Product consolidation configuration
PRODUCT_FILES = [
    "Product_Samples_Camping.csv",
    "Product_Samples_Kitchen.csv", 
    "Product_Samples_Ski.csv"
]
PRODUCT_OUTPUT_FILE = "Product_Samples_Combined.csv"

# ProductCategory consolidation configuration  
PRODUCT_CATEGORY_FILES = [
    "ProductCategory_Samples_Camping.csv",
    "ProductCategory_Samples_Kitchen.csv",
    "ProductCategory_Samples_Ski.csv"
]
PRODUCT_CATEGORY_OUTPUT_FILE = "ProductCategory_Samples_Combined.csv"


def get_file_path(filename, directory=INPUT_DIR):
    """Get the full path for a file in the specified directory."""
    script_dir = Path(__file__).parent
    return script_dir / directory / filename


def validate_files_exist(file_list, file_type="Product"):
    """Validate that all required input files exist."""
    missing_files = []
    for filename in file_list:
        file_path = get_file_path(filename)
        if not file_path.exists():
            missing_files.append(str(file_path))
    
    if missing_files:
        print(f"❌ Missing {file_type} files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    return True


def consolidate_csv_files(file_list, output_filename, domain_type="Product"):
    """
    Consolidate multiple CSV files into a single file.
    
    Args:
        file_list: List of input CSV filenames
        output_filename: Output CSV filename
        domain_type: Type of domain being consolidated (for logging)
    """
    print(f"🔄 Consolidating {domain_type} files...")
    
    # Validate input files exist
    if not validate_files_exist(file_list, domain_type):
        return False
    
    consolidated_data = []
    total_records = 0
    
    # Read and combine all files
    for filename in file_list:
        file_path = get_file_path(filename)
        print(f"   📄 Reading {filename}...")
        
        try:
            df = pd.read_csv(file_path)
            record_count = len(df)
            consolidated_data.append(df)
            total_records += record_count
            print(f"      ✅ Loaded {record_count} records")
            
        except Exception as e:
            print(f"      ❌ Error reading {filename}: {e}")
            return False
    
    # Combine all DataFrames
    if consolidated_data:
        combined_df = pd.concat(consolidated_data, ignore_index=True)
        
        # Write to output file
        output_path = get_file_path(output_filename, OUTPUT_DIR)
        try:
            combined_df.to_csv(output_path, index=False)
            print(f"   💾 Written {len(combined_df)} total records to {output_filename}")
            print(f"      📁 Output location: {output_path}")
            return True
            
        except Exception as e:
            print(f"   ❌ Error writing {output_filename}: {e}")
            return False
    else:
        print(f"   ❌ No data to consolidate for {domain_type}")
        return False


def consolidate_products():
    """Consolidate all product CSV files."""
    print("🎯 Product Domain Consolidation")
    print("=" * 50)
    
    success = consolidate_csv_files(
        PRODUCT_FILES, 
        PRODUCT_OUTPUT_FILE, 
        "Product"
    )
    
    if success:
        print("✅ Product consolidation completed successfully!")
    else:
        print("❌ Product consolidation failed!")
    
    return success


def consolidate_product_categories():
    """Consolidate all product category CSV files."""
    print("\n🎯 Product Category Domain Consolidation")
    print("=" * 50)
    
    # Check if any product category files are configured
    if not PRODUCT_CATEGORY_FILES or all(not file for file in PRODUCT_CATEGORY_FILES):
        print("ℹ️  Product Category consolidation not configured yet")
        print("   Run create_category_from_product.py first to generate category files")
        return True
    
    success = consolidate_csv_files(
        PRODUCT_CATEGORY_FILES,
        PRODUCT_CATEGORY_OUTPUT_FILE,
        "Product Category"
    )
    
    if success:
        print("✅ Product Category consolidation completed successfully!")
    else:
        print("❌ Product Category consolidation failed!")
    
    return success


def main():
    """Main consolidation orchestrator."""
    print("🔧 Product Domain Input Consolidation Utility")
    print("=" * 60)
    
    all_success = True
    
    # Consolidate Products
    product_success = consolidate_products()
    all_success = all_success and product_success
    
    # Consolidate Product Categories (future feature)
    category_success = consolidate_product_categories()
    all_success = all_success and category_success
    
    # Final summary
    print("\n" + "=" * 60)
    if all_success:
        print("🎉 All domain consolidation completed successfully!")
        print(f"📁 Combined files available in: {get_file_path('', OUTPUT_DIR)}")
    else:
        print("❌ Some consolidation operations failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()