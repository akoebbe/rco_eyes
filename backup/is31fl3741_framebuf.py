# modified from Adafruit_CircuitPython_Pixel_Framebuf
# this is a work in progress...

from micropython import const
import adafruit_framebuf

# build the table to convert the summed color to a single gamma corrected color
gamma_table = []
def build_gamma():
    for x in range(255*9):
        gamma_table.append(gamma(x))

def gamma(g):
    v = int((g / (255*9)) ** 2.6 * 255 + 0.5)
    return v

HORIZONTAL = const(1)
VERTICAL = const(2)

# pylint: disable=too-many-function-args
class IS31Framebuffer(adafruit_framebuf.FrameBuffer):
    def __init__(
        self,
        matrix,
        width,
        height,
        rotation=0,
        scale=False,
    ):  # pylint: disable=too-many-arguments
        self._width = width
        self._height = height
        self._matrix = matrix
        self._scale = scale
        self._buffer = bytearray(width * height * 3)
        super().__init__(
            self._buffer, width, height, buf_format=adafruit_framebuf.RGB888
        )
        self.rotation = rotation
        build_gamma()

    def blit(self):
        """blit is not yet implemented"""
        raise NotImplementedError()

    def display(self):
        """Copy the raw buffer changes to the grid and show"""
        print(self._height, self._width)
        for _y in range(self._height):
            for _x in range(self._width):
                r = g = b = 0
                # if self._scale is True:
                    # index = (_y * (self.stride*3) + (_x*3)) * 3
                    # for _yy in range(3):
                    #     for _xx in range(0, 9, 3):
                    #         r += self._buffer[index+_xx]
                    #         g += self._buffer[index+1+_xx]
                    #         b += self._buffer[index+2+_xx]
                    #     index += self.stride*3
                    # r = gamma_table[r]
                    # g = gamma_table[g]
                    # b = gamma_table[b]
                # else:
                index = (_y * self.stride + _x) * 3
                r = self._buffer[index]
                g = self._buffer[index+1]
                b = self._buffer[index+2]

                print(_x, _y, index, self._matrix.r_offset)

                self._matrix[self._matrix.pixel_addrs(_x, _y)[self._matrix.r_offset]] = r
                self._matrix[self._matrix.pixel_addrs(_x, _y)[self._matrix.g_offset]] = g
                self._matrix[self._matrix.pixel_addrs(_x, _y)[self._matrix.b_offset]] = b
        self._matrix.show()
