import asyncio
import json
from bleak import BleakScanner

def load_known_devices():
    devices = {"devices": []}
    try:
        with open('known_ble.json', 'r') as fr:
            content = fr.read()
            devices = json.loads(content)
    except FileNotFoundError:
        pass
    return devices

def save_known_devices(devices):
    with open('known_ble.json', 'w') as fw:
        fw.write(json.dumps(devices, indent=4))

def scan_devices():
    current_devices = []
    async def run():
        devices = await BleakScanner.discover()
        for d in devices:
            current_devices.append({"address": d.address, "name": d.name})
            print(d)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    return current_devices

def merge_devices(current_devices, known_devices):
    for d in current_devices:
        if not d in known_devices["devices"]:
            known_devices["devices"].append(d)
            print(f"New device found: {d}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Welcome to BLE agent, scanning close BLE devices')
    known_devices = load_known_devices()
    current_devices = scan_devices()
    merge_devices(current_devices, known_devices)
    save_known_devices(known_devices)
    print('END')

