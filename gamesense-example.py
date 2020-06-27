import requests # pip install requests
from time import sleep
import json
import os


# Constants

GAME = 'TEST'
REGISTRATION = f'{{ "game": "{GAME}", "game_display_name": "testing", "developer": "me" }}'
HEADERS = {'Content-Type': 'application/json'}
DEVICETYPE = 'rgb-103-zone'
VALUE = 'VALUE'

EVENTHANDLER = f'{{ "game": "{GAME}", "event": "ILLUMINATE", "min_value": 0, "max_value": 100,  "icon_id": 0, "handlers": [ {{ "device-type": "{DEVICETYPE}", "zone": "one", "color": {{ "gradient": {{ "zero": {{ "red": 0, "green": 255, "blue": 0 }}, "hundred": {{  "red": 255, "green": 0, "blue": 0 }} }} }},"mode": "percent" }} ] }}'

EVENT = f'{{ "game": "{GAME}", "event": "ILLUMINATE",  "data": {{ "value": {VALUE}  }} }}'


# Functions

def load_core_props(path) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except OSError as e:
        print(f"{e}")
        return None
    except json.JSONDecodeError as je:
        print(f"{je}")
        return None


# Program

# Get the %PROGRAMDATA% path from the Windows environment
program_data_path = os.getenv('PROGRAMDATA')

# Load the coreProps.json file to get the address of the GameSense service
cp = load_core_props(f"{program_data_path}/SteelSeries/SteelSeries Engine 3/coreProps.json")

print(f"Contents of coreProps.json -> {json.JSONEncoder().encode(cp)}")


print('\nRegister')

# Register this script with the GameSense engine
r = requests.post(url=f"http://{cp['address']}/game_metadata",data=REGISTRATION,headers=HEADERS)

print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')

print('\nBind game event')

# Bind the game event handler
r = requests.post(url=f"http://{cp['address']}/bind_game_event",data=EVENTHANDLER,headers=HEADERS)

print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')

print('\nSending game events...')

while True:
    # Ramp up
    for i in range(0,101):
        # Send a game event
        r = requests.post(url=f"http://{cp['address']}/game_event",data=EVENT.replace(VALUE,f'{i}'),headers=HEADERS)
        if r.status_code != 200:
            print(f'Status: {r.status_code}')
            print(f'Response: {r.json()}')
        sleep(0.01)
    # Ramp down.
    for i in range(99,-1,-1):
        # Send a game event
        r = requests.post(url=f"http://{cp['address']}/game_event",data=EVENT.replace(VALUE,f'{i}'),headers=HEADERS)
        if r.status_code != 200:
            print(f'Status: {r.status_code}')
            print(f'Response: {r.json()}')
        sleep(0.01)
