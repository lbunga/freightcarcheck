"""Filtering and search utilities for train manifests."""
import pandas as pd
from typing import List, Optional


def filter_by_hazmat(cars_df: pd.DataFrame, hazmat_only: bool = False) -> pd.DataFrame:
    """Filter cars to show only hazmat or all cars."""
    if hazmat_only:
        return cars_df[cars_df['is_hazmat'] == True].reset_index(drop=True)
    return cars_df


def filter_by_hazmat_class(cars_df: pd.DataFrame, classes: List[int]) -> pd.DataFrame:
    """Filter cars by hazmat class (1-9)."""
    if not classes:
        return cars_df
    return cars_df[cars_df['hazmat_class'].isin(classes)].reset_index(drop=True)


def filter_by_car_type(cars_df: pd.DataFrame, car_types: List[str]) -> pd.DataFrame:
    """Filter cars by type (flat, tank, gondola, etc.)."""
    if not car_types:
        return cars_df
    return cars_df[cars_df['car_type'].isin(car_types)].reset_index(drop=True)


def search_cars(cars_df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """
    Search cars by car ID, cargo description, origin, or destination.
    Case-insensitive partial match.
    """
    if not search_term or search_term.strip() == '':
        return cars_df
    
    search_lower = search_term.lower()
    mask = (
        cars_df['car_id'].str.lower().str.contains(search_lower, na=False) |
        cars_df['cargo_description'].str.lower().str.contains(search_lower, na=False) |
        cars_df['origin'].str.lower().str.contains(search_lower, na=False) |
        cars_df['destination'].str.lower().str.contains(search_lower, na=False)
    )
    return cars_df[mask].reset_index(drop=True)


def apply_filters(
    cars_df: pd.DataFrame,
    search_term: Optional[str] = None,
    hazmat_only: bool = False,
    hazmat_classes: Optional[List[int]] = None,
    car_types: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Apply all filters at once."""
    result = cars_df.copy()
    
    if search_term:
        result = search_cars(result, search_term)
    
    if hazmat_only:
        result = filter_by_hazmat(result, hazmat_only=True)
    
    if hazmat_classes:
        result = filter_by_hazmat_class(result, hazmat_classes)
    
    if car_types:
        result = filter_by_car_type(result, car_types)
    
    return result.reset_index(drop=True)
