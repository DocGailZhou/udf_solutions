"""
Test ProductCategory Generation Results
"""

import pandas as pd
from pathlib import Path

def test_category_generation():
    """Test the category generation results."""
    print("🧪 Testing ProductCategory Generation Results")
    print("=" * 60)
    
    # File paths
    script_dir = Path(__file__).parent
    
    files_to_test = {
        "ProductCategory_Samples_Camping.csv": "Contoso Camping",
        "ProductCategory_Samples_Kitchen.csv": "Contoso Kitchen", 
        "ProductCategory_Samples_Ski.csv": "Contoso Ski Sportswear",
        "ProductCategory_Samples_Combined.csv": "All Brands"
    }
    
    total_categories = 0
    
    for filename, expected_brand in files_to_test.items():
        file_path = script_dir / "../input" / filename
        
        print(f"\n📂 Testing {filename}...")
        
        if not file_path.exists():
            print(f"   ❌ File not found!")
            continue
        
        try:
            df = pd.read_csv(file_path)
            
            # Basic statistics
            print(f"   📊 Categories: {len(df)}")
            
            # Check required columns
            required_columns = ['CategoryID', 'ParentCategoryId', 'CategoryName', 
                              'CategoryDescription', 'BrandName', 'BrandLogoUrl', 'IsActive']
            missing_cols = [col for col in required_columns if col not in df.columns]
            
            if missing_cols:
                print(f"   ❌ Missing columns: {missing_cols}")
                continue
            else:
                print("   ✅ All required columns present")
            
            # Check brands
            unique_brands = df['BrandName'].unique()
            print(f"   🏷️  Brands: {', '.join(unique_brands)}")
            
            # Check parent IDs
            unique_parents = df['ParentCategoryId'].unique()
            print(f"   👥 Parent IDs: {', '.join(unique_parents)}")
            
            # Check IsActive values
            active_count = df[df['IsActive'] == True].shape[0]
            print(f"   ✅ Active categories: {active_count}/{len(df)}")
            
            total_categories += len(df)
            
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
    
    print(f"\n📈 Summary:")
    print(f"   Total categories across all files: {total_categories}")
    print("   ✅ ProductCategory generation test completed!")

if __name__ == "__main__":
    test_category_generation()