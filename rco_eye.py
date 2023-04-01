import adafruit_is31fl3741
import is31fl3741_framebuf
from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT
import adafruit_imageload
import math
import asyncio


class Pupil:
    def __init__(self, file, px_bleed):
        self.bmp, self.idx = adafruit_imageload.load(file)
        self.width = self.bmp.width
        self.height = self.bmp.height
        self.px_bleed = px_bleed
        self.position = (0, 0)

    def draw(self, eye: Eye):
        x, y = self.position
        for i in range(0, self.width):
            for j in range(0, self.height):
                if self.bmp[i,j] > 0:
                    eye.pixel(i + x, j + y, self.idx[self.bmp[i,j]])

    def set_position(self, x: float, y: float):
        '''Sets the pupil position with the x,y being the center point of the pupil'''
        self.position = (x - math.floor((self.width - 1) / 2), y - math.floor((self.height - 1) / 2))


class Eyelid:
    def __init__(self, file_top, file_bottom, open_offset: int, squint_offset: int, closed_offset: int, wide_offset: int):
        self.top_bmp, self.top_idx = adafruit_imageload.load(file_top)
        self.top_width = self.top_bmp.width
        self.top_height = self.top_bmp.height

        self.bottom_bmp, self.bottom_idx = adafruit_imageload.load(file_bottom)
        self.bottom_width = self.bottom_bmp.width
        self.bottom_height = self.bottom_bmp.height

        self.current_offset = open_offset
        self.open_offset = open_offset
        self.squint_offset = squint_offset
        self.closed_offset = closed_offset
        self.wide_offset = wide_offset

    def draw(self, eye):
        for i in range(0, self.bottom_width):
            for j in range(0, self.bottom_height):
                if self.bottom_bmp[i,j] > 0:
                    eye.pixel(i, eye.height + j - self.current_offset, self.bottom_idx[self.bottom_bmp[i,j]])

        for i in range(0, self.top_width):
            for j in range(0, self.top_height):
                if self.top_bmp[i,j] > 0:
                    eye.pixel(i, j - self.top_height + self.current_offset, self.top_idx[self.top_bmp[i,j]])
    
    def squint(self):
        self.current_offset = self.squint_offset

    def open(self):
        self.current_offset = self.open_offset

    def close(self):
        self.current_offset = self.closed_offset

    def wide(self):
        self.current_offset = self.wide_offset


class Eye:
    def __init__(self, i2c, address, led_width, led_height, led_brightness, outer_color, pupil: Pupil, eyelid: Eyelid):
        matrix = Adafruit_RGBMatrixQT(i2c=i2c, address=address, allocate=adafruit_is31fl3741.PREFER_BUFFER)
        matrix.set_led_scaling(led_brightness)
        matrix.global_current = 0xff
        matrix.enable = True

        self.buf = is31fl3741_framebuf.IS31Framebuffer(matrix, led_width, led_height)

        self.height = led_height
        self.width = led_width
        self.outer_color = outer_color
        self.pupil = pupil
        self.eyelid = eyelid
        self.pupil_range_x = self.width + 1 - self.pupil.width + 2 * self.pupil.px_bleed
        self.pupil_range_y = self.height + 1 - self.pupil.height + 2 * self.pupil.px_bleed
        self.pupil_range_x_offset = int((self.width - self.pupil_range_x) / 2)
        self.pupil_range_y_offset = int((self.height - self.pupil_range_y) / 2)

        self.center_pupil()
        self.draw()

    def pixel(self, x, y, color):
        self.buf.pixel(x, y, color)

    def pupil_position(self, x, y):
        x = round((self.pupil_range_x - 1) * x) + self.pupil_range_x_offset
        y = round((self.pupil_range_y - 1) * y) + self.pupil_range_y_offset

        self.pupil.set_position(x, y)

    def center_pupil(self):
        self.pupil_position(.5, .5)

    def draw(self):
        self.buf.fill(self.outer_color)
        self.pupil.draw(self)
        self.eyelid.draw(self)
        self.buf.display()


class Animator:
    def __init__(self, left: Eye, right: Eye):
        self.left = left
        self.right = right
        self.state = "open"
    
    async def wink(self):
        if not self.state == "open":
            return
        
        eye = self.right
        eyelid = eye.eyelid

        eyelid.squint()
        eye.draw()

        eyelid.close()
        eye.draw()

        await asyncio.sleep(.5)

        eyelid.squint()
        eye.draw()

        eyelid.open()
        eye.draw()

    async def blink(self):
        if self.state == "open":
            self.squint()
        
        self.close()
        self.open()


    def close(self):
        if self.state == "open":
            self.squint()

        self.left.eyelid.close()
        self.right.eyelid.close()
        self.left.draw()
        self.right.draw()
        self.state = "closed"

    def squint(self):
        self.left.eyelid.squint()
        self.right.eyelid.squint()
        self.left.draw()
        self.right.draw()
        self.state = "squint"

    def open(self):
        if self.state == "closed":
            self.squint()
        if self.state == "crossed":
            self.left.pupil_position(0.5, 0.5)
            self.right.pupil_position(0.5, 0.5)

        self.left.eyelid.open()
        self.right.eyelid.open()
        self.left.draw()
        self.right.draw()
        self.state = "open"

    def cross(self):
        if not self.state == "open":
            self.open()

        self.left.pupil_position(0.92, 0.5)
        self.right.pupil_position(0.08, 0.5)
        self.left.draw()
        self.right.draw()
        self.state = "crossed"


