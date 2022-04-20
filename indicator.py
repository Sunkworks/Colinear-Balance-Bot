import neopixel
import board
# File is not in use anymore
pixel_pin = board.D18 #File used for indicating LED-lights on robot.
pixel_count = 3 
pixel_order = neopixel.GRB

pixels = neopixel.NeoPixel(
        pixel_pin, pixel_count, brightness=0.5, auto_write=False, pixel_order=pixel_order
)

def indicate(num, color):
    pixels[num] = color
    pixels.show()

