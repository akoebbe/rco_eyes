# Robot Co-op LED Eyes

The code is written in CircuitPython 8.0.2 and when you plug the controller in to 
your computer, it will show as a USB drive with all of the code and images. The 
controller will reboot everytime a file is changed on the USB drive, so it's best 
to turn any autosave feature off in your editor.

The boards all connect via STEMMA QT connectors and can be connected in any order 
using any of the ports. Use any USB-C power supply to power the eyes. They 
probably only need 1-2 amps at the standard 5v.

Code repository: https://github.com/akoebbe/rco_eyes

## Important Notes

> All references to "left" and "right" eyes (in code and documentation) is from 
> the perspective of the viewer and not of the bot. If this is a problem or
> confusing (or offensive to the bot), I can refactor that.

> Make sure the Wii Nunchuck is plugged in with the notch is oriented to the same
> as the "Notch Up" printed text on the board connector

```
,-----.       ,-----. 
|     | Notch |     |
|     `-------'     |
|    ,---------.    |
|    `---------'    |
`-------------------'
```

## Controls

|                     Button | Action                             |
| -------------------------: | ---------------------------------- |
|                   Joystick | Move pupil                         |
|                          C | Squint                             |
|                    Z (tap) | Blink                              |
|                   Z (hold) | Close eyelids                      |
|        Sharp Right or Left | Wink (Right eye)                   |
|           Sharp Up or Down | Cross eyes for 1 second            |
| C + Z (simultaneous, hold) | Cross eyes (difficult to pull off) |


## Configuration (`config.py`)

Global settings can be found in the `config.py` in the same folder as this file. 
The theme is selected by uncommenting the desired `from eyes.[theme folder].data 
import EyeTheme` line near the top. The other settings should be self explanitory 
or have a comment along side.

The `led_brightness` value is a range from `0` (off) to `255` (brightest). The 
red, green, and blue behave differently at different brightnesses, so you may have 
to tweak your bitmap colors if you change this value.

## Custom Themes

To make your own theme, copy one of the existing folders in the `/eyes` folder and 
edit/replace the bitmaps. You will probably need to edit the `data.py` file in the 
copied theme folder to specify any different image filenames and other theme 
settings. 

### Bitmap Specs

- Images need to be 8-bit, indexed BMP files.
- The first color in the index will be treated as transparent
- Eyes are layered (bottom to top) in the following order 
  1. Background Color
  2. Pupil
  3. Lower eye lid
  4. Upper eye lid

### Background Color

This will be the fallback color if all other pixels above are transparent. Think
of it as the "whites" of the eyes. This is simply a solid hex color.

### Pupil

The pupil should have an odd number for height and width since the displays are 
13x9. This will ensure the pupils will be centered. Make sure to crop the pupils 
as tight as possible. The smaller the pupil bitmap the faster the display will 
respond.

The `pupil_px_bleed`, while sounding metal af, sets the number of pixels the pupil 
is allowed to scroll off the screen when moving the joystick. The higher this 
value the further the pupil will move. In general, you probably want this to be 
less than half the width and height of your pupil bitmap. So if your pupil is 7px 
wide, then 2px or 3px would probably be a good bleed setting.

### Eyelids

Eyelid images should be 13px wide. The eyelids will extend above (top lid) and 
below (bottom lid) the display when the eye is open. As the eye closes the lids 
will slide in to cover more of the eye, resulting me more of the lids' bitmaps 
being shown.

The important thing to remember is that the two lids need to be tall enough to 
cover the whole eye when they are closed.

The eyelids also have several offset settings to control their position at 
different expressions: open, squint, closed, wide (wide not currently 
implemented). The number is how many rows of pixels should be visible for that 
expression. The higher the value, the more the lids cover the eye.

Optionally, you can take advantage of this by putting pixels in the normally 
off-screen area of the eyelid so that the hidden pixels will only show when the 
eyes squint/close.



## SPRITE LAYERING REFERENCE
```
              .---------------Visible Area---------------.
              |                               .----------------------.
              |                               |  <- Upper Eyelid ->  |
              |                                ----------------------
 .----------------------.                                |
 |  <- Lower Eyelid ->  |                                |
  ----------------------                                 |
              |        .-----------------------.         |
              |        |         Pupil <^>     |         |
              v         -----------------------          v
              .------------------------------------------.
              |             Background Color             |
               ------------------------------------------

                       Side view of bitmap layers
```



## EYELID OFFSET REFERENCE
```
  .---------------.
  | Top Eyelid    |
  |               |
.-|               |-.
| | ***********   | |1 -\              
| | **         *  | |2   3 pixel offset    |
| | *           * | |3 -/                  |
| '---------------' |4                     v
|                   |5       Increasing the offset brings
| .---------------. |6       the eyelids closer together 
| | *           * | |7                     ^
| |  *         *  | |8                     |
| |   *********   | |9                     |
'-|               |-' 
  |               |
  | Bottom Eyelid |
  '---------------'

                Top-down view of eyelid layers
```