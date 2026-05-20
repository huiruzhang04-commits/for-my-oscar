#!/usr/bin/env python3
"""v4b: 用Chuboomba SMB1 NES风格精灵替换Goomba"""
from PIL import Image
import os

GAME_DIR = r'C:\Users\a4216\.cola\outputs\super-mario-word-game'
SPRITE_DIR = os.path.join(GAME_DIR, 'assets', 'sprites')
# 列出文件名
sprite_dir = os.path.join(GAME_DIR, '精灵图')
files = [x for x in os.listdir(sprite_dir) if 'Chuboomba' in x]
SHEET = os.path.join(sprite_dir, files[0])

sheet = Image.open(SHEET).convert('RGBA')
print(f'Sheet: {sheet.size}')

def crop_save(box, name, target_size=None):
    img = sheet.crop(box).convert('RGBA')
    data = list(img.getdata())
    cleaned = []
    for px in data:
        if abs(px[0]-20)<15 and abs(px[1]-20)<15 and abs(px[2]-20)<15:
            cleaned.append((px[0],px[1],px[2],0))
        else:
            cleaned.append(px)
    img.putdata(cleaned)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    if target_size:
        img = img.resize(target_size, Image.NEAREST)
    out = os.path.join(SPRITE_DIR, name)
    img.save(out)
    print(f'  OK: {name} ({img.size[0]}x{img.size[1]})')

# WITHOUT CANDY - idle帧 (第一个栗宝宝)
crop_save((4, 8, 48, 60), 'goomba_walk.png', (32, 32))
# jumped 被踩扁的帧
crop_save((170, 6, 218, 44), 'goomba_stomp.png', (32, 32))

print('\nDone!')
