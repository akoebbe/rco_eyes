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

from eyes.asmr_original.data import EyeTheme

class Config:
    eye_theme: EyeTheme = EyeTheme  

    # These settings are specific to the 13x9 LED displays. You shouldn't need to change these
    led_count = 117
    led_height = 9
    led_width = 13
