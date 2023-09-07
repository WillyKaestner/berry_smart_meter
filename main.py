import time
import logging.config
import uuid

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_energy_monitor import BrickletEnergyMonitor

import database as db
import crud
import config
from logging_config import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def get_energy_brick_data(meter_uuid: uuid.UUID):
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
    energy_data = db.MeasurementCreate(voltage=voltage,
                                       current=current,
                                       energy=energy,
                                       real_power=real_power,
                                       apparent_power=apparent_power,
                                       reactive_power=reactive_power,
                                       power_factor=power_factor,
                                       frequency=frequency,
                                       meter_uuid=meter_uuid)

    logger.info("Measurements received from energy brick")
    return energy_data


def fake_data():
    energy_data = db.MeasurementCreate(voltage=235,
                                       current=1,
                                       energy=1,
                                       real_power=1,
                                       apparent_power=1,
                                       reactive_power=1,
                                       power_factor=1,
                                       frequency=51)
    return energy_data


def main(config_data: config.ConfigMeter):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    logger.info(f"Program started at {current_time}")
    start = time.perf_counter()

    energy_data = get_energy_brick_data(meter_uuid=config_data.meter_uuid)
    if config_data.run_type == "dry run":
        energy_data = fake_data()
    repository = crud.SqlAlchemyEnergyData(db=db.get_db())
    repository.add(energy_data)

    end = time.perf_counter()
    logger.info(f"Saved measurements in the database: {energy_data.dict()}")
    logger.info(f"Program ended. Execution time: {end - start:.02f}s")


if __name__ == "__main__":
    main(config.get_config_meter())
    logger.info("Git Pull update - 14:56 commit - success")
