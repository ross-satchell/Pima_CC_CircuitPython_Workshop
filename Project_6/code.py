import pykit_explorer
from ble_uart import BLEUart
from cpu_temp import CPUTemperature

ble  = BLEUart()
temp = CPUTemperature()

while True:
    ble.poll()  # process connection status messages
    if ble.connected:
        ble.send(f"Temp: {temp.formatted_string()}\n")
        print(f"Temp: {temp.formatted_string()}")
    time.sleep(1)