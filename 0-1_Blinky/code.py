import time
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True    # Turn the LED On
    time.sleep(0.2)
    led.value = False
    time.sleep(0.2)

# Questions for class:
#                       How to make LED blink faster?
#                       How to make LED blink slower?