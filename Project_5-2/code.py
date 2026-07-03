import pykit_explorer
from imu_sensor import IMUSensor
from neopixels import NeoPixels, Colors, OFF

imu = IMUSensor()
px  = NeoPixels()

while True:
    imu.print_all()
    if imu.is_shaking():
        px.fill(Colors.	WHITE)
        time.sleep(0.2)
    else:
        px.off()
    time.sleep(0.1)