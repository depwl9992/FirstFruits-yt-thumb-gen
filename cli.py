#!/usr/env python3
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from datetime import datetime
import thumb_gen
import os

####### START OF THE MAIN THREAD ###########################################
fn = ""
bg = ""
path=Path(fn)
if len(sys.argv) == 2:
    print(f"Opening {sys.argv[1]}...")
    fn = sys.argv[1]
    path = Path(fn)

while (True):    
    while (not path.is_file()):
        fn = input("Enter filename of image: ")
        path = Path(fn)
    
    # Open background image and work out centre
    try:
        bg = Image.open(fn).convert('RGB')
        bg.verify()
        print("Background image loaded!")
        break #Exit infinite loop when image is validated!
    except Exception:
        print("Invalid image")
        fn = ""
        path = Path(fn)
        continue
    
    
now = datetime.now()
fDate = now.strftime("%Y-%m-%d") # Initial input date. We'll reformat for text and filename later.

passage = input("Enter today's passage: ")
is_2_line = input("Will your title need 2 lines? (Y/N): ")

if is_2_line == "Y" or is_2_line == "y":
    title = input("Enter the first line of the title: ")
    title2 = input("Enter the second line of the title: ")
else:
    title = input("Enter the title: ")
    title2 = ""

is_today = input(f"Is this thumbnail for today on {fDate}? (Y/N): ")
if is_today == "N" or is_today == "n":
    while (True):
        fDate = input("Enter today's date as 'YYYY-MM-DD': ") # Get parseable user-entered date and preserve for backlog of thumbnails plus filenaming.
        try:
            thumb_date = datetime.strptime(fDate, "%Y-%m-%d").date()
            break
        except Exception:
            print("Incorrect date format!")
            continue
            
    fDate = thumb_date.strftime("%B %d, %Y")
else:
    thumb_date = datetime.strptime(fDate, "%Y-%m-%d").date()
    fDate = thumb_date.strftime("%B %d, %Y")
    
thumb = thumb_gen.rescale_image(bg)

thumb = thumb_gen.draw_text(thumb, "First Fruits", thumb_gen.NAME)

if is_2_line:
    thumb = thumb_gen.draw_text(thumb, passage, thumb_gen.PASSAGE3)
    thumb = thumb_gen.draw_text(thumb, title, thumb_gen.TITLE3_1)
    thumb = thumb_gen.draw_text(thumb, title2, thumb_gen.TITLE3_2)
else:
    thumb = thumb_gen.draw_text(thumb, passage, thumb_gen.PASSAGE2)
    thumb = thumb_gen.draw_text(thumb, title, thumb_gen.TITLE2_1)

thumb = thumb_gen.draw_text(thumb, fDate, thumb_gen.DATE)

isExist = os.path.exists("output/")
if not isExist:
    os.makedirs("output/")
    
fnDate = thumb_date.strftime("output/%Y-%m-%d.png")

if fn == fnDate:
    fnDateBak = thumb_date.strftime("output/%Y-%m-%d_bak.png")
    bg.save(fnDateBak)
    
thumb.save(fnDate)