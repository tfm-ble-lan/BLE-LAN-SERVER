import asyncio
from bleak import BleakScanner

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


    async def run():
        devices = await BleakScanner.discover()
        for d in devices:
            print(d)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Guys')

