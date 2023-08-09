"""Database Models declared using SQLAlchemy"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text


Base = declarative_base()


class EnergyData(Base):  # Database Model
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    voltage = Column(Integer)
    current = Column(Integer)
    energy = Column(Integer)
    real_power = Column(Integer)
    apparent_power = Column(Integer)
    reactive_power = Column(Integer)
    power_factor = Column(Integer)
    frequency = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    meter_uuid = Column(UUID(), autoincrement=False)
