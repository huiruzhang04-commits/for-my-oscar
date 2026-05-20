#!/usr/bin/env python3
"""v3: 精灵图放大版 - 所有精灵放大2x, 匹配960x540画布"""
from PIL import Image, ImageDraw
import math
import os

GAME_DIR = r'C:\Users\a4216\.cola\outputs\super-mario-word-game'
SPRITE_DIR = os.path.join(GAME_DIR, 'assets', 'sprites')
SHEET_DIR = os.path.join(GAME_DIR, '精灵图')
os.makedirs(SPRITE_DIR, exist_ok=True)

def crop_scale(img, box, output_name, target_size):
    """裁剪去背景 + 缩放到目标尺寸"""
    cropped = img.crop(box).convert('RGBA')
    # 去背景(20,20,20)
    data = list(cropped.getdata())
    cleaned = []
    for px in data:
        if abs(px[0]-20)<15 and abs(px[1]-20)<15 and abs(px[2]-20)<15:
            cleaned.append((px[0], px[1], px[2], 0))
        else:
            a = px[3] if len(px) > 3 else 255
            cleaned.append((px[0], px[1], px[2], a))
    cropped.putdata(cleaned)
    bbox = cropped.getbbox()
    if bbox:
        cropped = cropped.crop(bbox)
    result = cropped.resize(target_size, Image.NEAREST)
    out_path = os.path.join(SPRITE_DIR, output_name)
    result.save(out_path)
    print(f'  OK: {output_name} ({target_size[0]}x{target_size[1]})')
    return out_path

print('Loading sheets...')
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

# ===== 放大2倍的目标尺寸 =====
# 马里奥: 16x16 -> 32x32 (小), 16x32 -> 32x64 (大)
# 敌人: 16x16 -> 32x32
# 物品: 16x16 -> 32x32
# Boss: 40x40 -> 80x80
# 场景: 保持或微调

print('\n=== 1. Mario Sprites (2x scale) ===')

crop_scale(ssb64, (14, 14, 40, 28), 'mario_small_idle.png', (32, 32))

# walk 3帧横条 (96x32)
walk_small = Image.new('RGBA', (96, 32), (0,0,0,0))
for i, box in enumerate([(14,14,26,26), (24,14,38,26), (34,14,48,26)]):
    frame = ssb64.crop(box).convert('RGBA')
    data = list(frame.getdata())
    cleaned = [(px[0],px[1],px[2],0) if abs(px[0]-20)<15 and abs(px[1]-20)<15 and abs(px[2]-20)<15 else ((px[0],px[1],px[2],px[3]) if len(px)>3 else (px[0],px[1],px[2],255)) for px in data]
    frame.putdata(cleaned)
    bbox = frame.getbbox()
    if bbox: frame = frame.crop(bbox)
    frame = frame.resize((32, 32), Image.NEAREST)
    walk_small.paste(frame, (i*32, 0), frame)
walk_small.save(os.path.join(SPRITE_DIR, 'mario_small_walk.png'))
print('  OK: mario_small_walk.png (96x32, 3 frames @ 32x32 each)')

crop_scale(ssb64, (36, 42, 54, 56), 'mario_small_jump.png', (32, 32))
crop_scale(ssb64, (37, 105, 68, 137), 'mario_big_idle.png', (32, 64))

# big walk 3帧 (96x64)
walk_big = Image.new('RGBA', (96, 64), (0,0,0,0))
for i, box in enumerate([(36,45,52,68), (92,46,112,67), (142,47,165,67)]):
    frame = ssb64.crop(box).convert('RGBA')
    data = list(frame.getdata())
    cleaned = [(px[0],px[1],px[2],0) if abs(px[0]-20)<15 and abs(px[1]-20)<15 and abs(px[2]-20)<15 else ((px[0],px[1],px[2],px[3]) if len(px)>3 else (px[0],px[1],px[2],255)) for px in data]
    frame.putdata(cleaned)
    bbox = frame.getbbox()
    if bbox: frame = frame.crop(bbox)
    frame = frame.resize((32, 64), Image.NEAREST)
    walk_big.paste(frame, (i*32, 0), frame)
walk_big.save(os.path.join(SPRITE_DIR, 'mario_big_walk.png'))
print('  OK: mario_big_walk.png (96x64, 3 frames @ 32x64 each)')

crop_scale(ssb64, (328, 108, 360, 145), 'mario_big_jump.png', (32, 64))
crop_scale(ssb64, (14, 14, 40, 28), 'mario_small_star.png', (32, 32))
crop_scale(ssb64, (37, 105, 68, 137), 'mario_big_star.png', (32, 64))

print('\n=== 2. Enemies (2x) ===')

g = goomba_sheet.crop((5, 2, 55, 55)).convert('RGBA').resize((32, 32), Image.NEAREST)
g.save(os.path.join(SPRITE_DIR, 'goomba_walk.png'))
print('  OK: goomba_walk.png (32x32)')
gs = goomba_sheet.crop((60, 25, 120, 52)).convert('RGBA')
b = gs.getbbox()
if b: gs = gs.crop(b)
gs = gs.resize((32, 16), Image.NEAREST)
gs.save(os.path.join(SPRITE_DIR, 'goomba_stomp.png'))
print('  OK: goomba_stomp.png (32x16)')

k = koopa_sheet.crop((12, 10, 65, 75)).convert('RGBA')
b = k.getbbox()
if b: k = k.crop(b)
k = k.resize((32, 48), Image.NEAREST)
k.save(os.path.join(SPRITE_DIR, 'koopa_walk.png'))
print('  OK: koopa_walk.png (32x48)')

ks = koopa_sheet.crop((70, 18, 130, 62)).convert('RGBA')
b = ks.getbbox()
if b: ks = ks.crop(b)
ks = ks.resize((32, 32), Image.NEAREST)
ks.save(os.path.join(SPRITE_DIR, 'koopa_shell.png'))
print('  OK: koopa_shell.png (32x32)')

print('\n=== 3. Boss (2x) ===')
bi = bowser_sheet.crop((5, 2, 100, 118)).convert('RGBA')
b = bi.getbbox()
if b: bi = bi.crop(b)
bi = bi.resize((80, 80), Image.NEAREST)
bi.save(os.path.join(SPRITE_DIR, 'bowser_idle.png'))
print('  OK: bowser_idle.png (80x80)')

bh = bowser_sheet.crop((110, 5, 220, 115)).convert('RGBA')
b = bh.getbbox()
if b: bh = bh.crop(b)
bh = bh.resize((80, 80), Image.NEAREST)
bh.save(os.path.join(SPRITE_DIR, 'bowser_hurt.png'))
print('  OK: bowser_hurt.png (80x80)')

print('\n=== 4. Items (2x) ===')

# 金币 4帧 (128x32)
coin_img = Image.new('RGBA', (128, 32), (0,0,0,0))
for i in range(4):
    for cx in range(32):
        for cy in range(32):
            dx, dy = cx-16, cy-16
            if dx*dx+dy*dy <= 144:
                angle = i * math.pi / 2
                brightness = int(abs(math.cos(angle+dx*0.1))*55+200)
                coin_img.putpixel((i*32+cx, cy), (brightness,brightness,0,255))
coin_img.save(os.path.join(SPRITE_DIR, 'coin.png'))
print('  OK: coin.png (128x32, 4 frames @ 32x32 each)')

# 蘑菇
mushroom = Image.new('RGBA', (32, 32), (0,0,0,0))
for cx in range(32):
    for cy in range(32):
        dx, dy = cx-16, cy-18
        if dx*dx+dy*dy <= 90:
            mushroom.putpixel((cx,cy), (227,57,55,255))
        elif 10<=cy<=30 and abs(dx)<=8:
            mushroom.putpixel((cx,cy), (245,222,179,255))
mushroom.save(os.path.join(SPRITE_DIR, 'mushroom.png'))
print('  OK: mushroom.png (32x32)')

# 星星
star = Image.new('RGBA', (32, 32), (0,0,0,0))
pts = [(16,0),(20,10),(32,12),(22,18),(26,30),(16,22),(6,30),(10,18),(0,12),(12,10)]
ImageDraw.Draw(star).polygon(pts, fill=(255,215,0,255))
star.save(os.path.join(SPRITE_DIR, 'star.png'))
print('  OK: star.png (32x32)')

print('\n=== 5. Scene Elements ===')

gt = ground_sheet.crop((4,4,36,36)).convert('RGBA').resize((64,64), Image.NEAREST)
gt.save(os.path.join(SPRITE_DIR, 'ground_top.png'))
gf = ground_sheet.crop((40,4,72,36)).convert('RGBA').resize((64,64), Image.NEAREST)
gf.save(os.path.join(SPRITE_DIR, 'ground_fill.png'))
print('  OK: ground_top/fill (64x64)')

# 问号块 64x64
block_q = Image.new('RGBA', (64, 64), (0,0,0,0))
dq = ImageDraw.Draw(block_q)
dq.rounded_rectangle([4,4,59,59], radius=6, fill=(255,160,0,255), outline=(139,69,19,255), width=3)
dq.text((20,12), '?', fill=(255,255,255,255))
block_q.save(os.path.join(SPRITE_DIR, 'block_question.png'))

# 砖块 64x64
block_b = Image.new('RGBA', (64, 64), (0,0,0,0))
db = ImageDraw.Draw(block_b)
db.rectangle([0,0,63,63], fill=(180,80,40,255), outline=(120,50,20,255), width=3)
db.line([0,32,63,32], fill=(120,50,20,255), width=2)
db.line([32,0,32,63], fill=(120,50,20,255), width=2)
for dot_x in [8,24,40,56]:
    for dot_y in [8,24,40,56]:
        db.point((dot_x,dot_y), fill=(150,60,25,255))
block_b.save(os.path.join(SPRITE_DIR, 'block_brick.png'))
print('  OK: block_question/brick (64x64)')

# 管道 128x64
pt = pipe_sheet.crop((4,4,68,52)).convert('RGBA').resize((128,64), Image.NEAREST)
pt.save(os.path.join(SPRITE_DIR, 'pipe_top.png'))
pb = pipe_sheet.crop((4,56,68,104)).convert('RGBA').resize((128,64), Image.NEAREST)
pb.save(os.path.join(SPRITE_DIR, 'pipe_body.png'))
print('  OK: pipe_top/body (128x64)')

# 云朵 128x64
cloud = Image.new('RGBA', (128, 64), (0,0,0,0))
dc = ImageDraw.Draw(cloud)
dc.ellipse([12,20,60,60], fill=(255,255,255,255))
dc.ellipse([40,8,100,60], fill=(255,255,255,255))
dc.ellipse([76,24,116,60], fill=(255,255,255,255))
cloud.save(os.path.join(SPRITE_DIR, 'cloud.png'))

# 山丘 128x128
hill = Image.new('RGBA', (128, 128), (0,0,0,0))
dh = ImageDraw.Draw(hill)
dh.polygon([(0,104),(40,32),(80,64),(104,16),(128,104)], fill=(80,180,60,255))
dh.polygon([(128,104),(80,64),(128,128)], fill=(60,140,40,255))
hill.save(os.path.join(SPRITE_DIR, 'hill.png'))
print('  OK: cloud(128x64), hill(128x128)')

# 单词路障 96x80
wb = Image.new('RGBA', (96, 80), (0,0,0,0))
dwb = ImageDraw.Draw(wb)
dwb.rounded_rectangle([4,4,91,76], radius=8, fill=(139,69,19,255), outline=(90,40,10,255), width=3)
dwb.text((27,24), 'ABC', fill=(255,255,255,255))
wb.save(os.path.join(SPRITE_DIR, 'word_block.png'))
print('  OK: word_block (96x80)')

print('\n=== Done! ===')
files = sorted([f for f in os.listdir(SPRITE_DIR) if f.endswith('.png')])
total = sum(os.path.getsize(os.path.join(SPRITE_DIR,f)) for f in files)
print(f'Total: {len(files)} sprites, {total} bytes')
