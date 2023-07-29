"""Data Schemas defined with pydantic"""

from pydantic import BaseModel

class EnergyDataCreate(BaseModel):  # Data Schema
    voltage: int
    current: int
    energy: int
    real_power: int
    apparent_power: int
    reactive_power: int
    power_factor: int
    frequency: int
