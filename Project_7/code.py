import pykit_explorer
import random
from lcd_display import LCDDisplay, Colors

lcd = LCDDisplay()
lcd.backlight_on()

group, _ = lcd.make_group(Colors.BLACK)

LABEL_COLORS = [Colors.RED, Colors.GREEN, Colors.BLUE, Colors.WHITE]
LABEL_NAMES  = ["Label 1", "Label 2", "Label 3", "Label 4"]
Y_POSITIONS  = [20, 50, 80, 110]

name_labels  = []
value_labels = []

for i in range(4):
    name_lbl = lcd.add_label(group, LABEL_NAMES[i], 60, Y_POSITIONS[i],
                             color=LABEL_COLORS[i], scale=2)
    value_lbl = lcd.add_label(group, "0.00", 180, Y_POSITIONS[i],
                              color=LABEL_COLORS[i], scale=2)
    name_labels.append(name_lbl)
    value_labels.append(value_lbl)

while True:
    for i in range(4):
        value_labels[i].text = f"{random.uniform(0, 100):.2f}"
    time.sleep(0.5)