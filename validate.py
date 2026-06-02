"""Validation script to test FreightcarchecK components."""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    try:
        import pandas as pd
        print("  ✓ pandas imported")
        
        import plotly.graph_objects as go
        print("  ✓ plotly imported")
        
        import numpy as np
        print("  ✓ numpy imported")
        
        from models import Train, Car, Cargo, HazmatInfo
        print("  ✓ models imported")
        
        from utils.calculations import calculate_total_tonnage, calculate_braking_ratio
        print("  ✓ calculations imported")
        
        from utils.filters import apply_filters
        print("  ✓ filters imported")
        
        from utils.visualizations import create_train_layout
        print("  ✓ visualizations imported")
        
        from utils.data_loader import load_sample_trains, trains_json_to_dataframe
        print("  ✓ data_loader imported")
        
        print("\n✅ All imports successful!\n")
        return True
    except Exception as e:
        print(f"\n❌ Import failed: {e}\n")
        return False


def test_data_generation():
    """Test data generation and loading."""
    print("🧪 Testing data generation...")
    try:
        import data_generator
        
        # Generate sample data
        trains = data_generator.generate_sample_trains(1)
        print(f"  ✓ Generated {len(trains)} sample train")
        
        train = trains[0]
        print(f"  ✓ Train ID: {train['train_id']}")
        print(f"  ✓ Total cars: {train['total_cars']}")
        print(f"  ✓ Total weight: {train['total_weight_tons']} tons")
        
        # Count hazmat
        hazmat_count = sum(1 for car in train['cars'] if car['cargo']['hazmat_info']['is_hazmat'])
        print(f"  ✓ Hazmat cars: {hazmat_count}")
        
        print("\n✅ Data generation successful!\n")
        return True
    except Exception as e:
        print(f"\n❌ Data generation failed: {e}\n")
        return False


def test_data_loading():
    """Test loading and processing generated data."""
    print("🧪 Testing data loading and calculations...")
    try:
        from utils.data_loader import load_sample_trains, trains_json_to_dataframe
        from utils.calculations import (
            calculate_total_tonnage,
            calculate_hazmat_tonnage,
            calculate_braking_ratio,
            get_weight_distribution,
        )
        
        # Load sample trains
        trains = load_sample_trains('data')
        if not trains:
            print("  ⚠️  No sample trains found. Generating...")
            import data_generator
            trains = data_generator.generate_sample_trains(1)
            Path('data').mkdir(exist_ok=True)
            import json
            with open('data/sample_trains.json', 'w') as f:
                json.dump(trains, f, indent=2)
        
        print(f"  ✓ Loaded {len(trains)} train(s)")
        
        # Convert to DataFrame
        df = trains_json_to_dataframe(trains)
        print(f"  ✓ Converted to DataFrame with {len(df)} cars")
        
        # Test calculations
        total_tons = calculate_total_tonnage(df)
        print(f"  ✓ Total tonnage: {total_tons} tons")
        
        hazmat_tons = calculate_hazmat_tonnage(df)
        print(f"  ✓ Hazmat tonnage: {hazmat_tons} tons")
        
        ratio = calculate_braking_ratio(hazmat_tons, total_tons)
        print(f"  ✓ Braking ratio: {ratio:.4f}")
        
        dist = get_weight_distribution(df)
        print(f"  ✓ Weight distribution: Front {dist['front']}%, Middle {dist['middle']}%, Rear {dist['rear']}%")
        
        print("\n✅ Data loading and calculations successful!\n")
        return True
    except Exception as e:
        print(f"\n❌ Data loading/calculations failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_filters():
    """Test filtering functionality."""
    print("🧪 Testing filters...")
    try:
        from utils.data_loader import load_sample_trains, trains_json_to_dataframe
        from utils.filters import apply_filters
        
        trains = load_sample_trains('data')
        if not trains:
            import data_generator
            trains = data_generator.generate_sample_trains(1)
        
        df = trains_json_to_dataframe(trains)
        
        # Test search
        filtered = apply_filters(df, search_term='Grain')
        print(f"  ✓ Search filter: Found {len(filtered)} cars with 'Grain'")
        
        # Test hazmat-only
        filtered = apply_filters(df, hazmat_only=True)
        print(f"  ✓ Hazmat filter: Found {len(filtered)} hazmat cars")
        
        # Test car type
        filtered = apply_filters(df, car_types=['tank'])
        print(f"  ✓ Car type filter: Found {len(filtered)} tank cars")
        
        print("\n✅ Filters working correctly!\n")
        return True
    except Exception as e:
        print(f"\n❌ Filter test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("  FreightcarchecK - Component Validation")
    print("=" * 60)
    print()
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Data Generation", test_data_generation()))
    results.append(("Data Loading", test_data_loading()))
    results.append(("Filters", test_filters()))
    
    print("=" * 60)
    print("  Validation Summary")
    print("=" * 60)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:.<40} {status}")
    print()
    
    if all(r[1] for r in results):
        print("🎉 All validations passed! Ready to run:")
        print("   python -m streamlit run app.py")
    else:
        print("⚠️  Some validations failed. Review errors above.")
    
    print()
