# See /eyes/README.txt for reference diagrams

EYE_PATH = __file__[:__file__.rfind('/') + 1] # Leave this line alone, it just figures out the folder

class EyeTheme:
    pupil_image = EYE_PATH + 'pupil.bmp' # should have an odd number of pixels for width and height
    pupil_px_bleed = 2 # How many pixels of the pupil are allowed off the edges of the display

    whites_color = 0x000000

    right_top_eyelid = EYE_PATH + 'eyelid-top-right.bmp' # 13px wide
    right_bottom_eyelid = EYE_PATH + 'eyelid-bottom.bmp' # 13px wide
    left_top_eyelid = EYE_PATH + 'eyelid-top-left.bmp' # 13px wide
    left_bottom_eyelid = EYE_PATH + 'eyelid-bottom.bmp' # 13px wide
    
    eyelid_open_offset = 3 # pixel rows visible
    eyelid_squint_offset = 5
    eyelid_closed_offset = 7
    eyelid_wide_offset = 2
    

