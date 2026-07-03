import pykit_explorer
from imu_sensor import IMUSensor  
from neopixels import NeoPixels, Colors

#Instantiating each of the classes into Global objects
imu = IMUSensor()
px = NeoPixels()

#Constants
GRAVITY = 10
RGB_MAX = 255
RGB_MIN = 0

def acceleration_to_rgb(ax, ay, az):
    """
    Converts 3-axis accelerometer readings into RGB color values for NeoPixel display.

    This function maps acceleration values from the IMU sensor (x, y, z axes) to RGB
    color channels (red, green, blue) with values normalized to the 0-255 range. Each
    acceleration axis is independently mapped: the x-axis controls red intensity, the
    y-axis controls green intensity, and the z-axis controls blue intensity.

    The mapping uses a linear transformation centered on Earth's gravity (GRAVITY = 10):
    - Acceleration range: [-GRAVITY, +GRAVITY] maps to RGB range [0, 255]
    - Formula: ((acceleration + GRAVITY) / (GRAVITY * 2)) * RGB_MAX
    - This centers the mapping so that 0g acceleration produces 127 (mid-range RGB)

    Clamping ensures that mapped values stay within valid bounds:
    - If a calculated RGB value exceeds 255, it's clamped to 255 (maximum brightness)
    - If a calculated RGB value drops below 0, it's clamped to 0 (no brightness)
    This prevents integer overflow and ensures the NeoPixels receive valid color input.

    Args:
        ax (float): Acceleration on the x-axis in m/s² or g-force (from IMU sensor)
        ay (float): Acceleration on the y-axis in m/s² or g-force (from IMU sensor)
        az (float): Acceleration on the z-axis in m/s² or g-force (from IMU sensor)

    Returns:
        tuple: A 3-tuple (r, g, b) where each value is an integer in range [0, 255]
               representing the red, green, and blue color channels respectively.
               This tuple can be passed directly to NeoPixels.fill() for display.

    Example:
        If ax=10, ay=0, az=-10 (max x-accel, no y-accel, min z-accel):
        - r = int(((10+10)/(10*2))*255) = 255 (red at full brightness)
        - g = int(((0+10)/(10*2))*255) = 127 (green at half brightness)
        - b = int(((-10+10)/(10*2))*255) = 0 (blue at no brightness)
        - Returns: (255, 127, 0) - displays as orange
    """
    #maps the acceleration value to a range of 0-255 for red
    r = int(((ax+GRAVITY)/(GRAVITY*2))*RGB_MAX) 
    #maps the acceleration value to a range of 0-255 for green
    g = int(((ay+GRAVITY)/(GRAVITY*2))*RGB_MAX) 
    #maps the acceleration value to a range of 0-255 for blue
    b = int(((az+GRAVITY)/(GRAVITY*2))*RGB_MAX) 

    if (r > RGB_MAX):       r = RGB_MAX
    elif (r < RGB_MIN):     r = RGB_MIN

    if (g > RGB_MAX):       g = RGB_MAX
    elif (g < RGB_MIN):     g = RGB_MIN

    if (b > RGB_MAX):       b = RGB_MAX
    elif (b < RGB_MIN):     b = RGB_MIN

    return (r, g, b)    # Return the RGB values as a tuple to be used for NeoPixel color and LCD display


while True:
    ax, ay, az = imu.acceleration   #sets the acceleration values from the IMU sensor to the variables ax, ay, az for x, y, z axis
    print(f"X: {ax}, Y: {ay}, Z: {az}")
    #setting RGB values to a tuple to modify the color of the neopixels and to display on the LCD
    r,g,b = acceleration_to_rgb(ax, ay, az)
    rgbcoordinate = (r,g,b)         
    print(f"RGB: {rgbcoordinate}\n")
    px.fill(rgbcoordinate)  # Pass tuple to NeoPixels
    time.sleep(0.1)