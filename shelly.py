import requests
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

IP_ADDRESS_PLUG_1 = "192.168.1.91"
IP_ADDRESS_PLUG_2 = "192.168.1.147"
IP_ADDRESS_PLUG_3 = "192.168.1.84"
IP_ADDRESS_PLUG_4 = "192.168.1.105"


def control_plugs(energy_data):
    if energy_data.real_power > 500000:
        turn_shelly_off(IP_ADDRESS_PLUG_1)
        turn_shelly_off(IP_ADDRESS_PLUG_2)
        turn_water_boiler_off()
        turn_shelly_off(IP_ADDRESS_PLUG_4)
    elif energy_data.real_power < 200000:
        turn_shelly_on(IP_ADDRESS_PLUG_1)
        turn_shelly_on(IP_ADDRESS_PLUG_2)
        turn_water_boiler_on()
        turn_shelly_on(IP_ADDRESS_PLUG_4)
    else:
        logger.info(f"Current Energy consumption of {energy_data.real_power / 100:.2f} Watt. Not controlling Plugs")


def turn_shelly_on(ip_address):
    url = f'http://{ip_address}/relay/0?turn=on'
    try:
        response = requests.get(url)
        logger.info(f"Shelly plug with IP {ip_address} turned on. Response: {response}")
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# Turn the Shelly device off.
def turn_shelly_off(ip_address):
    url = f'http://{ip_address}/relay/0?turn=off'
    try:
        response = requests.get(url)
        logger.info(f"Shelly plug with IP {ip_address} turned off. Response: {response}")
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def turn_water_boiler_off():
    turn_shelly_off(IP_ADDRESS_PLUG_3)
    # Get current time
    current_time = datetime.now()
    # Convert to a string (for example, in ISO format)
    current_time_str = current_time.isoformat()
    # Prepare the data to be saved as JSON
    data_to_save = {'switch_off_time': current_time_str}
    # Write to switch_off.json file
    with open('switch_off.json', 'w') as file:
        json.dump(data_to_save, file)
    logger.info(f"Water boiler turned off at {current_time_str}")


def turn_water_boiler_on():
    # load switch_off.json file
    with open('switch_off.json', 'r') as file:
        data = json.load(file)
    # Get switch_off_time
    switch_off_time = data['switch_off_time']
    # Convert to datetime object
    switch_off_time = datetime.fromisoformat(switch_off_time)
    # Get current time
    current_time = datetime.now()
    # Calculate time difference
    time_difference = current_time - switch_off_time
    # Convert time difference to minutes
    time_difference_minutes = time_difference.total_seconds() / 60
    # If time difference is more than 30 minutes, turn on water boiler
    if time_difference_minutes > 20:
        turn_shelly_on(IP_ADDRESS_PLUG_3)
        logger.info(f"Water boiler turned on at {current_time.isoformat()}")
    else:
        logger.info(f"Water boiler not turned on. Time difference of {time_difference_minutes:.2f} minutes since switch off")

