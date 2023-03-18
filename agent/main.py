import asyncio
import json
import time
from bleak import BleakScanner, BleakClient
import json
import requests

def send_to_server(devices):
    print("Sending update")
    e = requests.put('http://127.0.0.1/api/ble', headers={"X-API-KEY": "custom_key"}, verify=False, data=devices)
    pass

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
            current_devices.append({"address": d.address, "name": d.name, "rssi": d.rssi, "bluetooth_address": d.details.adv.bluetooth_address})
            print(d)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    return current_devices

def merge_devices(current_devices, known_devices):
    for d in current_devices:
        if not d in known_devices["devices"]:
            known_devices["devices"].append(d)
            print(f"New device found: {d}")


async def scan_for_device(device_address):
    scanner = BleakScanner(detection_callback=callback)
    # scanner.register_detection_callback(callback)
    await scanner.start()
    await asyncio.sleep(30.0)
    await scanner.stop()

async def callback(device, advertisement_data):
    if device.address == device_address:
        print(f"Dispositivo encontrado: {device}, RSSI:{device.rssi}")
        print(advertisement_data)



def follow_ble(mac):
    # while True:
    #     d = BleakScanner.find_device_by_address(mac)
    #     pass
    #     time.sleep(3)

    MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"

    async def search(mac):
        async with BleakClient(mac) as client:
            data = await client.connect()
            client.disconnect()
            # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
            # print("Model Number: {0}".format("".join(map(chr, model_number))))

    asyncio.run(search(mac))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Welcome to BLE agent, scanning close BLE devices')
    send_to_server("{}")
    known_devices = {"devices": []}
    # known_devices = load_known_devices()
    # current_devices = scan_devices()
    # merge_devices(current_devices, known_devices)
    # save_known_devices(known_devices)
    device_address = "A4:C1:38:1A:2D:1C"
    asyncio.run(scan_for_device(device_address))
    # follow_ble("A4:C1:38:1A:2D:1C")
    print('END')
    # 65:D8:85:03:E9:34
    # F5:92:A2:6A:7A:7D
    # E0:68:1F:48:14:10
#     44:51:40:F6:D0:CF


## APPLE tag llavero?? D8:AF:51:DB:81:E0

#-28 0m
#-46 1m
#-52 2m
#-54 3m
