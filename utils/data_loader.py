"""Data loading utilities."""
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict


def load_train_json(filepath: str) -> Dict:
    """Load train data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def trains_json_to_dataframe(trains_data: List[Dict]) -> pd.DataFrame:
    """
    Convert JSON train data to a pandas DataFrame for easier processing.
    Handles both single train and list of trains.
    """
    if isinstance(trains_data, dict):
        trains_data = [trains_data]
    
    rows = []
    for train in trains_data:
        for car in train['cars']:
            hazmat_info = car['cargo']['hazmat_info']
            
            car_weights = {
                'flat': 30,
                'tank': 140,
                'gondola': 38,
                'box': 35,
                'hopper': 35,
            }
            car_weight = car_weights.get(car['car_type'], 35)
            total_weight = car_weight + car['cargo']['weight_tons']
            
            row = {
                'train_id': train['train_id'],
                'car_id': car['car_id'],
                'position': car['position'],
                'car_type': car['car_type'],
                'capacity_tons': car['capacity_tons'],
                'cargo_weight_tons': car['cargo']['weight_tons'],
                'total_weight_tons': total_weight,
                'cargo_description': car['cargo']['description'],
                'is_hazmat': hazmat_info['is_hazmat'],
                'hazmat_class': hazmat_info['hazmat_class'],
                'un_code': hazmat_info['un_code'],
                'origin': car['cargo']['origin'],
                'destination': car['cargo']['destination'],
            }
            rows.append(row)
    
    return pd.DataFrame(rows)


def load_sample_trains(data_dir: str = 'data') -> List[Dict]:
    """Load all sample trains from data directory."""
    data_path = Path(data_dir) / 'sample_trains.json'
    
    if not data_path.exists():
        return []
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # Handle both single train and list of trains
    if isinstance(data, dict) and 'train_id' in data:
        return [data]
    elif isinstance(data, list):
        return data
    
    return []
