import pykit_explorer
from digital_io import DigitalOutput

led = DigitalOutput(board.LED)

while True:
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)