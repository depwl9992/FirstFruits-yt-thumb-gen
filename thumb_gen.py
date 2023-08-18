#!/usr/bin/env python3
# See also: https://legacy.imagemagick.org/Usage/fonts/#soft_shadow
# Youtube thumbnail = 1280x720
# 
# First Fruits Vert = 46
# Scripture Vert = 256
# Title Vert = 357
#
# 3-Line:
#  - Scripture = 229
#  - Title 1 = 334
#  - Title 2 = 440
#
# Date Vert = 567
#
# Requirements: pip install Pillow
# See https://pillow.readthedocs.io/en/latest/installation.html for documentation.
#
# Usage:
# - Pre-load the program directory with input image and font files.
#   Note - it is helpful to crop out toolbars and resize to a 16x9 image beforehand,
#    but doing so is not required as the rescale_image() function will attempt to rescale
#    the background image anyway.
#   Fonts used: SitkaDisplay-Bold.ttf, SitkaDisplay-Italic.ttf, SitkaDisplay-BoldItalic.ttf
#
# - Run thumb_gen.py <filename of background image>
#   Note - The image path will be prompted for if it is omitted from the command line arg.
#    Additionally, the image will be checked for existence and validity before proceeding
#    to text inputs.
#
# - Enter text data as prompted.
#
# - The 1280x720 'thumbnail.png' image will be generated upon completion.
#
# Revision History:
# - 2023-08-11 (Daniel) - Initial revision. Kinda just works as is, but is command-line only.
#   If we can pass in text as arguments and run from a web form that would be super cool!!
#

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from datetime import datetime

########## GROUP NAME & TODAY'S DATE ############
NAME = {
    "font":"SitkaDisplay-Bold.ttf",
    "size":165,
    "top":47,
    "blur":15,
    "blur_offs":10,
    "color":"#76bee0",
    "stroke":12,
    "stroke_color":"black"
}

DATE = {
    "font":"SitkaDisplay-Italic.ttf",
    "size":73,
    "top":550,
    "blur":12,
    "blur_offs":6,
    "color":"#2f2f2f",
    "stroke":4,
    "stroke_color":"white"
}

########## USE FOR 2-LINE TITLES ##############
PASSAGE2 = {
    "font":"SitkaDisplay-Bold.ttf",
    "size":106,
    "top":256,
    "blur":15,
    "blur_offs":10,
    "color":"#b0d5dd",
    "stroke":8,
    "stroke_color":"black"
}

TITLE2_1 = {
    "font":"SitkaDisplay-BoldItalic.ttf",
    "size":106,
    "top":357,
    "blur":15,
    "blur_offs":10,
    "color":"#b0d5dd",
    "stroke":8,
    "stroke_color":"black"
}

########### USE FOR 3-LINE TITLES ################
PASSAGE3 = {
    "font":"SitkaDisplay-Bold.ttf",
    "size":106,
    "top":208,
    "blur":15,
    "blur_offs":10,
    "color":"#b0d5dd",
    "stroke":8,
    "stroke_color":"black"
}

TITLE3_1 = {
    "font":"SitkaDisplay-BoldItalic.ttf",
    "size":106,
    "top":306,
    "blur":15,
    "blur_offs":10,
    "color":"#b0d5dd",
    "stroke":8,
    "stroke_color":"black"
}

TITLE3_2 = {
    "font":"SitkaDisplay-BoldItalic.ttf",
    "size":106,
    "top":402,
    "blur":15,
    "blur_offs":10,
    "color":"#b0d5dd",
    "stroke":8,
    "stroke_color":"black"
}

# Process input image, oversize if necessary and crop to the required 1280x720 canvas.
def rescale_image(img):
    in_height = img.height
    in_width = img.width
    print(f"Original size : {in_width}x{in_height}")

    out_ratio = (1280/720)
    in_ratio = (in_width/in_height)
    if out_ratio > in_ratio: # Input image is too tall (letterbox, square, vertical)
        out_width=1280
        out_height=1280 / in_ratio
        
        left_1280 = 0
        right_1280= 1280
        top_720 = (out_height-720)/2
        bot_720 = top_720+720
        print(f"Image too tall - crop height after resize ({out_height} --> 720)")
        
        
    elif out_ratio < in_ratio: # Input image is too wide
        out_width=in_ratio * 720
        out_height = 720    
        
        left_1280=(out_width-1280)/2
        right_1280=left_1280+1280
        top_720=0
        bot_720=720
        print(f"Image too wide - crop width after resize ({out_width} --> 1280)")
        
        
    else: # Input image may only need scaling.
        out_height=720
        out_width=1280
        
        left_1280=0
        right_1280=1280
        top_720=0
        bot_720=720
        print("Image just right - resize only")
        
        
    area = (left_1280,top_720,right_1280,bot_720) # Final image size. We will crop to make sure this is the case.

    print(f"New size : {int(out_width)}x{int(out_height)}")
      
    if in_height != out_height and in_width != out_width:
        img = img.resize((int(out_width),int(out_height)))
        print("Resized to output, kept aspect ratio")
        
    if out_height != 720 or out_width != 1280:
        img = img.crop(area)
        print("Cropped to output. Should be 1280x720")
        
    return img

# Process text for each line and draw over background image using dictionary definitions for formatting and positioning.
def draw_text(img, text, dic):
# --------- Generate "First Fruits" Channel Name -----------
    x = img.width//2
    y = dic["top"] + (dic["size"]//2)

    # Create font
    font = ImageFont.truetype(dic["font"], dic["size"])

    # Create piece of canvas to draw text on and blur
    blurred = Image.new('RGBA', img.size)
    draw = ImageDraw.Draw(blurred)
    draw.text(xy=(x+dic["blur_offs"],y+dic["blur_offs"]), text=text, fill='black', font=font, anchor='mm')
    blurred = blurred.filter(ImageFilter.BoxBlur(dic["blur"]))

    # Paste soft text onto background
    img.paste(blurred,blurred)

    # Draw on sharp text
    draw = ImageDraw.Draw(img)
    draw.text(xy=(x,y), text=text, fill=dic["color"], font=font, anchor='mm', stroke_width=dic["stroke"], stroke_fill=dic["stroke_color"])

    return img