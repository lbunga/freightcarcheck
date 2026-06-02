"""Data models for FreightcarchecK application."""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class HazmatInfo:
    """Hazmat classification information (DOT standard)."""
    is_hazmat: bool
    hazmat_class: Optional[int] = None  # 1-9 per DOT classification
    un_code: Optional[str] = None  # UN number (e.g., UN1072)
    description: str = ""
    
    def __post_init__(self):
        if self.is_hazmat and self.hazmat_class is None:
            raise ValueError("Hazmat cars must have a hazmat_class")


@dataclass
class Cargo:
    """Cargo information for a rail car."""
    description: str
    weight_tons: float
    hazmat_info: HazmatInfo
    origin: str
    destination: str


@dataclass
class Car:
    """Represents a single freight rail car."""
    car_id: str
    car_type: str  # flat, tank, gondola, box, etc.
    capacity_tons: float
    cargo: Cargo
    position: int  # Position in train (1-150)
    
    @property
    def actual_weight_tons(self) -> float:
        """Return actual weight (car + cargo)."""
        car_weight = {
            'flat': 30,
            'tank': 140,
            'gondola': 38,
            'box': 35,
            'hopper': 35,
        }
        return car_weight.get(self.car_type, 35) + self.cargo.weight_tons


@dataclass
class Train:
    """Represents a freight train with multiple cars."""
    train_id: str
    cars: List[Car]
    manifest_date: datetime
    
    @property
    def total_cars(self) -> int:
        return len(self.cars)
    
    @property
    def total_weight_tons(self) -> float:
        """Total weight including all cars and cargo."""
        return sum(car.actual_weight_tons for car in self.cars)
    
    @property
    def hazmat_cars(self) -> List[Car]:
        """Return list of hazmat cars."""
        return [car for car in self.cars if car.cargo.hazmat_info.is_hazmat]
    
    @property
    def hazmat_weight_tons(self) -> float:
        """Total weight of hazmat cargo only."""
        return sum(car.cargo.weight_tons for car in self.hazmat_cars)
    
    @property
    def braking_ratio(self) -> float:
        """Braking weight ratio: hazmat weight / total weight."""
        if self.total_weight_tons == 0:
            return 0
        return self.hazmat_weight_tons / self.total_weight_tons
