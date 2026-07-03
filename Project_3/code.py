import pykit_explorer
from digital_io import DigitalOutput, EdgeDetector

led = DigitalOutput(board.LED)
btn = EdgeDetector(board.D3)

while True:
    btn.update()
    if btn.fell:
        led.toggle()
    time.sleep(0.01)