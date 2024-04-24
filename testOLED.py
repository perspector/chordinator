from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1309
import time

# used for text
from PIL import ImageFont, ImageDraw
text_height = 48

#import glob
#fonts_list = ["Merriweather-Black.ttf", "Monoid-Bold-Dollar-1-l.ttf", "NovaMono-Regular.ttf", "RubikScribble-Regular.ttf", "ComicNeue-Bold.ttf", "ComicNeue-BoldItalic.ttf", "Roboto*"]
#fonts_list = glob.glob('/home/superuser/*.ttf')
font = ImageFont.truetype("Merriweather-Black.ttf", text_height) # Merriweather Black is the best so far


# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
#serial = i2c(port=1, address=0x3C)
serial = spi(device=0, port=0)

# substitute ssd1331(...) or sh1106(...) below if using that device
#device = ssd1306(serial)
device = ssd1309(serial, width=128, height=64, rotate=2)

#device.contrast(255) # 0 - 255

# use device.cleanup() for low power mode
# use device.show() to wake device from low power mode
# use device.clear() to clear the display

device.clear()

chords_list = ["Ab", "Abm", "A", "Am", "D#", "D#m"]

def show_message(message):
    with canvas(device) as draw:
        device.show()
        #draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text(
            #(round((device.width - text_height*len(message)) / 2), (device.height - text_height) / 2),
            #((128-text_height)/2,32),
            (device.width/2, device.height/2),
            message,
            fill="white",
            font=font,
            anchor="mm"
        )
        #device.hide()

#for chord in chords_list:
#for f in fonts_list:
#    print(f)
#    font = ImageFont.truetype(f, text_height)
#    show_message("Abm #")
#    time.sleep(5)

show_message("Abm")
time.sleep(10)
