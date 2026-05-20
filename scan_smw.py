from PIL import Image
import os, glob

d = r'D:\Users\a4216\Downloads'
files = glob.glob(os.path.join(d, '*Yoshi*'))
img = Image.open(files[0]).convert('RGBA')
w, h = img.size
MAGENTA = (248, 0, 248)

# 精确扫描: 找每种元素的实际边界
def find_regions(target_color_range, min_size=10):
    """找到指定颜色范围的连续区域"""
    regions = []
    in_region = False
    start_x = 0
    for y in range(h):
        row = [img.getpixel((x, y))[:3] for x in range(w)]
        for x in range(w):
            r, g, b = row[x]
            match = target_color_range(r, g, b)
            if match and not in_region:
                in_region = True
                start_x = x
                region_y = y
            elif not match and in_region:
                in_region = False
                if x - start_x > min_size:
                    regions.append((start_x, region_y, x, y))
    return regions

print('=== Scanning for pipes (green + white highlight) ===')
# 管道特征: 深绿色(0,160-200,0) + 白色高光
def is_pipe(r, g, b):
    return g > 140 and r < 60 and b < 60 and (r,g,b) != MAGENTA

pipe_regions = find_regions(is_pipe, 20)
for reg in pipe_regions[:5]:
    print(f'  Pipe region: {reg}')

print('\n=== Scanning for ground/bricks (brown) ===')
def is_brown(r, g, b):
    return r > 160 and g > 80 and g < 200 and b < 120 and (r,g,b) != MAGENTA

brown_regions = find_regions(is_brown, 30)
for reg in brown_regions[:10]:
    print(f'  Brown region: {reg}')

print('\n=== Scanning for question blocks (yellow) ===')  
def is_yellow(r, g, b):
    return r > 220 and g > 200 and b < 80 and (r,g,b) != MAGENTA

yellow_regions = find_regions(is_yellow, 5)
for reg in yellow_regions[:10]:
    print(f'  Yellow region: {reg}')

print('\n=== Scanning for coins (bright yellow) ===')
def is_coin(r, g, b):
    return r > 230 and g > 220 and b < 60 and (r,g,b) != MAGENTA

coin_regions = find_regions(is_coin, 3)
for reg in coin_regions[:10]:
    print(f'  Coin region: {reg}')
