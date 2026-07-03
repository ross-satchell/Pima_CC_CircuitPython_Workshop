import pykit_explorer
from imu_sensor import IMUSensor
from neopixels  import NeoPixels, Colors, OFF

imu = IMUSensor()
px  = NeoPixels()

while True:
    direction = imu.tilt_direction()
    if direction == "LEFT":
        px.fill(Colors.RED)
    elif direction == "RIGHT":
        px.fill(Colors.BLUE)
    elif direction == "UP":
        px.fill(Colors.GREEN)
    elif direction == "DOWN":
        px.fill(Colors.YELLOW)
    else:
        px.off()