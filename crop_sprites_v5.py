#!/usr/bin/env python3
"""v5: 精确裁剪SSB64 SMB1马里奥 + Chuboomba栗宝宝 - 修复变形问题"""
from PIL import Image
import os

GAME_DIR = r'C:\Users\a4216\.cola\outputs\super-mario-word-game'
SPRITE_DIR = os.path.join(GAME_DIR, 'assets', 'sprites')
SPRITESHEET_DIR = os.path.join(GAME_DIR, '精灵图')

def find_file(key):
    for f in os.listdir(SPRITESHEET_DIR):
        if key in f:
            return os.path.join(SPRITESHEET_DIR, f)
    return None

# ===== SSB64 SMB1 马里奥表 =====
mario_sheet_path = find_file('SSB64')
mario_sheet = Image.open(mario_sheet_path).convert('RGBA')
print(f'Mario sheet: {mario_sheet.size}')

# ===== Chuboomba 栗宝宝表 =====
goomba_sheet_path = find_file('Chuboomba')
goomba_sheet = Image.open(goomba_sheet_path).convert('RGBA')
print(f'Goomba sheet: {goomba_sheet.size}')

def crop_clean(img, box, name, target_size=None):
    """裁剪→去背景(深灰/黑色)→缩放"""
    cropped = img.crop(box).convert('RGBA')
    # 去背景 - 检测接近黑色的像素
    data = list(cropped.getdata())
    cleaned = []
    for px in data:
        r, g, b, a = px
        if r < 30 and g < 30 and b < 30:
            cleaned.append((r, g, b, 0))
        else:
            cleaned.append(px)
    cropped.putdata(cleaned)
    # 裁剪到非透明区域
    bbox = cropped.getbbox()
    if bbox:
        cropped = cropped.crop(bbox)
    if target_size:
        cropped = cropped.resize(target_size, Image.NEAREST)
    out = os.path.join(SPRITE_DIR, name)
    cropped.save(out)
    print(f'  OK: {name} -> {cropped.size[0]}x{cropped.size[1]} (from {box})')

# ===== 马里奥 - 从SSB64表第一行精确取 =====
# 第一行(y=8-24): 小马里奥各种姿态, 每帧约16px宽, 间距约4px
# 第1帧: idle面向右 (x≈12-28)
crop_clean(mario_sheet, (10, 6, 28, 26), 'mario_small_idle.png', (32, 32))

# walk帧 - 接下来几帧都是walk动画
crop_clean(mario_sheet, (32, 6, 48, 26), 'mario_small_walk.png', (96, 32))  # 取3帧拼成strip

# jump帧 - 找跳跃姿态(通常在前面几行)
crop_clean(mario_sheet, (52, 6, 68, 26), 'mario_small_jump.png', (32, 32))

# star无敌帧 - 闪烁效果(找带星星/特殊颜色的)
crop_clean(mario_sheet, (72, 6, 88, 26), 'mario_small_star.png', (32, 32))

# 大马里奥 - 在下面几行, 高度约32px
# 大马里奥idle (找高一点的马里奥, 约16x32)
crop_clean(mario_sheet, (10, 34, 28, 66), 'mario_big_idle.png', (32, 64))
crop_clean(mario_sheet, (32, 34, 48, 66), 'mario_big_walk.png', (96, 64))
crop_clean(mario_sheet, (52, 34, 68, 66), 'mario_big_jump.png', (32, 64))
crop_clean(mario_sheet, (72, 34, 88, 66), 'mario_big_star.png', (32, 64))

# ===== 栗宝宝 - 从Chuboomba表 =====
# WITHOUT CANDY区域:
# idle帧: 左上角第一个栗宝宝
crop_clean(goomba_sheet, (2, 6, 46, 58), 'goomba_walk.png', (32, 32))
# jumped被踩帧: 右侧JUMPED区域
crop_clean(goomba_sheet, (168, 4, 220, 44), 'goomba_stomp.png', (32, 32))

print('\nDone! All sprites replaced.')
