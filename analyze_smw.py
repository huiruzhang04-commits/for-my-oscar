from PIL import Image
import os, glob

d = r'D:\Users\a4216\Downloads'
files = glob.glob(os.path.join(d, '*Yoshi*'))
if not files:
    files = glob.glob(os.path.join(d, '*Mario World*'))
img_path = files[0]
print(f'File: {img_path}')

img = Image.open(img_path)
print(f'Size: {img.size}, Mode: {img.mode}')

w, h = img.size

for y in range(0, h, 20):
    row_pixels = [img.getpixel((x, y)) for x in range(w)]
    non_black = [(x, px) for x, px in enumerate(row_pixels) if px[0] > 15 or px[1] > 15 or px[2] > 15]
    if non_black:
        xs = [x for x, _ in non_black]
        colors = set()
        step = max(1, len(non_black) // 10)
        for _, px in non_black[::step]:
            colors.add((px[0], px[1], px[2]))
        print(f'y={y:3d}: x={min(xs):4d}-{max(xs):4d}  colors={list(colors)[:5]}')
