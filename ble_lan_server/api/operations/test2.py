import asyncio
from bleak import BleakClient

address = "47:87:4D:26:13:39"
MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"


async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main(address))
