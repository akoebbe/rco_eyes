# SPDX-FileCopyrightText: 2020 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

""" Configuration data for the bot eyes """
EYE_PATH = __file__[:__file__.rfind('/') + 1]
EYE_DATA = {
    'eye_image'        : EYE_PATH + 'rcobot_8x8-eyes.bmp',
    'upper_lid_image'  : EYE_PATH + 'rcobot_8x8-upper-lids.bmp',
    'lower_lid_image'  : EYE_PATH + 'rcobot_8x8-lower-lids.bmp',
    'stencil_image'    : EYE_PATH + 'rcobot_8x8-stencil.bmp',
    'transparent'      : (255, 0, 255), # Transparent color in above images
    'eye_move_min'     : (-3, -3),     # eye_image (left, top) move limit
    'eye_move_max'     : (3, 3),     # eye_image (right, bottom) move limit
    'upper_lid_open'   : (0, -6),    # upper_lid_image pos when open
    'upper_lid_center' : (0, -4),    # " when eye centered
    'upper_lid_closed' : (0, 0),     # " when closed
    'lower_lid_open'   : (0, 6),    # lower_lid_image pos when open
    'lower_lid_center' : (0, 4),    # " when eye centered
    'lower_lid_closed' : (0, 0),    # " when closed
}
