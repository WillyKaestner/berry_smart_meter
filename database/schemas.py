"""Data Schemas defined with pydantic"""
import datetime

import pydantic as pyd


class MeasurementCreate(pyd.BaseModel):  # Data Schema
    voltage: int
    current: int
    energy: int
    real_power: int
    apparent_power: int
    reactive_power: int
    power_factor: int
    frequency: int
    meter_uuid: pyd.UUID4


class MeasurementResponse(pyd.BaseModel):  # Data Schema
    id: int
    voltage: int
    current: int
    energy: int
    real_power: int
    apparent_power: int
    reactive_power: int
    power_factor: int
    frequency: int
    meter_uuid: pyd.UUID4
    created_at: datetime.datetime
