#!/usr/bin/env python3
"""从精灵表裁剪游戏需要的29个精灵图"""
from PIL import Image, ImageDraw
import math
import os

GAME_DIR = r'C:\Users\a4216\.cola\outputs\super-mario-word-game'
SPRITE_DIR = os.path.join(GAME_DIR, 'assets', 'sprites')
SHEET_DIR = os.path.join(GAME_DIR, '精灵图')

os.makedirs(SPRITE_DIR, exist_ok=True)

def crop_and_save(img, box, output_name, target_size=None):
    """裁剪并保存，可选缩放到目标尺寸"""
    cropped = img.crop(box)
    if target_size:
        cropped = cropped.resize(target_size, Image.NEAREST)
    out_path = os.path.join(SPRITE_DIR, output_name)
    cropped.save(out_path)
    print(f'  OK: {output_name} ({cropped.size[0]}x{cropped.size[1]}) from box={box}')
    return out_path

# ===== 加载精灵表 =====
print('Loading sprite sheets...')
ssb64 = Image.open(os.path.join(SHEET_DIR, 'Custom _ Edited - Super Smash Bros. Customs - 01 Mario - Mario (SSB64 SMB1-Style).png'))
goomba_sheet = Image.open(os.path.join(SHEET_DIR, "SNES - Super Mario World 2_ Yoshi's Island - Enemies - Goomba.png"))
koopa_sheet = Image.open(os.path.join(SHEET_DIR, "SNES - Super Mario World 2_ Yoshi's Island - Enemies - Koopa & Paratroopa.png"))
bowser_sheet = Image.open(os.path.join(SHEET_DIR, "Custom _ Edited - Mario & Luigi Customs - Bowser's Inside Story Enemies - Chuboomba (SMB1 NES-Style).png"))
ground_sheet = Image.open(os.path.join(SHEET_DIR, 'Custom _ Edited - Mario Customs - Tilesets - Ground.png'))
pipe_sheet = Image.open(os.path.join(SHEET_DIR, 'SNES - Super Mario World - Miscellaneous - Pipes.png'))
print(f'  SSB64 Mario: {ssb64.size}')
print(f'  Goomba: {goomba_sheet.size}')
print(f'  Koopa: {koopa_sheet.size}')
print(f'  Bowser/Chuboomba: {bowser_sheet.size}')
print(f'  Ground: {ground_sheet.size}')
print(f'  Pipes: {pipe_sheet.size}')

# ===== 1. 马里奥精灵 =====
print('\n=== 1. Mario Sprites ===')

# SSB64 SMB1 Mario sprite layout (based on pixel analysis):
# y=16-31: small mario idle/walk frames (5 frames, each ~7px wide at x=16,24,32,41,48)
# y=32-47: small mario jump (~8px wide at x=41)
# y=48-79: big mario walk frames (many frames, 11-15px wide)
# y=80-95: EMPTY
# y=96-127: big mario idle/jump

# 小马里奥 idle (first frame from y=16-31 row)
crop_and_save(ssb64, (10, 13, 30, 33), 'mario_small_idle.png', (16, 16))

# 小马里奥 walk 3帧横条
walk_small = Image.new('RGBA', (48, 16), (0, 0, 0, 0))
for i, ox in enumerate([11, 19, 27]):
    frame = ssb64.crop((ox, 13, ox + 16, 33))
    frame = frame.resize((16, 16), Image.NEAREST)
    walk_small.paste(frame, (i * 16, 0))
walk_small.save(os.path.join(SPRITE_DIR, 'mario_small_walk.png'))
print('  OK: mario_small_walk.png (48x16, 3 frames)')

# 小马里奥 jump
crop_and_save(ssb64, (36, 30, 56, 50), 'mario_small_jump.png', (16, 16))

# 大马里奥 idle
crop_and_save(ssb64, (34, 93, 56, 129), 'mario_big_idle.png', (16, 32))

# 大马里奥 walk 3帧
walk_big = Image.new('RGBA', (48, 32), (0, 0, 0, 0))
# 大马里奥帧在 y=48-79 区域
big_frames_x = [35, 91, 149]
for i, ox in enumerate(big_frames_x):
    frame = ssb64.crop((ox, 45, ox + 16, 81))
    frame = frame.resize((16, 32), Image.NEAREST)
    walk_big.paste(frame, (i * 16, 0))
walk_big.save(os.path.join(SPRITE_DIR, 'mario_big_walk.png'))
print('  OK: mario_big_walk.png (48x32, 3 frames)')

# 大马里奥 jump
crop_and_save(ssb64, (335, 110, 358, 150), 'mario_big_jump.png', (16, 32))

# 星星马里奥 (用同款，颜色不同可以后续处理)
crop_and_save(ssb64, (10, 13, 30, 33), 'mario_small_star.png', (16, 16))
crop_and_save(ssb64, (34, 93, 56, 129), 'mario_big_star.png', (16, 32))

# ===== 2. 敌人精灵 =====
print('\n=== 2. Enemy Sprites ===')

# Goomba (406x59) - 横向排列的帧
crop_and_save(goomba_sheet, (5, 5, 55, 53), 'goomba_walk.png', (16, 16))
# Goomba stomped - 扁平版
stomped = Image.new('RGBA', (16, 8), (0, 0, 0, 0))
# 用goomba的某个姿态压扁
g = goomba_sheet.crop((5, 30, 55, 53))
g = g.resize((16, 8), Image.NEAREST)
stomped.paste(g, (0, 0))
stomped.save(os.path.join(SPRITE_DIR, 'goomba_stomp.png'))
print('  OK: goomba_stomp.png (16x8)')

# Koopa (991x1686) - 取前几个帧
crop_and_save(koopa_sheet, (10, 10, 60, 60), 'koopa_walk.png', (16, 24))
crop_and_save(koopa_sheet, (70, 20, 120, 60), 'koopa_shell.png', (16, 16))

# ===== 3. Boss (Chuboomba/SMB1 Bowser) =====
print('\n=== 3. Boss Sprites ===')
# Chuboomba (548x122) - SMB1 NES style Bowser
crop_and_save(bowser_sheet, (10, 5, 90, 110), 'bowser_idle.png', (40, 40))
crop_and_save(bowser_sheet, (100, 5, 180, 110), 'bowser_hurt.png', (40, 40))

# ===== 4. 物品精灵 =====
print('\n=== 4. Item Sprites ===')

# 金币 4帧动画
coin_img = Image.new('RGBA', (64, 16), (0, 0, 0, 0))
for i in range(4):
    for cx in range(16):
        for cy in range(16):
            dx, dy = cx - 8, cy - 8
            if dx * dx + dy * dy <= 36:
                angle = i * math.pi / 2
                brightness = int(abs(math.cos(angle + dx * 0.2)) * 55 + 200)
                coin_img.putpixel((i * 16 + cx, cy), (brightness, brightness, 0, 255))
coin_img.save(os.path.join(SPRITE_DIR, 'coin.png'))
print('  OK: coin.png (64x16, 4 frames)')

# 蘑菇
mushroom = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
for cx in range(16):
    for cy in range(16):
        dx, dy = cx - 8, cy - 9
        if dx * dx + dy * dy <= 20:
            mushroom.putpixel((cx, cy), (227, 57, 55, 255))
        elif 4 <= cy <= 15 and abs(dx) <= 4:
            mushroom.putpixel((cx, cy), (245, 222, 179, 255))
mushroom.save(os.path.join(SPRITE_DIR, 'mushroom.png'))
print('  OK: mushroom.png (16x16)')

# 星星
star = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
pts = [(8, 0), (10, 5), (16, 6), (11, 9), (13, 15), (8, 11), (3, 15), (5, 9), (0, 6), (6, 5)]
ImageDraw.Draw(star).polygon(pts, fill=(255, 215, 0, 255))
star.save(os.path.join(SPRITE_DIR, 'star.png'))
print('  OK: star.png (16x16)')

# ===== 5. 场景元素 =====
print('\n=== 5. Scene Elements ===')

# 地面 (808x496)
crop_and_save(ground_sheet, (8, 8, 40, 40), 'ground_top.png', (32, 32))
crop_and_save(ground_sheet, (48, 8, 80, 40), 'ground_fill.png', (32, 32))

# 问号块
block_q = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
dq = ImageDraw.Draw(block_q)
dq.rectangle([2, 2, 29, 29], fill=(255, 160, 0, 255), outline=(139, 69, 19, 255), width=2)
dq.text((10, 6), '?', fill=(255, 255, 255, 255))
block_q.save(os.path.join(SPRITE_DIR, 'block_question.png'))
print('  OK: block_question.png (32x32)')

# 普通砖块
block_b = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
db = ImageDraw.Draw(block_b)
db.rectangle([0, 0, 31, 31], fill=(180, 100, 50, 255), outline=(100, 50, 20, 255), width=2)
db.line([0, 16, 31, 16], fill=(100, 50, 20, 255), width=1)
db.line([16, 0, 16, 31], fill=(100, 50, 20, 255), width=1)
block_b.save(os.path.join(SPRITE_DIR, 'block_brick.png'))
print('  OK: block_brick.png (32x32)')

# 管道 (608x256)
crop_and_save(pipe_sheet, (5, 5, 69, 53), 'pipe_top.png', (64, 32))
crop_and_save(pipe_sheet, (5, 60, 69, 108), 'pipe_body.png', (64, 32))

# 云朵
cloud = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
dc = ImageDraw.Draw(cloud)
dc.ellipse([8, 8, 28, 24], fill=(255, 255, 255, 255))
dc.ellipse([20, 4, 44, 24], fill=(255, 255, 255, 255))
dc.ellipse([36, 10, 56, 26], fill=(255, 255, 255, 255))
cloud.save(os.path.join(SPRITE_DIR, 'cloud.png'))
print('  OK: cloud.png (64x32)')

# 山丘
hill = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
dh = ImageDraw.Draw(hill)
dh.polygon([(0, 48), (16, 16), (32, 32), (48, 8), (64, 48)], fill=(106, 176, 76, 255))
hill.save(os.path.join(SPRITE_DIR, 'hill.png'))
print('  OK: hill.png (64x64)')

# 单词路障
wb = Image.new('RGBA', (48, 40), (0, 0, 0, 0))
dwb = ImageDraw.Draw(wb)
dwb.rectangle([2, 2, 45, 37], fill=(139, 69, 19, 255), outline=(80, 40, 10, 255), width=2)
dwb.text((14, 10), 'ABC', fill=(255, 255, 255, 255))
wb.save(os.path.join(SPRITE_DIR, 'word_block.png'))
print('  OK: word_block.png (48x40)')

# ===== 完成 =====
print('\n=== Summary ===')
files = sorted(os.listdir(SPRITE_DIR))
pngs = [f for f in files if f.endswith('.png')]
print(f'Total PNG files: {len(pngs)}')
for f in pngs:
    fp = os.path.join(SPRITE_DIR, f)
    sz = Image.open(fp).size
    fsize = os.path.getsize(fp)
    print(f'  {f}: {sz[0]}x{sz[1]} ({fsize} bytes)')
