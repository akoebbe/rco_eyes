# pylint: disable=report-shadowed-imports
import math
import sys
import busio
import random
import time
import board
import displayio
import framebufferio
import adafruit_imageload
import adafruit_is31fl3741
from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT
import is31fl3741_framebuf
import adafruit_framebuf

# Specify pins
eye_cin = board.A0
eye_din = board.A1
eye_led_count = 64
eye_led_height = 8
eye_led_width = 8

# TO LOAD DIFFERENT EYE DESIGNS: change the middle word here (between
# 'eyes.' and '.data') to one of the folder names inside the 'eyes' folder:
# from eyes.werewolf.data import EYE_DATA
# from eyes.cyclops.data import EYE_DATA
# from eyes.kobold.data import EYE_DATA
# from eyes.adabot.data import EYE_DATA
# from eyes.skull.data import EYE_DATA
# pylint: disable=wrong-import-position
from eyes.rcobot_8x8.data import EYE_DATA

# UTILITY FUNCTIONS AND CLASSES --------------------------------------------

# pylint: disable=too-few-public-methods
class Sprite(displayio.TileGrid):
    """Single-tile-with-bitmap TileGrid subclass, adds a height element
    because TileGrid doesn't appear to have a way to poll that later,
    object still functions in a displayio.Group.
    """

    height = 0

    def __init__(self, filename, transparent=None):
        """Create Sprite object from color-paletted BMP file, optionally
        set one color to transparent (pass as RGB tuple or list to locate
        nearest color, or integer to use a known specific color index).
        """
        bitmap, palette = adafruit_imageload.load(
            filename, bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        if isinstance(transparent, (tuple, list)):  # Find closest RGB match
            closest_distance = 0x1000000  # Force first match
            for color_index, color in enumerate(palette):  # Compare each...
                delta = (
                    transparent[0] - ((color >> 16) & 0xFF),
                    transparent[1] - ((color >> 8) & 0xFF),
                    transparent[2] - (color & 0xFF),
                )
                rgb_distance = (
                    delta[0] * delta[0] + delta[1] * delta[1] + delta[2] * delta[2]
                )  # Actually dist^2
                if rgb_distance < closest_distance:  # but adequate for
                    closest_distance = rgb_distance  # compare purposes,
                    closest_index = color_index  # no sqrt needed
            palette.make_transparent(closest_index)
        elif isinstance(transparent, int):
            palette.make_transparent(transparent)
        super(Sprite, self).__init__(bitmap, pixel_shader=palette)
        self.height = bitmap.height


# ONE-TIME INITIALIZATION --------------------------------------------------

displayio.release_displays()

# Create our own I2C bus with a 1Mhz frequency for faster updates
# i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
i2c = board.STEMMA_I2C()

matrix = Adafruit_RGBMatrixQT(i2c=i2c, address=0x30, allocate=adafruit_is31fl3741.PREFER_BUFFER)
matrix.set_led_scaling(0x01)
matrix.global_current = 0xff
matrix.enable = True




framebuf = is31fl3741_framebuf.IS31Framebuffer(matrix, 13, 9)

framebuf.fill(0xFF0000)
framebuf.display()

display = framebufferio.FramebufferDisplay(framebuf)


while True:
    pass

# Initialize the IS31FL3741 displayio display
# is31_fb = is31fl3741.FrameBuffer(
#     width=13,
#     height=9,
#     is31=is31,
#     scale=True,
#     gamma=True
# )
# display = framebufferio.FramebufferDisplay(is31_fb, auto_refresh=True)

# Turn the brightness down


# Order in which sprites are added determines the 'stacking order' and
# visual priority. Lower lid is added before the upper lid so that if they
# overlap, the upper lid is 'on top' (e.g. if it has eyelashes or such).
SPRITES = displayio.Group()
SPRITES.append(Sprite(EYE_DATA["eye_image"]))  # Base image is opaque
SPRITES.append(Sprite(EYE_DATA["lower_lid_image"], EYE_DATA["transparent"]))
SPRITES.append(Sprite(EYE_DATA["upper_lid_image"], EYE_DATA["transparent"]))
SPRITES.append(Sprite(EYE_DATA["stencil_image"], EYE_DATA["transparent"]))


# buf = framebufferio.FramebufferDisplay(framebuffer=pixel_framebuffer.buf)

# framebuf = is31.IS31FL3741_FrameBuffer(matrix)
# fb = framebufferio.FramebufferDisplay(framebuf)

display.show(SPRITES)


EYE_CENTER = (
    (EYE_DATA["eye_move_min"][0] + EYE_DATA["eye_move_max"][0])  # Pixel coords of eye
    / 2,  # image when centered
    (EYE_DATA["eye_move_min"][1] + EYE_DATA["eye_move_max"][1])  # ('neutral' position)
    / 2,
)
EYE_RANGE = (
    abs(
        EYE_DATA["eye_move_max"][0]
        - EYE_DATA["eye_move_min"][0]  # Max eye image motion
    )
    / 2,  # delta from center
    abs(EYE_DATA["eye_move_max"][1] - EYE_DATA["eye_move_min"][1]) / 2,
)
UPPER_LID_MIN = (
    min(
        EYE_DATA["upper_lid_open"][0],  # Motion bounds of
        EYE_DATA["upper_lid_closed"][0],
    ),  # upper and lower
    min(EYE_DATA["upper_lid_open"][1], EYE_DATA["upper_lid_closed"][1]),  # eyelids
)
UPPER_LID_MAX = (
    max(EYE_DATA["upper_lid_open"][0], EYE_DATA["upper_lid_closed"][0]),
    max(EYE_DATA["upper_lid_open"][1], EYE_DATA["upper_lid_closed"][1]),
)
LOWER_LID_MIN = (
    min(EYE_DATA["lower_lid_open"][0], EYE_DATA["lower_lid_closed"][0]),
    min(EYE_DATA["lower_lid_open"][1], EYE_DATA["lower_lid_closed"][1]),
)
LOWER_LID_MAX = (
    max(EYE_DATA["lower_lid_open"][0], EYE_DATA["lower_lid_closed"][0]),
    max(EYE_DATA["lower_lid_open"][1], EYE_DATA["lower_lid_closed"][1]),
)
EYE_PREV = (0, 0)
EYE_NEXT = (0, 0)
MOVE_STATE = False  # Initially stationary
MOVE_EVENT_DURATION = random.uniform(0.1, 3)  # Time to first move
BLINK_STATE = 2  # Start eyes closed
BLINK_EVENT_DURATION = random.uniform(0.25, 0.5)  # Time for eyes to open
TIME_OF_LAST_MOVE_EVENT = TIME_OF_LAST_BLINK_EVENT = time.monotonic()


# MAIN LOOP ----------------------------------------------------------------

while True:
    NOW = time.monotonic()
    # Eye movement ---------------------------------------------------------

    if NOW - TIME_OF_LAST_MOVE_EVENT > MOVE_EVENT_DURATION:
        TIME_OF_LAST_MOVE_EVENT = NOW  # Start new move or pause
        MOVE_STATE = not MOVE_STATE  # Toggle between moving & stationary
        if MOVE_STATE:  # Starting a new move?
            MOVE_EVENT_DURATION = random.uniform(0.08, 0.17)  # Move time
            ANGLE = random.uniform(0, math.pi * 2)
            EYE_NEXT = (
                math.cos(ANGLE) * EYE_RANGE[0],  # (0,0) in center,
                math.sin(ANGLE) * EYE_RANGE[1],
            )  # NOT pixel coords
        else:  # Starting a new pause
            MOVE_EVENT_DURATION = random.uniform(0.04, 3)  # Hold time
            EYE_PREV = EYE_NEXT

    # Fraction of move elapsed (0.0 to 1.0), then ease in/out 3*e^2-2*e^3
    RATIO = (NOW - TIME_OF_LAST_MOVE_EVENT) / MOVE_EVENT_DURATION
    RATIO = 3 * RATIO * RATIO - 2 * RATIO * RATIO * RATIO
    EYE_POS = (
        EYE_PREV[0] + RATIO * (EYE_NEXT[0] - EYE_PREV[0]),
        EYE_PREV[1] + RATIO * (EYE_NEXT[1] - EYE_PREV[1]),
    )

    # Blinking -------------------------------------------------------------

    if NOW - TIME_OF_LAST_BLINK_EVENT > BLINK_EVENT_DURATION:
        TIME_OF_LAST_BLINK_EVENT = NOW  # Start change in blink
        BLINK_STATE += 1  # Cycle paused/closing/opening
        if BLINK_STATE == 1:  # Starting a new blink (closing)
            BLINK_EVENT_DURATION = random.uniform(0.03, 0.07)
        elif BLINK_STATE == 2:  # Starting de-blink (opening)
            BLINK_EVENT_DURATION *= 2
        else:  # Blink ended,
            BLINK_STATE = 0  # paused
            BLINK_EVENT_DURATION = random.uniform(BLINK_EVENT_DURATION * 3, 4)
    if BLINK_STATE:  # Currently in a blink?
        # Fraction of closing or opening elapsed (0.0 to 1.0)
        RATIO = (NOW - TIME_OF_LAST_BLINK_EVENT) / BLINK_EVENT_DURATION
        if BLINK_STATE == 2:  # Opening
            RATIO = 1.0 - RATIO  # Flip ratio so eye opens instead of closes
    else:  # Not blinking
        RATIO = 0

    # Eyelid tracking ------------------------------------------------------

    # Initial estimate of 'tracked' eyelid positions
    UPPER_LID_POS = (
        EYE_DATA["upper_lid_center"][0] + EYE_POS[0],
        EYE_DATA["upper_lid_center"][1] + EYE_POS[1],
    )
    LOWER_LID_POS = (
        EYE_DATA["lower_lid_center"][0] + EYE_POS[0],
        EYE_DATA["lower_lid_center"][1] + EYE_POS[1],
    )
    # Then constrain these to the upper/lower lid motion bounds
    UPPER_LID_POS = (
        min(max(UPPER_LID_POS[0], UPPER_LID_MIN[0]), UPPER_LID_MAX[0]),
        min(max(UPPER_LID_POS[1], UPPER_LID_MIN[1]), UPPER_LID_MAX[1]),
    )
    LOWER_LID_POS = (
        min(max(LOWER_LID_POS[0], LOWER_LID_MIN[0]), LOWER_LID_MAX[0]),
        min(max(LOWER_LID_POS[1], LOWER_LID_MIN[1]), LOWER_LID_MAX[1]),
    )
    # Then interpolate between bounded tracked position to closed position
    UPPER_LID_POS = (
        UPPER_LID_POS[0] + RATIO * (EYE_DATA["upper_lid_closed"][0] - UPPER_LID_POS[0]),
        UPPER_LID_POS[1] + RATIO * (EYE_DATA["upper_lid_closed"][1] - UPPER_LID_POS[1]),
    )
    LOWER_LID_POS = (
        LOWER_LID_POS[0] + RATIO * (EYE_DATA["lower_lid_closed"][0] - LOWER_LID_POS[0]),
        LOWER_LID_POS[1] + RATIO * (EYE_DATA["lower_lid_closed"][1] - LOWER_LID_POS[1]),
    )

    # Move eye sprites -----------------------------------------------------

    SPRITES[0].x, SPRITES[0].y = (
        int(EYE_CENTER[0] + EYE_POS[0] + 0.5),
        int(EYE_CENTER[1] + EYE_POS[1] + 0.5),
    )
    SPRITES[2].x, SPRITES[2].y = (
        int(UPPER_LID_POS[0] + 0.5),
        int(UPPER_LID_POS[1] + 0.5),
    )
    SPRITES[1].x, SPRITES[1].y = (
        int(LOWER_LID_POS[0] + 0.5),
        int(LOWER_LID_POS[1] + 0.5),
    )
