#!/usr/bin/env python3
"""v4: 用Ground瓦片集替换所有场景精灵 - 云朵/山丘/砖块/管道/地面全部用真实素材"""
from PIL import Image, ImageDraw
import os

GAME_DIR = r'C:\Users\a4216\.cola\outputs\super-mario-word-game'
SPRITE_DIR = os.path.join(GAME_DIR, 'assets', 'sprites')
SHEET = os.path.join(GAME_DIR, '精灵图',
    'Custom _ Edited - Mario Customs - Tilesets - Ground.png')

sheet = Image.open(SHEET).convert('RGBA')
print(f'Sheet: {sheet.size}')

def crop_save(box, name, target_size=None, bg=(20,20,20)):
    """裁剪+去背景+缩放"""
    img = sheet.crop(box).convert('RGBA')
    data = list(img.getdata())
    cleaned = []
    for px in data:
        if abs(px[0]-bg[0])<15 and abs(px[1]-bg[1])<15 and abs(px[2]-bg[2])<15:
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

# ===== 云朵 - 左上角区域 =====
# 多种云朵形态，选最清晰的几款
crop_save((28, 8, 108, 58), 'cloud.png', (128, 64))       # 大云朵
crop_save((120, 10, 180, 45), 'cloud_small.png', (64, 32)) # 小云朵(备用)

# ===== 山丘/建筑 - 紫色圆柱 =====
crop_save((4, 170, 148, 296), 'hill.png', (128, 128))      # 大山丘组
crop_save((156, 190, 260, 290), 'hill_small.png', (96, 80)) # 小山丘

# ===== 地面砖块 - 棕色区域左下 =====
# 地面顶层(有草的)
crop_save((4, 300, 36, 332), 'ground_top.png', (64, 64))
# 地面填充层
crop_save((38, 300, 70, 332), 'ground_fill.png', (64, 64))

# ===== 问号块 - 橙色?块 =====
# 找问号块位置: 看图片右侧中间有橙色?块
crop_save((588, 302, 618, 332), 'block_question.png', (64, 64))

# ===== 普通砖块 =====
crop_save((4, 336, 36, 368), 'block_brick.png', (64, 64))

# ===== 管道 - 灰色/绿色管道 =====
# 管道头部(圆顶)
crop_save((388, 300, 450, 332), 'pipe_top.png', (128, 64))
# 管道身体
crop_save((388, 336, 450, 368), 'pipe_body.png', (128, 64))

# ===== 额外: 装饰性砖块变体 =====
# 可以保留备用

print('\n=== Done! ===')
files = sorted([f for f in os.listdir(SPRITE_DIR) if f.endswith('.png')])
total = sum(os.path.getsize(os.path.join(SPRITE_DIR,f)) for f in files)
print(f'Total sprites: {len(files)}, {total} bytes')
