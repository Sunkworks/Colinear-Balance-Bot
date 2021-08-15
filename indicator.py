import neopixel
import board

pixel_pin = board.D18
pixel_count = 3
pixel_order = neopixel.GRB

pixels = neopixel.NeoPixel(
        pixel_pin, pixel_count, brightness=0.5, auto_write=False, pixel_order=pixel_order
)

def indicate(num, color):
    pixels[num] = color
    pixels.show()

