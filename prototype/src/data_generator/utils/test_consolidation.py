"""
Test script for Product Domain Consolidation Utility
"""

import pandas as pd
from pathlib import Path

def test_consolidation():
    """Test the consolidation results."""
    print("🧪 Testing Product Domain Consolidation Results")
    print("=" * 60)
    
    # File paths
    script_dir = Path(__file__).parent
    combined_file = script_dir / "../input/Product_Samples_Combined.csv"
    
    if not combined_file.exists():
        print("❌ Combined file not found! Run consolidation utility first.")
        return
    
    # Load the combined file
    df = pd.read_csv(combined_file)
    
    # Basic statistics
    print(f"📊 Total products in combined file: {len(df)}")
    
    # Count by brand
    brand_counts = df['BrandName'].value_counts()
    print("\n🏷️  Products by Brand:")
    for brand, count in brand_counts.items():
        print(f"   {brand}: {count} products")
    
    # Count by category
    category_counts = df['CategoryName'].value_counts()
    print(f"\n📂 Product Categories: {len(category_counts)} unique categories")
    
    # Price range
    print(f"\n💰 Price Range:")
    print(f"   Minimum: ${df['ListPrice'].min():.2f}")
    print(f"   Maximum: ${df['ListPrice'].max():.2f}")
    print(f"   Average: ${df['ListPrice'].mean():.2f}")
    
    # Verify no duplicates
    duplicates = df.duplicated(subset=['ProductID']).sum()
    print(f"\n🔍 Data Quality:")
    if duplicates == 0:
        print("   ✅ No duplicate ProductIDs found")
    else:
        print(f"   ⚠️  {duplicates} duplicate ProductIDs found")
    
    print("\n✅ Product consolidation test completed!")

if __name__ == "__main__":
    test_consolidation()