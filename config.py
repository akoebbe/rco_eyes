"""
              .---------------Visible Area---------------.
              |                               .----------------------.
              |                               |     Upper Eyelid     |
              |                               '----------------------'
 .----------------------.                                |
 |     Lower Eyelid     |                                |
 '----------------------'                                |
              |        .-----------------------.         |
              |        |         Pupil         |         |
              v        '-----------------------'         v
              .------------------------------------------.
              |             Background Color             |
              '------------------------------------------'

                       Side view of bitmap layers

"""

# Uncomment the line with the theme you want. Comment out the others.
from eyes.asmr_original.data import EyeTheme
#from eyes.asmr_hearts.data import EyeTheme
#from eyes.asmr_real.data import EyeTheme

class Config:
    eye_theme: EyeTheme = EyeTheme  
    joystick_invert_x = False # Capitalize the first letter of booleans
    joystick_invert_y = False # Capitalize the first letter of booleans

    led_brightness = 1 # 0-255

    # These settings are specific to the 13x9 LED displays. You shouldn't need to change these
    led_count = 117
    led_height = 9
    led_width = 13
    left_display_address = 0x30
    right_display_address = 0x31
