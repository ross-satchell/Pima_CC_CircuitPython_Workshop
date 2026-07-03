import pykit_explorer
from neopixels import NeoPixels, Colors

px = NeoPixels()  # 5 LEDs, brightness 0.1

px.fill(Colors.RED)
print("All Neopixels should be red")
time.sleep(1)
px.set(2, Colors.GREEN)
print("Pixel 2 should be green")
time.sleep(1)
px.color_chase(Colors.BLUE)
print("Neopixels should chase blue")
px.rainbow_cycle(cycles=2)
print("Neopixels should cycle through rainbow colors")
px.off()