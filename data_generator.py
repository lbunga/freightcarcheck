"""Generate realistic sample train manifest data."""
import json
import random
from datetime import datetime
from models import Train, Car, Cargo, HazmatInfo


# Sample cargo descriptions and hazmat classifications
HAZMAT_CARGO = [
    {
        'description': 'Flammable Liquids (Class 3)',
        'hazmat_class': 3,
        'un_code': 'UN1072',
        'weight_range': (15, 35),
    },
    {
        'description': 'Flammable Liquids - Gasoline',
        'hazmat_class': 3,
        'un_code': 'UN1203',
        'weight_range': (20, 40),
    },
    {
        'description': 'Flammable Solids (Class 4)',
        'hazmat_class': 4,
        'un_code': 'UN1325',
        'weight_range': (10, 30),
    },
    {
        'description': 'Oxidizing Substances (Class 5)',
        'hazmat_class': 5,
        'un_code': 'UN2014',
        'weight_range': (15, 35),
    },
    {
        'description': 'Toxic Substances (Class 6)',
        'hazmat_class': 6,
        'un_code': 'UN1583',
        'weight_range': (5, 25),
    },
    {
        'description': 'Corrosive Materials (Class 8)',
        'hazmat_class': 8,
        'un_code': 'UN1830',
        'weight_range': (20, 40),
    },
    {
        'description': 'Miscellaneous Hazardous (Class 9)',
        'hazmat_class': 9,
        'un_code': 'UN3077',
        'weight_range': (10, 30),
    },
]

SAFE_CARGO = [
    ('Grain', (25, 50)),
    ('Coal', (50, 80)),
    ('Steel Coils', (35, 70)),
    ('Machinery Equipment', (20, 50)),
    ('Automotive Parts', (15, 40)),
    ('Paper Products', (20, 35)),
    ('Lumber', (15, 30)),
    ('Containers', (10, 25)),
    ('Cement', (40, 70)),
    ('Aggregates', (60, 100)),
]

CAR_TYPES = {
    'flat': {'count': 0.35, 'capacity': 80},  # 35% flatcars
    'tank': {'count': 0.30, 'capacity': 150},  # 30% tank cars
    'gondola': {'count': 0.20, 'capacity': 90},  # 20% gondolas
    'hopper': {'count': 0.10, 'capacity': 100},  # 10% hoppers
    'box': {'count': 0.05, 'capacity': 70},  # 5% boxcars
}

ORIGINS = ['Chicago, IL', 'Houston, TX', 'Denver, CO', 'Los Angeles, CA', 'Atlanta, GA', 'Dallas, TX', 'Kansas City, MO']
DESTINATIONS = ['New York, NY', 'San Francisco, CA', 'Memphis, TN', 'Phoenix, AZ', 'Miami, FL', 'Portland, OR', 'Minneapolis, MN']


def generate_realistic_train(num_cars: int = 150, hazmat_percentage: float = 0.18) -> dict:
    """
    Generate a realistic freight train manifest.
    
    Args:
        num_cars: Number of cars in the train (default 150)
        hazmat_percentage: Percentage of hazmat cars (default 18%)
    
    Returns:
        Dictionary representation of Train object serializable to JSON
    """
    train_id = f"TRAIN-{random.randint(10000, 99999)}"
    cars_data = []
    num_hazmat = int(num_cars * hazmat_percentage)
    
    # Determine car type distribution
    car_type_counts = {}
    remaining = num_cars
    for car_type, config in CAR_TYPES.items():
        count = int(num_cars * config['count'])
        car_type_counts[car_type] = min(count, remaining)
        remaining -= car_type_counts[car_type]
    
    # Distribute remaining cars
    if remaining > 0:
        for car_type in car_type_counts:
            if remaining > 0:
                car_type_counts[car_type] += 1
                remaining -= 1
    
    # Create cars with hazmat distribution
    position = 1
    hazmat_positions = set(random.sample(range(num_cars), num_hazmat))
    
    for car_type, count in car_type_counts.items():
        for _ in range(count):
            is_hazmat = (position - 1) in hazmat_positions
            
            if is_hazmat:
                hazmat = random.choice(HAZMAT_CARGO)
                cargo_weight = random.uniform(hazmat['weight_range'][0], hazmat['weight_range'][1])
                hazmat_info = {
                    'is_hazmat': True,
                    'hazmat_class': hazmat['hazmat_class'],
                    'un_code': hazmat['un_code'],
                    'description': hazmat['description'],
                }
                cargo_desc = hazmat['description']
            else:
                cargo_name, weight_range = random.choice(SAFE_CARGO)
                cargo_weight = random.uniform(weight_range[0], weight_range[1])
                hazmat_info = {
                    'is_hazmat': False,
                    'hazmat_class': None,
                    'un_code': None,
                    'description': '',
                }
                cargo_desc = cargo_name
            
            car = {
                'car_id': f"{car_type.upper()[:3]}-{position:05d}",
                'car_type': car_type,
                'capacity_tons': CAR_TYPES[car_type]['capacity'],
                'position': position,
                'cargo': {
                    'description': cargo_desc,
                    'weight_tons': round(cargo_weight, 2),
                    'hazmat_info': hazmat_info,
                    'origin': random.choice(ORIGINS),
                    'destination': random.choice(DESTINATIONS),
                }
            }
            cars_data.append(car)
            position += 1
    
    # Calculate totals
    total_weight = sum(
        CAR_TYPES[car['car_type']]['capacity'] * 0.3 + car['cargo']['weight_tons']  # Rough estimate
        for car in cars_data
    )
    
    train_manifest = {
        'train_id': train_id,
        'cars': cars_data,
        'manifest_date': datetime.now().isoformat(),
        'total_cars': len(cars_data),
        'total_weight_tons': round(total_weight, 2),
    }
    
    return train_manifest


def generate_sample_trains(count: int = 3) -> list:
    """Generate multiple sample trains for the POC."""
    return [generate_realistic_train() for _ in range(count)]


if __name__ == '__main__':
    # Generate and save sample trains
    trains = generate_sample_trains(3)
    
    with open('data/sample_trains.json', 'w') as f:
        json.dump(trains, f, indent=2)
    
    print(f"Generated {len(trains)} sample trains")
    print(f"Sample train: {trains[0]['train_id']}")
    print(f"  - Total cars: {trains[0]['total_cars']}")
    print(f"  - Total weight: {trains[0]['total_weight_tons']} tons")
    hazmat_count = sum(1 for car in trains[0]['cars'] if car['cargo']['hazmat_info']['is_hazmat'])
    print(f"  - Hazmat cars: {hazmat_count}")
