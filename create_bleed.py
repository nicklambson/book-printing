from PIL import Image
from tkinter import Tk, filedialog, simpledialog
from pathlib import Path

def get_outside_pixels(im):
    width, height = im.size
    left = im.crop((0, 0, 1, height))
    right = im.crop((width - 1, 0, width, height))
    top = im.crop((0, 0, width, 1))
    bottom = im.crop((0, height - 1, width, height))
    return left, right, top, bottom

def get_left_right_bleed(im):
    width, height = im.size
    new_image = Image.new('CMYK', (width * ADD_PIXELS, height))
    for i in range(ADD_PIXELS):
        new_image.paste(im, (i, 0))
    return new_image

def get_top_bottom_bleed(im):
    width, height = im.size
    new_image = Image.new('CMYK', (width, height * ADD_PIXELS))
    for i in range(ADD_PIXELS):
        new_image.paste(im, (0, i))
    return new_image

def combine_bleeds(left, right, top, bottom, original):
    width, height = original.size
    new_image = Image.new('CMYK', (ADD_PIXELS * 2 + width, ADD_PIXELS * 2 + height))
    new_image.paste(left, (0, 0))
    new_image.paste(left, (0, ADD_PIXELS * 2))
    new_image.paste(left, (0, ADD_PIXELS))
    new_image.paste(right, (width + ADD_PIXELS, 0))
    new_image.paste(right, (width + ADD_PIXELS, ADD_PIXELS * 2))
    new_image.paste(right, (width + ADD_PIXELS, ADD_PIXELS))
    new_image.paste(top, (ADD_PIXELS, 0))
    new_image.paste(bottom, (ADD_PIXELS, height + ADD_PIXELS))
    new_image.paste(original, (ADD_PIXELS, ADD_PIXELS))
    return new_image

Tk().withdraw()

DPI = simpledialog.askinteger(title="Ask DPI...", prompt="What is your DPI? (Default: 300)", initialvalue=300)
MM_PER_INCH = 25.4
PIXELS_PER_MM = DPI / MM_PER_INCH
BLEED_MM = simpledialog.askinteger(title="Ask Bleed...", prompt="How much bleed (mm) to add to each side? (Default: 5mm)", initialvalue=5)
ADD_PIXELS = round(PIXELS_PER_MM * BLEED_MM)


# MY_IMAGE = filedialog.askopenfilename(title="Select file...", filetypes=(("PNG Files", "*.png"),))
MY_FOLDER = Path(filedialog.askdirectory(title="Select folder..."))
for image in MY_FOLDER.rglob("*.png"):
    print(f"Processing {image}...")
    im = Image.open(image)
    left, right, top, bottom = get_outside_pixels(im)


    left_bleed = get_left_right_bleed(left)
    right_bleed = get_left_right_bleed(right)
    top_bleed = get_top_bottom_bleed(top)
    bottom_bleed = get_top_bottom_bleed(bottom)

    new_image = combine_bleeds(left_bleed, right_bleed, top_bleed, bottom_bleed, im)
    new_name = image.stem + ".jpg"
    new_path = image.parent / new_name
    new_image.save(new_path, "JPEG")

