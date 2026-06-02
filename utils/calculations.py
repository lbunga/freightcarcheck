"""Calculation utilities for train manifest analysis."""
import pandas as pd
from typing import Dict, List, Tuple


def calculate_total_tonnage(cars_df: pd.DataFrame) -> float:
    """Calculate total tonnage including car weight and cargo."""
    car_weights = {
        'flat': 30,
        'tank': 140,
        'gondola': 38,
        'box': 35,
        'hopper': 35,
    }
    
    total = 0
    for _, row in cars_df.iterrows():
        car_weight = car_weights.get(row['car_type'], 35)
        total += car_weight + row['cargo_weight_tons']
    
    return round(total, 2)


def calculate_hazmat_tonnage(cars_df: pd.DataFrame) -> float:
    """Calculate total hazmat cargo tonnage."""
    hazmat_df = cars_df[cars_df['is_hazmat'] == True]
    return round(hazmat_df['cargo_weight_tons'].sum(), 2)


def get_weight_distribution(cars_df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate weight distribution across train sections.
    Returns percentages for front (cars 1-50), middle (51-100), rear (101-150).
    """
    car_weights = {
        'flat': 30,
        'tank': 140,
        'gondola': 38,
        'box': 35,
        'hopper': 35,
    }
    
    def get_car_total_weight(row):
        car_weight = car_weights.get(row['car_type'], 35)
        return car_weight + row['cargo_weight_tons']
    
    cars_df_copy = cars_df.copy()
    cars_df_copy['total_weight'] = cars_df_copy.apply(get_car_total_weight, axis=1)
    
    total_weight = cars_df_copy['total_weight'].sum()
    
    if total_weight == 0:
        return {'front': 0.0, 'middle': 0.0, 'rear': 0.0}
    
    front = cars_df_copy[cars_df_copy['position'] <= 50]['total_weight'].sum()
    middle = cars_df_copy[(cars_df_copy['position'] > 50) & (cars_df_copy['position'] <= 100)]['total_weight'].sum()
    rear = cars_df_copy[cars_df_copy['position'] > 100]['total_weight'].sum()
    
    return {
        'front': round(front / total_weight * 100, 1),
        'middle': round(middle / total_weight * 100, 1),
        'rear': round(rear / total_weight * 100, 1),
    }


def calculate_braking_ratio(hazmat_tons: float, total_tons: float) -> float:
    """Calculate braking weight ratio: hazmat / total."""
    if total_tons == 0:
        return 0.0
    return round(hazmat_tons / total_tons, 4)


def get_hazmat_summary(cars_df: pd.DataFrame) -> Dict:
    """
    Get summary of hazmat by class.
    Returns dict with hazmat class as key, count and tonnage as values.
    """
    hazmat_df = cars_df[cars_df['is_hazmat'] == True]
    
    summary = {}
    for hazmat_class in sorted(hazmat_df['hazmat_class'].dropna().unique()):
        class_data = hazmat_df[hazmat_df['hazmat_class'] == hazmat_class]
        summary[f'Class {int(hazmat_class)}'] = {
            'count': len(class_data),
            'tonnage': round(class_data['cargo_weight_tons'].sum(), 2),
        }
    
    return summary
