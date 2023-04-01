# pylint: disable=report-shadowed-imports
import busio
import board
from supervisor import ticks_ms
from adafruit_nunchuk import Nunchuk
import asyncio
import adafruit_debouncer as debouncer
from rco_eye import Eye, Pupil, Eyelid, Animator

from config import Config

# Specify pins
led_count = Config.led_count
led_height = Config.led_height
led_width = Config.led_width
led_center_x = int((Config.led_width - 1) / 2)
led_center_y = int((Config.led_height - 1) / 2)
pupil_px_bleed = Config.eye_theme.pupil_px_bleed

i2c = busio.I2C(board.SCL1, board.SDA1, frequency=1000000)

# i2c = board.STEMMA_I2C()
nc = Nunchuk(i2c)

left_pupil = Pupil(Config.eye_theme.pupil_image, Config.eye_theme.pupil_px_bleed)
right_pupil = Pupil(Config.eye_theme.pupil_image, Config.eye_theme.pupil_px_bleed)

left_eyelid = Eyelid(
    Config.eye_theme.left_top_eyelid,
    Config.eye_theme.left_bottom_eyelid,
    Config.eye_theme.eyelid_open_offset,
    Config.eye_theme.eyelid_squint_offset,
    Config.eye_theme.eyelid_closed_offset,
    Config.eye_theme.eyelid_wide_offset
)

right_eyelid = Eyelid(
    Config.eye_theme.right_top_eyelid, 
    Config.eye_theme.right_bottom_eyelid, 
    Config.eye_theme.eyelid_open_offset,
    Config.eye_theme.eyelid_squint_offset,
    Config.eye_theme.eyelid_closed_offset,
    Config.eye_theme.eyelid_wide_offset
)

left_eye = Eye(
    i2c, 
    Config.left_display_address,
    led_width, 
    led_height, 
    Config.led_brightness,
    Config.eye_theme.whites_color, 
    left_pupil, 
    left_eyelid
)
right_eye = Eye(
    i2c, 
    Config.right_display_address,
    led_width, 
    led_height, 
    Config.led_brightness,
    Config.eye_theme.whites_color, 
    right_pupil, 
    right_eyelid
)

animator = Animator(left_eye, right_eye)

c_button = debouncer.Button(lambda : nc.buttons.C, value_when_pressed=True)
z_button = debouncer.Button(lambda : nc.buttons.Z, value_when_pressed=True)

async def nunchuck_button_monitor():
    while True:
        c_button.update()
        z_button.update()

        if c_button.fell or c_button.rose or z_button.fell or z_button.rose:
            if z_button.pressed and c_button.pressed:
                animator.cross()
            elif c_button.pressed:
                animator.squint()
            elif z_button.pressed:
                animator.close()
            else:
                animator.open()

        await asyncio.sleep(0)

async def nunchuck_joystick_monitor():
    last_joy_position = nc.joystick

    while True:
        current_joy = nc.joystick
        if not last_joy_position == current_joy:
            
            x = (current_joy.x/255) if not Config.joystick_invert_x else ((255-current_joy.x)/255)
            y = ((255-current_joy.y)/255) if not Config.joystick_invert_y else (current_joy.y/255)

            left_eye.pupil_position(x, y)
            right_eye.pupil_position(x, y)

            last_joy_position = current_joy

            left_eye.draw()
            right_eye.draw()

        await asyncio.sleep(0)

async def nunchuck_accelerometer_monitor():
    while True:

        if nc.acceleration.x < 200:
            await animator.wink()

        if nc.acceleration.y < 200:
            animator.cross()
            await asyncio.sleep(1)
            animator.open()

        await asyncio.sleep(0)



async def main():
    nunchuck_joystick_task = asyncio.create_task(nunchuck_joystick_monitor())
    nunchuck_accelerometer_task = asyncio.create_task(nunchuck_accelerometer_monitor())
    nunchuck_buttton_task = asyncio.create_task(nunchuck_button_monitor())

    await asyncio.gather(nunchuck_joystick_task, nunchuck_buttton_task, nunchuck_accelerometer_task)

asyncio.run(main())