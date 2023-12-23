import requests
import logging

logger = logging.getLogger(__name__)

IP_ADDRESS_PLUG_1 = "192.168.1.91"


def control_plugs(energy_data):
    if energy_data.real_power > 200000:
        turn_shelly_off(IP_ADDRESS_PLUG_1)
    else:
        turn_shelly_on(IP_ADDRESS_PLUG_1)


def turn_shelly_on(ip_address):
    url = f'http://{ip_address}/relay/0?turn=on'
    try:
        response = requests.get(url)
        logger.info(f"Shelly plug turned on. Response: {response}")
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# Turn the Shelly device off.
def turn_shelly_off(ip_address):
    url = f'http://{ip_address}/relay/0?turn=off'
    try:
        response = requests.get(url)
        logger.info(f"Shelly plug turned off. Response: {response}")
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

