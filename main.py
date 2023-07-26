# python -m pip install tinkerforge
import logging.config
from pydantic import BaseModel
from sqlalchemy import Column, Integer
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_energy_monitor import BrickletEnergyMonitor

from config import SETTINGS
from logging_config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# SCHEMA & DB MODELS
Base = declarative_base()


class EnergyDataCreate(BaseModel):  # Data Schema
    voltage: int
    current: int
    energy: int
    real_power: int
    apparent_power: int
    reactive_power: int
    power_factor: int
    frequency: int


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


class SqlAlchemyLocation:
    """
    SQLAlchemy ORM implementation for handling a database as storage
    """
    def __init__(self, db: Session):
        self.db = db

    def add(self, location_data: EnergyDataCreate):
        db_surfspot = EnergyData(**location_data.dict())
        self.db.add(db_surfspot)
        self.db.commit()
        self.db.refresh(db_surfspot)
        # return db_surfspot

    # def get_by_id(self, location_id: int) -> schemas.LocationResponse | None:
    #     location_query = self._get_location_by_id_query(location_id)
    #     return location_query.first()
    #
    # def get_by_name(self, location_name: str) -> schemas.LocationResponse | None:
    #     return self.db.query(EnergyData).filter(EnergyData.name == location_name).first()
    #
    # def list(self) -> list[schemas.LocationResponse]:
    #     return self.db.query(EnergyData).all()
    #
    # def update(self, location_id: int, updated_location: schemas.LocationBase) -> schemas.LocationResponse:
    #     spot_query = self._get_location_by_id_query(location_id)
    #     spot_query.update(updated_location.dict(), synchronize_session=False)
    #     self.db.commit()
    #     return spot_query.first()
    #
    # def delete(self, location_id: int) -> bool:
    #     location_query = self._get_location_by_id_query(location_id)
    #     location_data = location_query.first()
    #
    #     if location_data is None:
    #         return False
    #     else:
    #         location_query.delete(synchronize_session=False)
    #         self.db.commit()
    #         return True
    #
    # def _get_location_by_id_query(self, location_id: int) -> any:
    #     return self.db.query(EnergyData).filter(EnergyData.id == location_id)


def create_db_engine(alembic_use: bool = False):
    sqlalchemy_database_url = f"postgresql://{SETTINGS.database_username}:{SETTINGS.database_password}@" \
                              f"{SETTINGS.database_host}:5432/{SETTINGS.database_name}"
    if alembic_use is True:
        return sqlalchemy_database_url

    engine = create_engine(sqlalchemy_database_url)
    return engine


def get_db() -> Session:
    """
    Creates a database session and returns it, while still closing the database session if an error occurs.

    We put the creation of the sessionlocal() and handling of the requests in a try block. And then we close it in the
    "finally" block. This way we make sure the database session is always closed after the request. Even if there was
    an exception while processing the request.

    Returns:
        SQLAlchemy Database session
    """
    engine = create_db_engine()
    sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = sessionlocal()
    try:
        return db
    finally:
        db.close()


def get_energy_brick_data():
    HOST = "localhost"
    PORT = 4223
    UID = "Us4"  # Change XYZ to the UID of your Energy Monitor Bricklet

    ipcon = IPConnection()  # Create IP connection
    em = BrickletEnergyMonitor(UID, ipcon)  # Create device object

    ipcon.connect(HOST, PORT)  # Connect to brickd
    # Don't use device before ipcon is connected

    # Get current energy data
    voltage, current, energy, real_power, apparent_power, reactive_power, power_factor, \
        frequency = em.get_energy_data()
    # energy_data = EnergyDataCreate(*em.get_energy_data())
    energy_data = EnergyDataCreate(voltage=voltage,
                                   current=current,
                                   energy=energy,
                                   real_power=real_power,
                                   apparent_power=apparent_power,
                                   reactive_power=reactive_power,
                                   power_factor=power_factor,
                                   frequency=frequency)

    return energy_data


def fake_data():
    energy_data = EnergyDataCreate(voltage=235,
                                   current=1,
                                   energy=1,
                                   real_power=1,
                                   apparent_power=1,
                                   reactive_power=1,
                                   power_factor=1,
                                   frequency=51)
    return energy_data


def main():
    # energy_data = get_energy_brick_data()
    energy_data = fake_data()
    repository = SqlAlchemyLocation(db=get_db())
    repository.add(energy_data)
    logger.info(f"Saved measurements in the database: {energy_data.dict()}")


if __name__ == "__main__":
    main()
