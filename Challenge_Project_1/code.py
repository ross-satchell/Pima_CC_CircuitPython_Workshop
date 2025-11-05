"""
This project will initialize the display using displayio and draw a solid black
background, a Microchip "Meatball" logo, and move the logo around the screen from the IMU data
This is the starting point for Project 1 in the CircuitPython workshop
"""
import time
import board
import adafruit_icm20x
import displayio
import adafruit_imageload
import digitalio
import microcontroller
import neopixel
from fourwire import FourWire
from adafruit_st7789 import ST7789
import traceback
import sys

def DisableAutoReload():
    import supervisor
    supervisor.runtime.autoreload = False
    print("Auto-reload is currently disabled.")
    print("After saving your code, send a CTRL+C, then CTRL+D to restart.")
    
# uncomment this if auto-reload is causing issues from your editor     
# DisableAutoReload()

# Change these to True to show debug print statements
Debug_Display = False
Debug_IMU = False
Debug_IMU_Drift = False

# NeoPixels may have been turned on by a previously loaded program
# This will turn them all off
pixel_pin = board.NEOPIXEL
num_pixels = 5  # 5 NeoPixels total: 1 on dev board, 4 on ruler baseboard
# Create pixels object
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)
# Turn off all NeoPixels
pixels.fill(0x000000)
pixels.show()

# Create i2c object that will be used by the IMU
i2c = board.I2C()  # uses board.SCL and board.SDA pins

# The ICM20948 address is set to 0x69. However if it cannot be found try alternate address 0x68 
try:
    icm = adafruit_icm20x.ICM20948(i2c, 0x69)
except ValueError as e:
    #print(traceback.format_exception(e))
    print("No ICM20948 found at address 0x69. Trying alternate address 0x68.")
    try:
        icm = adafruit_icm20x.ICM20948(i2c, 0x68)
    except ValueError as f:
        #print(traceback.format_exception(f))
        print("No ICM20948 found at either address. Is your dev board connected to Ruler?")
        sys.exit()

if Debug_Display:
    print("Create output pin called 'backlight' for LCD backlight on PA06")
backlight = digitalio.DigitalInOut(microcontroller.pin.PA06)
backlight.direction = digitalio.Direction.OUTPUT
if Debug_Display:
    print("Turn TFT Backlight On")
backlight.value = False # Backlight is Active LOW

# Release any resources currently in use for the displays
if Debug_Display:
    print("Release displays")
displayio.release_displays()

if Debug_Display:
    print("Create SPI Object for display")
spi = board.LCD_SPI()
tft_cs = board.LCD_CS
tft_dc = board.D4

WIDTH = 240
HEIGHT = 135
LOGO_WIDTH = 32
LOGO_HEIGHT = 30

if Debug_Display:
    print("Create DisplayBus")
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=90, width=WIDTH, height=HEIGHT, rowstart=40, colstart=53
)

# Load the sprite sheet (bitmap)
if Debug_Display:
    print("Load Sprite sheet")
sprite_sheet, palette = adafruit_imageload.load("/Meatball_32x30_16color.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

# Create a sprite (tilegrid)
if Debug_Display:
    print("Create Sprite")
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width=1,
                            height=1,
                            tile_width=LOGO_WIDTH,
                            tile_height=LOGO_HEIGHT)

# Create a Group to hold the sprite
if Debug_Display:
    print("Create Group to hold Sprite")
group = displayio.Group(scale=1)

# Add the sprite to the Group
if Debug_Display:
    print("Append Sprite to Group")
group.append(sprite)

# Add the Group to the Display
if Debug_Display:
    print("Add Group to Display")
display.root_group = group

# Set sprite location
if Debug_Display:
    print("Set Sprite Initial Location")
group.x = 150
group.y = 70

X_pos = 150
Y_pos = 70

while True:

    X, Y, Z = icm.acceleration

    if Debug_IMU:
        print("X: {:.2f}".format(X))
        print("Y: {:.2f}".format(Y))
        print("Z: {:.2f}".format(Z))
        print("")

    X_pos += int(X)
    Y_pos -= int(Y)

    group.x = X_pos
    group.y = Y_pos

    time.sleep(0.02)
