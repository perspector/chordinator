"""
DiscoPie programmed, designed, and 3D printed by Benjamin Chase for Baked Dessert Cafe and Gallery
Copyright (c) 2022 pythoncoder8888
All code is licensed under the MIT License
See LICENSE.txt for more details
"""

import os
import time
import RPi.GPIO as GPIO

import board
import neopixel
import random

pixel_pin = board.D12
num_pixels = 40
ORDER = neopixel.GRB
pixel_brightness = 0.1

color_list = [(255, 0, 0), (252, 104, 5), (255, 255, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=pixel_brightness, auto_write=False, pixel_order=ORDER
)

for i in range(num_pixels):
    pixels[i] = (0,255,0)
    pixels.show()
    time.sleep(0.1)

time.sleep(2)

pixels.fill((0, 0, 0))

GPIO.setmode(GPIO.BCM)

global current_color
current_color = 0


def rainbow(colors, length):
    global current_color
    for j in range(num_pixels):
        pixels[j] = colors[current_color]
        pixels.show()
        time.sleep(length)
    current_color = current_color + 1
    if current_color > 5:
        current_color = 0

try:
    while True:
        rainbow(color_list, 0.05)

except KeyboardInterrupt:
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(1.5)
    for i in range(num_pixels):
        pixels[-i] = (0, 0, 0)
        pixels.show()
        time.sleep(0.1)
    pixels.fill((0, 0, 0))
    pixels.show()
    print("\nQuit by user")
    GPIO.cleanup()
    exit()

except Exception as e:
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(5)
    print(e)
    pass

GPIO.cleanup()