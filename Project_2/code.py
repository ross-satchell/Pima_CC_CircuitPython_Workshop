import pykit_explorer
from digital_io import DigitalInput

btn = DigitalInput(board.D3)

while True:
    print(f'Value:	    {btn.value}')
    print(f'is pressed: {btn.is_pressed()}\n')