from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1309
import time

# used for text
from PIL import ImageFont, ImageDraw

text_height = 48
font = ImageFont.truetype("Merriweather-Black.ttf", text_height) # Merriweather Black is the best so far


serial = spi(device=0, port=0)

# substitute ssd1331(...) or sh1106(...) below if using that device
#device = ssd1306(serial)
device = ssd1309(serial, width=128, height=64, rotate=0)

device.contrast(1) # 0 - 255

# use device.cleanup() for low power mode
# use device.show() to wake device from low power mode
# use device.clear() to clear the display

device.clear()

chords_list = ["Ab", "Abm", "A", "Am", "D#", "D#m"]

class Display():
    def write(message):
        with canvas(device) as draw:
            draw.text(
                (device.width/2, device.height/2),
                message,
                fill="white",
                font=font,
                anchor="mm"
            )
