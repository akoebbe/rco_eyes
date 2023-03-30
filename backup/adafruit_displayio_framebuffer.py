"""
`adafruit_displayio_framebuffer`
================================================================================

DisplayIO compatible library for mock framebuffers


* Author(s): akoebbe

Implementation Notes
--------------------

**Hardware:**
None!

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
import displayio


# No init sequence needed since we are using actual hardware
_INIT_SEQUENCE = (
    b"\x00\x00"  # display off, sleep mode
    b"\xd5\x01\x80"  # divide ratio/oscillator: divide by 2, fOsc (POR)
    # b"\xa8\x01\x3f"  # multiplex ratio = 64 (POR)
    # b"\xd3\x01\x00"  # set display offset mode = 0x0
    # b"\x40\x00"  # set start line
    # b"\xad\x01\x8b"  # turn on DC/DC
    # b"\xa1\x00"  # segment remap = 1 (POR=0, down rotation)
    # b"\xc8\x00"  # scan decrement
    # b"\xda\x01\x12"  # set com pins
    # b"\x81\x01\xff"  # contrast setting = 0xff
    # b"\xd9\x01\x1f"  # pre-charge/dis-charge period mode: 2 DCLKs/2 DCLKs (POR)
    # b"\xdb\x01\x40"  # VCOM deselect level = 0.770 (POR)
    # b"\x20\x01\x20"  #
    # b"\x33\x00"  # turn on VPP to 9V
    # b"\xa6\x00"  # normal (not reversed) display
    # b"\xa4\x00"  # entire display off, retain RAM, normal status (POR)
    # b"\xaf\x00"  # DISPLAY_ON
)


class FramebufferDisplay(displayio.Display):
    """
    Mock framebuffer driver for use with DisplayIO

    :param int width: The width of the display. Maximum of 132
    :param int height: The height of the display. Maximum of 64
    :param int rotation: The rotation of the display. 0, 90, 180 or 270.
    """

    def __init__(self, **kwargs) -> None:
        bus = None
        init_sequence = bytearray(_INIT_SEQUENCE)
        super().__init__(
            None,
            init_sequence,
            **kwargs
        )
        self._is_awake = True  # Display starts in active state (_INIT_SEQUENCE)

    def _initialize(self, init_sequence):
        pass

    @property
    def is_awake(self) -> bool:
        """
        The power state of the display. (read-only)

        `True` if the display is active, `False` if in sleep mode.
        """
        return self._is_awake

    def sleep(self) -> None:
        """
        Put display into sleep mode. The display uses < 5uA in sleep mode.

        Sleep mode does the following:

            1) Stops the oscillator and DC-DC circuits
            2) Stops the OLED drive
            3) Remembers display data and operation mode active prior to sleeping
            4) The MP can access (update) the built-in display RAM
        """
        if self._is_awake:
            self._is_awake = False

    def wake(self) -> None:
        """
        Wake display from sleep mode
        """
        if not self._is_awake:
            self._is_awake = True