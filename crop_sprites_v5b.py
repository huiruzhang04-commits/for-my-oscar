#!/usr/bin/env python3
"""v5b: 精确坐标裁剪SSB64 SMB1马里奥 + Chuboomba"""
from PIL import Image
import os

GAME_DIR = r'C:\Users\a4216\.cola\outputs\super-mario-word-game'
SPRITE_DIR = os.path.join(GAME_DIR, 'assets', 'sprites')
SDIR = os.path.join(GAME_DIR, '精灵图')

def find(key):
    for f in os.listdir(SDIR):
        if key in f:
            return Image.open(os.path.join(SDIR, f)).convert('RGBA')
    return None

mario = find('SSB64')
goomba = find('Chuboomba')
print(f'Mario: {mario.size}, Goomba: {goomba.size}')

def crop(img, box, name, ts=None):
    c = img.crop(box).convert('RGBA')
    # 去黑背景
    d = list(c.getdata())
    c.putdata([(r,g,b,0) if r<30 and g<30 and b<30 else (r,g,b,a) for r,g,b,a in d])
    bb = c.getbbox()
    if bb:
        c = c.crop(bb)
    if ts:
        c = c.resize(ts, Image.NEAREST)
    c.save(os.path.join(SPRITE_DIR, name))
    print(f'  {name}: {c.size}')

# ===== 小马里奥 - 第一行 y=48-64, 每帧16x16 =====
# idle (第1帧)
crop(mario, (36, 46, 54, 66), 'mario_small_idle.png', (32, 32))
# walk strip (取3帧拼成宽图: 3*32=96高32)
w1 = mario.crop((54, 46, 72, 66)).convert('RGBA')
w2 = mario.crop((72, 46, 90, 66)).convert('RGBA')
w3 = mario.crop((90, 46, 108, 66)).convert('RGBA')
def clean(img):
    d = list(img.getdata())
    img.putdata([(px[0],px[1],px[2],0) if px[0]<30 and px[1]<30 and px[2]<30 else px for px in d])
for w in [w1,w2,w3]: clean(w)
walk_strip = Image.new('RGBA', (48, 16))
walk_strip.paste(w1, (0,0)); walk_strip.paste(w2, (16,0)); walk_strip.paste(w3, (32,0))
bb = walk_strip.getbbox()
if bb: walk_strip = walk_strip.crop(bb)
walk_strip = walk_strip.resize((96, 32), Image.NEAREST)
walk_strip.save(os.path.join(SPRITE_DIR, 'mario_small_walk.png'))
print(f'  mario_small_walk.png: {walk_strip.size} (3-frame strip)')

# jump
crop(mario, (108, 46, 126, 66), 'mario_small_jump.png', (32, 32))
# star
crop(mario, (126, 46, 144, 66), 'mario_small_star.png', (32, 32))

# ===== 大马里奥 - 第二行 y=80-112, 高度约32px =====
crop(mario, (36, 78, 56, 114), 'mario_big_idle.png', (32, 64))
crop(mario, (56, 78, 76, 114), 'mario_big_walk.png', (96, 64))  # 后面再处理strip
crop(mario, (76, 78, 96, 114), 'mario_big_jump.png', (32, 64))
crop(mario, (96, 78, 116, 114), 'mario_big_star.png', (32, 64))

# 大马里奥walk strip
bw1 = mario.crop((56, 78, 76, 114)).convert('RGBA')
bw2 = mario.crop((76, 78, 96, 114)).convert('RGBA')
bw3 = mario.crop((96, 78, 116, 114)).convert('RGBA')
for w in [bw1,bw2,bw3]: clean(w)
bwalk = Image.new('RGBA', (48, 36))
bwalk.paste(bw1,(0,0)); bwalk.paste(bw2,(16,0)); bwalk.paste(bw3,(32,0))
bb = bwalk.getbbox()
if bb: bwalk = bwalk.crop(bb)
bwalk = bwalk.resize((96, 64), Image.NEAREST)
bwalk.save(os.path.join(SPRITE_DIR, 'mario_big_walk.png'))
print(f'  mario_big_walk.png: {bwalk.size} (3-frame strip)')

# ===== 栗宝宝 =====
crop(goomba, (2, 4, 46, 58), 'goomba_walk.png', (32, 32))
crop(goomba, (168, 4, 220, 44), 'goomba_stomp.png', (32, 32))

print('\nDone!')
