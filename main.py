import time
import logging.config
import uuid

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_energy_monitor import BrickletEnergyMonitor

import database as db
import crud
import config
import shelly
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
    voltage, current, energy, real_power, apparent_power, reactive_power, power_factor, frequency = em.get_energy_data()
    energy_data = db.EnergyDataCreate(voltage=voltage,
                                      current=current,
                                      energy=energy,
                                      real_power=real_power,
                                      apparent_power=apparent_power,
                                      reactive_power=reactive_power,
                                      power_factor=power_factor,
                                      frequency=frequency,
                                      meter_uuid=meter_uuid)

    logger.debug("Measurements received from energy brick")
    return energy_data


def fake_data(meter_uuid):
    energy_data = db.EnergyDataCreate(voltage=235,
                                      current=1,
                                      energy=1,
                                      real_power=1,
                                      apparent_power=1,
                                      reactive_power=1,
                                      power_factor=1,
                                      frequency=51,
                                      meter_uuid=meter_uuid)
    return energy_data


def main(config_data: config.ConfigMeter):

    # setup the global database engine
    db.setup_db()

    current_time = time.strftime("%H:%M:%S", time.localtime())
    logger.debug(f"Program started at {current_time}")
    start = time.perf_counter()

    if config_data.run_type == "dry run":
        energy_data = fake_data("7c1b09f8-d6f6-4a4d-b4ad-07ac6ad991ae")
    else:
        energy_data = get_energy_brick_data(meter_uuid=config_data.meter_uuid)

    # Control shelly plugs based on the power consumption
    shelly.control_plugs(energy_data)

    #  Save data to database
    repository = crud.SqlAlchemyLocation()
    repository.add(energy_data)

    end = time.perf_counter()
    logger.info(f"Saved measurements in the database: {energy_data.dict()}")
    logger.debug(f"Program ended. Execution time: {end - start:.02f}s")


if __name__ == "__main__":
    main(config.get_config_meter())
