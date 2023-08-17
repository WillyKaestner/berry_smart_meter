"""Data Schemas defined with pydantic"""

import pydantic as pyd


class EnergyDataCreate(pyd.BaseModel):  # Data Schema
    voltage: int
    current: int
    energy: int
    real_power: int
    apparent_power: int
    reactive_power: int
    power_factor: int
    frequency: int
    meter_uuid: pyd.UUID4
