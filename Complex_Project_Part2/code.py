import pykit_explorer
from imu_sensor import IMUSensor  
from neopixels import NeoPixels, Colors
from ble_uart import BLEUart 
from lcd_display import LCDDisplay, Colors 

#Instantiating each of the classes into Global objects
imu = IMUSensor()
px = NeoPixels()
ble = BLEUart()
lcd = LCDDisplay()            

# Create a "container" (called a group) for the display 
# elements on the LCD, and set the background color to black.
group, palette = lcd.make_group(Colors.BLACK)   

#Header label for the project title
imuLabel0 = lcd.add_label(group, "IMU to RGB project ", 120, 0, scale=2, color=Colors.GREEN)

# IMU acceleration labels (name + value pairs) for ax, ay, az.
IMU_NAMES       = ["ax: ", "ay: ", "az: "]
IMU_Y_POSITIONS = [25, 45, 65]

imu_name_labels  = []
imu_value_labels = []

# Add then append each label to the group and the corresponding list for later access
for i in range(3):
    name_lbl = lcd.add_label(group, IMU_NAMES[i], 40, IMU_Y_POSITIONS[i], scale=2)
    value_lbl = lcd.add_label(group, "", 100, IMU_Y_POSITIONS[i], scale=2)
    imu_name_labels.append(name_lbl)
    imu_value_labels.append(value_lbl)

# RGB value labels (name + value pairs) for R, G, B.
RGB_NAMES             = ["R:", "G:", "B:"]
RGB_COLORS            = [Colors.RED, Colors.GREEN, Colors.BLUE]
RGB_NAME_X_POSITIONS  = [15, 85, 155]
RGB_VALUE_X_POSITIONS = [45, 115, 185]

rgb_name_labels  = []
rgb_value_labels = []

for i in range(3):
    name_lbl = lcd.add_label(group, RGB_NAMES[i], RGB_NAME_X_POSITIONS[i], 100,
                             scale=2, color=RGB_COLORS[i])
    value_lbl = lcd.add_label(group, "0", RGB_VALUE_X_POSITIONS[i], 100,
                              scale=2, color=RGB_COLORS[i])
    rgb_name_labels.append(name_lbl)
    rgb_value_labels.append(value_lbl)

#Constants
GRAVITY = 10
RGB_MAX = 255
RGB_MIN = 0

# Converts 3-axis accelerometer readings into RGB color values for NeoPixel display.
def acceleration_to_rgb(ax, ay, az):
    #maps the acceleration value to a range of 0-255 for red
    r = int(((ax+GRAVITY)/(GRAVITY*2))*RGB_MAX) 
    #maps the acceleration value to a range of 0-255 for green
    g = int(((ay+GRAVITY)/(GRAVITY*2))*RGB_MAX) 
    #maps the acceleration value to a range of 0-255 for blue
    b = int(((az+GRAVITY)/(GRAVITY*2))*RGB_MAX) 
    if(r > RGB_MAX):     r = RGB_MAX
    elif(g  >RGB_MAX):   g = RGB_MAX
    elif(b > RGB_MAX):   b = RGB_MAX
    elif(r < RGB_MIN):   r = RGB_MIN
    elif(g < RGB_MIN):   g = RGB_MIN
    elif(b < RGB_MIN):   b = RGB_MIN

    return (r, g, b)    # Return the RGB values as a tuple to be used for NeoPixel color and LCD display


while True:
    ax, ay, az = imu.acceleration   #sets the acceleration values from the IMU sensor to the variables ax, ay, az for x, y, z axis
    print(f"X: {ax}, Y: {ay}, Z: {az}")
    #setting RGB values to a tuple to modify the color of the neopixels and to display on the LCD
    r,g,b = acceleration_to_rgb(ax, ay, az)
    rgbcoordinate = (r,g,b)         
    print(f"RGB: {rgbcoordinate}")
    px.fill(rgbcoordinate)  # Pass tuple to NeoPixels

    #displaying data on the lcd
    imu_value_labels[0].text = str(round(ax, 2))   # ax value displayed on the LCD, rounded to 2 decimal places
    imu_value_labels[1].text = str(round(ay, 2))   # ay value displayed on the LCD, rounded to 2 decimal places
    imu_value_labels[2].text = str(round(az, 2))   # az value displayed on the LCD, rounded to 2 decimal places
    rgb_value_labels[0].text = str(r) # r value displayed on the LCD
    rgb_value_labels[1].text = str(g) # g value displayed on the LCD
    rgb_value_labels[2].text = str(b) # b value displayed on the LCD

    #sending data to the app via bluetooth
    msg = ble.poll()
    if ble.connected:
        ble.send("ax: " + str(round(ax, 2))+"\n" + 
                 "ay: " + str(round(ay, 2))+"\n" + 
                 "az: " + str(round(az, 2))+"\n" + 
                 "RGB: " + str(rgbcoordinate)+ "\n\n")