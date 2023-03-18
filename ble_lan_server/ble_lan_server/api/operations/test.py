import asyncio
from bleak import BleakScanner


async def main():
    print("scanning for 5 seconds, please wait...")

    devices = await BleakScanner.discover(return_adv=True)

    for d, a in devices.values():
        print()
        print(d)
        print("-" * len(str(d)))
        print(a)

asyncio.run(main())
