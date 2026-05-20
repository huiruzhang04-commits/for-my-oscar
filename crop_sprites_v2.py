#!/usr/bin/env python3
"""从精灵表精确裁剪游戏需要的29个精灵图 - v2 精确版"""
from PIL import Image, ImageDraw
import math
import os

GAME_DIR = r'C:\Users\a4216\.cola\outputs\super-mario-word-game'
SPRITE_DIR = os.path.join(GAME_DIR, 'assets', 'sprites')
SHEET_DIR = os.path.join(GAME_DIR, '精灵图')
os.makedirs(SPRITE_DIR, exist_ok=True)

def crop_exact(img, box, output_name, target_size):
    """精确裁剪到非背景边界，然后缩放到目标尺寸"""
    cropped = img.crop(box)
    # 去除背景色(20,20,20)
    cropped = cropped.convert('RGBA')
    datas = cropped.getdata()
    new_data = []
    for item in datas:
        r, g, b = item[0], item[1], item[2]
        if abs(r-20) < 15 and abs(g-20) < 15 and abs(b-20) < 15:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, 255 if len(item)<4 else item[3]))
    cropped.putdata(new_data)
    
    # 找实际内容边界
    bbox = cropped.getbbox()
    if bbox:
        cropped = cropped.crop(bbox)
    
    # 缩放到目标尺寸 (NEAREST保持像素锐利)
    result = cropped.resize(target_size, Image.NEAREST)
    out_path = os.path.join(SPRITE_DIR, output_name)
    result.save(out_path)
    print(f'  OK: {output_name} ({result.size[0]}x{result.size[1]}) from raw={box}')
    return out_path

# ===== 加载精灵表 =====
print('Loading sprite sheets...')
ssb64 = Image.open(os.path.join(SHEET_DIR,
    'Custom _ Edited - Super Smash Bros. Customs - 01 Mario - Mario (SSB64 SMB1-Style).png'))
goomba_sheet = Image.open(os.path.join(SHEET_DIR,
    "SNES - Super Mario World 2_ Yoshi's Island - Enemies - Goomba.png"))
koopa_sheet = Image.open(os.path.join(SHEET_DIR,
    "SNES - Super Mario World 2_ Yoshi's Island - Enemies - Koopa & Paratroopa.png"))
bowser_sheet = Image.open(os.path.join(SHEET_DIR,
    "Custom _ Edited - Mario & Luigi Customs - Bowser's Inside Story Enemies - Chuboomba (SMB1 NES-Style).png"))
ground_sheet = Image.open(os.path.join(SHEET_DIR,
    'Custom _ Edited - Mario Customs - Tilesets - Ground.png'))
pipe_sheet = Image.open(os.path.join(SHEET_DIR,
    'SNES - Super Mario World - Miscellaneous - Pipes.png'))

# SSB64 SMB1 Mario 精灵表布局分析结果：
# 小马里奥 idle/walk: y=17-24 (仅7px高!), 帧在 x=16,24,32,41,48 (每帧~7px宽)
# 小马里奥 jump: y=46-53 (7px高), x=38-50
# 大马里奥 walk: y=48-65 (17px高), 多帧分散排列
# 大马里奥 idle: y=107-135 (28px高), x=39-72
# 大马里奥 jump: y=110-143 (33px高), x=330-355

print('\n=== 1. Mario Sprites (precise crop + scale) ===')

# 小马里奥 idle - 第一帧 (16,17)-(38,24), 实际约22x7 → 放大到16x16
crop_exact(ssb64, (14, 14, 40, 28), 'mario_small_idle.png', (16, 16))

# 小马里奥 walk 3帧横条 (48x16)
walk_small = Image.new('RGBA', (48, 16), (0, 0, 0, 0))
frame_positions = [(14, 14, 26, 26), (24, 14, 38, 26), (34, 14, 48, 26)]
for i, box in enumerate(frame_positions):
    frame = ssb64.crop(box).convert('RGBA')
    # 去背景
    data = list(frame.getdata())
    cleaned = []
    for px in data:
        if abs(px[0]-20)<15 and abs(px[1]-20)<15 and abs(px[2]-20)<15:
            cleaned.append((px[0], px[1], px[2], 0))
        else:
            cleaned.append((px[0], px[1], px[2], 255))
    frame.putdata(cleaned)
    bbox = frame.getbbox()
    if bbox:
        frame = frame.crop(bbox)
    frame = frame.resize((16, 16), Image.NEAREST)
    walk_small.paste(frame, (i * 16, 0), frame if frame.mode=='RGBA' else None)
walk_small.save(os.path.join(SPRITE_DIR, 'mario_small_walk.png'))
print('  OK: mario_small_walk.png (48x16, 3 frames)')

# 小马里奥 jump
crop_exact(ssb64, (36, 42, 54, 56), 'mario_small_jump.png', (16, 16))

# 大马里奥 idle - (39,107)-(72,135) 约23x28 → 缩放到16x32
crop_exact(ssb64, (37, 105, 68, 137), 'mario_big_idle.png', (16, 32))

# 大马里奥 walk 3帧 (48x32)
walk_big = Image.new('RGBA', (48, 32), (0, 0, 0, 0))
big_frame_boxes = [(36, 45, 52, 68), (92, 46, 112, 67), (142, 47, 165, 67)]
for i, box in enumerate(big_frame_boxes):
    frame = ssb64.crop(box).convert('RGBA')
    data = list(frame.getdata())
    cleaned = []
    for px in data:
        if abs(px[0]-20)<15 and abs(px[1]-20)<15 and abs(px[2]-20)<15:
            cleaned.append((px[0], px[1], px[2], 0))
        else:
            cleaned.append((px[0], px[1], px[2], 255))
    frame.putdata(cleaned)
    bbox = frame.getbbox()
    if bbox:
        frame = frame.crop(bbox)
    frame = frame.resize((16, 32), Image.NEAREST)
    walk_big.paste(frame, (i * 16, 0), frame if frame.mode=='RGBA' else None)
walk_big.save(os.path.join(SPRITE_DIR, 'mario_big_walk.png'))
print('  OK: mario_big_walk.png (48x32, 3 frames)')

# 大马里奥 jump
crop_exact(ssb64, (328, 108, 360, 145), 'mario_big_jump.png', (16, 32))

# 星星马里奥 (同款)
crop_exact(ssb64, (14, 14, 40, 28), 'mario_small_star.png', (16, 16))
crop_exact(ssb64, (37, 105, 68, 137), 'mario_big_star.png', (16, 32))

# ===== 2. 敌人 =====
print('\n=== 2. Enemy Sprites ===')

# Goomba - Yoshi's Island sheet (406x59), 有透明通道
g_walk = goomba_sheet.crop((5, 2, 55, 55)).convert('RGBA')
g_walk = g_walk.resize((16, 16), Image.NEAREST)
g_walk.save(os.path.join(SPRITE_DIR, 'goomba_walk.png'))
print(f'  OK: goomba_walk.png (16x16)')

# Goomba stomped - 取扁平部分或压扁
g_stomp = goomba_sheet.crop((60, 25, 120, 52)).convert('RGBA')
bbox = g_stomp.getbbox()
if bbox:
    g_stomp = g_stomp.crop(bbox)
g_stomp = g_stomp.resize((16, 8), Image.NEAREST)
g_stomp.save(os.path.join(SPRITE_DIR, 'goomba_stomp.png'))
print(f'  OK: goomba_stomp.png (16x8)')

# Koopa walk
k_walk = koopa_sheet.crop((12, 10, 65, 75)).convert('RGBA')
bbox = k_walk.getbbox()
if bbox:
    k_walk = k_walk.crop(bbox)
k_walk = k_walk.resize((16, 24), Image.NEAREST)
k_walk.save(os.path.join(SPRITE_DIR, 'koopa_walk.png'))
print(f'  OK: koopa_walk.png (16x24)')

# Koopa shell
k_shell = koopa_sheet.crop((70, 18, 130, 62)).convert('RGBA')
bbox = k_shell.getbbox()
if bbox:
    k_shell = k_shell.crop(bbox)
k_shell = k_shell.resize((16, 16), Image.NEAREST)
k_shell.save(os.path.join(SPRITE_DIR, 'koopa_shell.png'))
print(f'  OK: koopa_shell.png (16x16)')

# ===== 3. Boss =====
print('\n=== 3. Boss Sprites ===')
# Chuboomba (548x122) - SMB1 NES style Bowser
b_idle = bowser_sheet.crop((5, 2, 100, 118)).convert('RGBA')
bbox = b_idle.getbbox()
if bbox:
    b_idle = b_idle.crop(bbox)
b_idle = b_idle.resize((40, 40), Image.NEAREST)
b_idle.save(os.path.join(SPRITE_DIR, 'bowser_idle.png'))
print(f'  OK: bowser_idle.png (40x40)')

b_hurt = bowser_sheet.crop((110, 5, 220, 115)).convert('RGBA')
bbox = b_hurt.getbbox()
if bbox:
    b_hurt = b_hurt.crop(bbox)
b_hurt = b_hurt.resize((40, 40), Image.NEAREST)
b_hurt.save(os.path.join(SPRITE_DIR, 'bowser_hurt.png'))
print(f'  OK: bowser_hurt.png (40x40)')

# ===== 4. 物品 =====
print('\n=== 4. Item Sprites ===')

# 金币 4帧
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
        if dx * dx + dy * dy <= 22:
            mushroom.putpixel((cx, cy), (227, 57, 55, 255))  # red cap
        elif 5 <= cy <= 15 and abs(dx) <= 4:
            mushroom.putpixel((cx, cy), (245, 222, 179, 255))  # skin
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

# 地面瓦片
gt = ground_sheet.crop((4, 4, 36, 36)).convert('RGBA').resize((32, 32), Image.NEAREST)
gt.save(os.path.join(SPRITE_DIR, 'ground_top.png'))
gf = ground_sheet.crop((40, 4, 72, 36)).convert('RGBA').resize((32, 32), Image.NEAREST)
gf.save(os.path.join(SPRITE_DIR, 'ground_fill.png'))
print('  OK: ground_top.png, ground_fill.png (32x32)')

# 问号块
block_q = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
dq = ImageDraw.Draw(block_q)
dq.rectangle([2, 2, 29, 29], fill=(255, 160, 0, 255), outline=(139, 69, 19, 255), width=2)
dq.text((9, 5), '?', fill=(255, 255, 255, 255))
block_q.save(os.path.join(SPRITE_DIR, 'block_question.png'))

# 普通砖块
block_b = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
db = ImageDraw.Draw(block_b)
db.rectangle([0, 0, 31, 31], fill=(180, 80, 40, 255), outline=(120, 50, 20, 255), width=2)
db.line([0, 16, 31, 16], fill=(120, 50, 20, 255), width=1)
db.line([16, 0, 16, 31], fill=(120, 50, 20, 255), width=1)
# 添加砖块纹理点
for dot_x in [4, 12, 20, 28]:
    for dot_y in [4, 12, 20, 28]:
        db.point((dot_x, dot_y), fill=(150, 60, 25, 255))
block_b.save(os.path.join(SPRITE_DIR, 'block_brick.png'))
print('  OK: block_question.png, block_brick.png (32x32)')

# 管道
pt = pipe_sheet.crop((4, 4, 68, 52)).convert('RGBA').resize((64, 32), Image.NEAREST)
pt.save(os.path.join(SPRITE_DIR, 'pipe_top.png'))
pb = pipe_sheet.crop((4, 56, 68, 104)).convert('RGBA').resize((64, 32), Image.NEAREST)
pb.save(os.path.join(SPRITE_DIR, 'pipe_body.png'))
print('  OK: pipe_top.png, pipe_body.png (64x32)')

# 云朵
cloud = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
dc = ImageDraw.Draw(cloud)
dc.ellipse([6, 10, 30, 30], fill=(255, 255, 255, 255))
dc.ellipse([20, 4, 50, 30], fill=(255, 255, 255, 255))
dc.ellipse([38, 12, 58, 30], fill=(255, 255, 255, 255))
cloud.save(os.path.join(SPRITE_DIR, 'cloud.png'))

# 山丘
hill = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
dh = ImageDraw.Draw(hill)
dh.polygon([(0, 52), (20, 16), (40, 32), (52, 8), (64, 52)], fill=(80, 180, 60, 255))
dh.polygon([(64, 52), (40, 32), (64, 64)], fill=(60, 140, 40, 255))
hill.save(os.path.join(SPRITE_DIR, 'hill.png'))
print('  OK: cloud.png, hill.png')

# 单词路障块
wb = Image.new('RGBA', (48, 40), (0, 0, 0, 0))
dwb = ImageDraw.Draw(wb)
dwb.rounded_rectangle([2, 2, 45, 37], radius=4, fill=(139, 69, 19, 255), outline=(90, 40, 10, 255), width=2)
dwb.text((13, 11), 'ABC', fill=(255, 255, 255, 255))
wb.save(os.path.join(SPRITE_DIR, 'word_block.png'))
print('  OK: word_block.png (48x40)')

# ===== 完成 =====
print('\n=== Done! ===')
files = sorted([f for f in os.listdir(SPRITE_DIR) if f.endswith('.png')])
total_size = sum(os.path.getsize(os.path.join(SPRITE_DIR, f)) for f in files)
print(f'Total: {len(files)} sprites, {total_size} bytes')
