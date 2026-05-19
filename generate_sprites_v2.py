#!/usr/bin/env python3
"""
生成 SMB 风格精灵图（替换占位 PNG）
使用标准 SMB 配色：红/蓝/棕/绿
"""

from PIL import Image, ImageDraw
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sprites')
os.makedirs(OUT, exist_ok=True)

# ── 色板 ──────────────────────────────────────────────────────
SKIN      = (255, 200, 150)
HAIR      = (130,  70,  30)
RED       = (220,  40,  40)
RED_DARK  = (140,  20,  20)
BLUE      = (40,   80, 220)
BLUE_DARK = (20,   40, 120)
BROWN     = (160, 100,  40)
BROWN_DARK= ( 80,  50,  20)
GREEN     = ( 40, 160,  40)
GREEN_D2  = ( 20,  80,  20)
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
YELLOW    = (255, 220,  40)
ORANGE    = (255, 140,  30)
TAN       = (222, 178, 110)
GOLD      = (255, 200,   0)
MAGENTA   = (200,  50, 200)

def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path)
    print(f'  OK: {name}' )

# ════════════════════════════════════════════════════════════
#  MARIO SMALL  (16×16)
# ════════════════════════════════════════════════════════════
def draw_mario_small(facing='right', frame=0):
    """SMB 小马里奥 16×16"""
    img = Image.new('RGBA', (16, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)

    # 帽子 (y=0~3)
    cx = 1 if facing == 'right' else 0
    d.rectangle([2, 0, 13, 3], fill=RED)
    # M 标志 (白色)
    d.point([8, 1], fill=WHITE)
    d.point([7, 2], fill=WHITE)
    d.point([9, 2], fill=WHITE)

    # 脸 (y=4~7)
    d.rectangle([4, 4, 11, 7], fill=SKIN)
    # 眼睛
    if facing == 'right':
        d.point([9, 5], fill=BLACK)
        d.point([10, 5], fill=BLACK)
    else:
        d.point([5, 5], fill=BLACK)
        d.point([6, 5], fill=BLACK)
    # 胡子
    d.rectangle([6, 7, 9, 7], fill=BROWN_DARK)

    # 身体/上衣 (y=8~10)
    d.rectangle([4, 8, 11, 10], fill=RED)
    # 背带 (蓝色)
    d.rectangle([6, 8, 9, 10], fill=BLUE)

    # 裤子 (y=11~13)
    d.rectangle([4, 11, 11, 13], fill=BLUE)
    # 鞋子 (y=14~15)
    shoe_y = 14 + (frame % 2)  # 走路动画
    d.rectangle([3, shoe_y, 6, 15], fill=BROWN)
    d.rectangle([9, shoe_y, 12, 15], fill=BROWN)

    if facing == 'left':
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

    return img

def draw_mario_small_jump(facing='right'):
    img = Image.new('RGBA', (16, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 帽子
    d.rectangle([2, 0, 13, 3], fill=RED)
    # 脸
    d.rectangle([4, 4, 11, 7], fill=SKIN)
    if facing == 'right':
        d.point([9, 5], fill=BLACK)
        d.point([10, 5], fill=BLACK)
    else:
        d.point([5, 5], fill=BLACK)
        d.point([6, 5], fill=BLACK)
    d.rectangle([6, 7, 9, 7], fill=BROWN_DARK)
    # 身体（跳跃时收缩）
    d.rectangle([4, 8, 11, 9], fill=RED)
    d.rectangle([6, 8, 9, 9], fill=BLUE)
    # 腿收起
    d.rectangle([4, 10, 7, 12], fill=BLUE)
    d.rectangle([8, 10, 11, 12], fill=BLUE)
    # 鞋
    d.rectangle([3, 12, 6, 14], fill=BROWN)
    d.rectangle([9, 12, 12, 14], fill=BROWN)
    if facing == 'left':
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img

print('[Mario Small]')
for f in range(2):
    save(draw_mario_small('right', f), f'mario_small_idle.png' if f==0 else 'mario_small_walk.png')
save(draw_mario_small_jump('right'), 'mario_small_jump.png')

# ════════════════════════════════════════════════════════════
#  MARIO BIG  (16×32)
# ════════════════════════════════════════════════════════════
def draw_mario_big(action='idle', facing='right', frame=0):
    img = Image.new('RGBA', (16, 32), (0,0,0,0))
    d = ImageDraw.Draw(img)

    # ── 帽子 (y=0~4)
    d.rectangle([1, 0, 14, 4], fill=RED)
    d.point([7, 1], fill=WHITE)
    d.point([8, 1], fill=WHITE)

    # ── 脸 (y=5~9)
    d.rectangle([3, 5, 12, 9], fill=SKIN)
    if facing == 'right':
        d.rectangle([9, 6, 11, 7], fill=BLACK)  # 眼睛
    else:
        d.rectangle([4, 6, 6, 7], fill=BLACK)
    d.rectangle([6, 8, 9, 9], fill=BROWN_DARK)  # 胡子

    # ── 上衣 (y=10~17)
    d.rectangle([2, 10, 13, 17], fill=RED)
    # 背带
    d.rectangle([5, 10, 10, 17], fill=BLUE)
    # 扣子
    d.point([6, 12], fill=YELLOW)
    d.point([9, 12], fill=YELLOW)

    # ── 手
    d.rectangle([0, 12, 2, 15], fill=SKIN)
    d.rectangle([13, 12, 15, 15], fill=SKIN)

    # ── 裤子 (y=18~25)
    d.rectangle([3, 18, 12, 25], fill=BLUE)
    # 白色圆点（经典 SMB 背带裤图案）
    for dx in [4, 7, 10]:
        d.point([dx, 20], fill=WHITE)
        d.point([dx, 23], fill=WHITE)

    # ── 鞋 (y=26~31)
    if action == 'walk':
        sy = 26 + (frame % 2)
    else:
        sy = 26
    d.rectangle([2, sy, 6, 31], fill=BROWN)
    d.rectangle([9, sy, 13, 31], fill=BROWN)

    if facing == 'left':
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img

def draw_mario_big_jump(facing='right'):
    img = Image.new('RGBA', (16, 32), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 帽子
    d.rectangle([1, 0, 14, 4], fill=RED)
    # 脸
    d.rectangle([3, 5, 12, 9], fill=SKIN)
    if facing == 'right':
        d.rectangle([9, 6, 11, 7], fill=BLACK)
    else:
        d.rectangle([4, 6, 6, 7], fill=BLACK)
    d.rectangle([6, 8, 9, 9], fill=BROWN_DARK)
    # 身体
    d.rectangle([2, 10, 13, 17], fill=RED)
    d.rectangle([5, 10, 10, 17], fill=BLUE)
    # 腿收起
    d.rectangle([3, 18, 7, 22], fill=BLUE)
    d.rectangle([8, 18, 12, 22], fill=BLUE)
    d.rectangle([2, 22, 6, 25], fill=BROWN)
    d.rectangle([9, 22, 13, 25], fill=BROWN)
    if facing == 'left':
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img

print('[Mario Big]')
save(draw_mario_big('idle', 'right', 0), 'mario_big_idle.png')
save(draw_mario_big('walk', 'right', 0), 'mario_big_walk.png')
save(draw_mario_big_jump('right'), 'mario_big_jump.png')

# ════════════════════════════════════════════════════════════
#  GOOMBA  (16×16)
# ════════════════════════════════════════════════════════════
def draw_goomba(frame=0):
    img = Image.new('RGBA', (16, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 身体（棕色）
    d.rectangle([3, 2, 12, 10], fill=BROWN)
    # 脸（浅棕）
    d.rectangle([4, 3, 11, 8], fill=TAN)
    # 眼睛（黑色，随 frame 变）
    ox = 1 if frame % 2 else 0
    d.rectangle([5+ox, 4, 6+ox, 5], fill=BLACK)
    d.rectangle([9-ox, 4, 10-ox, 5], fill=BLACK)
    # 眉毛（棕色）
    d.rectangle([5, 3, 7, 3], fill=BROWN_DARK)
    d.rectangle([8, 3, 10, 3], fill=BROWN_DARK)
    # 脚
    fy = 14 if frame % 2 else 13
    d.rectangle([3, fy, 7, 15], fill=BROWN_DARK)
    d.rectangle([8, fy, 12, 15], fill=BROWN_DARK)
    # 头顶黑点（Goomba 特征）
    d.point([7, 2], fill=BLACK)
    d.point([8, 2], fill=BLACK)
    return img

def draw_goomba_stomp():
    img = Image.new('RGBA', (16, 8), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([2, 0, 13, 7], fill=BROWN)
    d.ellipse([4, 2, 7, 5], fill=TAN)
    d.ellipse([8, 2, 11, 5], fill=TAN)
    return img

print('[Goomba]')
save(draw_goomba(0), 'goomba_walk.png')
save(draw_goomba_stomp(), 'goomba_stomp.png')

# ════════════════════════════════════════════════════════════
#  KOOPA (绿龟)  (16×24)
# ════════════════════════════════════════════════════════════
def draw_koopa(frame=0, is_shell=False, is_walking=True):
    if is_shell:
        img = Image.new('RGBA', (16, 16), (0,0,0,0))
        d = ImageDraw.Draw(img)
        # 龟壳（绿色带斑点）
        d.ellipse([1, 1, 14, 14], fill=GREEN)
        d.ellipse([3, 3, 12, 12], fill=GREEN_D2)
        # 斑点
        d.point([5, 4], fill=YELLOW)
        d.point([10, 4], fill=YELLOW)
        d.point([5, 10], fill=YELLOW)
        d.point([10, 10], fill=YELLOW)
        return img

    img = Image.new('RGBA', (16, 24), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 龟壳（背部）
    d.ellipse([2, 4, 13, 18], fill=GREEN)
    d.ellipse([4, 6, 11, 16], fill=GREEN_D2)
    # 脸（肤色）
    d.rectangle([5, 6, 10, 10], fill=TAN)
    # 眼睛
    d.point([7, 7], fill=BLACK)
    d.point([8, 7], fill=BLACK)
    # 脚
    fy = 19 if frame % 2 == 0 else 20
    d.rectangle([2, fy, 5, 23], fill=BROWN)
    d.rectangle([10, fy, 13, 23], fill=BROWN)
    return img

print('[Koopa]')
save(draw_koopa(0, is_walking=True), 'koopa_walk.png')
shell = draw_koopa(is_shell=True)
shell.save(os.path.join(OUT, 'koopa_shell.png'))
print('  OK koopa_shell.png')

# ════════════════════════════════════════════════════════════
#  BOWSER (32×32)
# ════════════════════════════════════════════════════════════
def draw_bowser(hurt=False):
    img = Image.new('RGBA', (32, 32), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 身体（橙色/红色）
    body_color = (255, 100, 80) if not hurt else (150, 150, 150)
    d.rectangle([8, 8, 23, 24], fill=body_color)
    # 龟壳（绿色）
    d.ellipse([6, 6, 25, 22], fill=GREEN)
    d.ellipse([8, 8, 23, 20], fill=GREEN_D2)
    # 头
    d.rectangle([10, 2, 21, 10], fill=body_color)
    # 眼睛
    if not hurt:
        d.point([12, 4], fill=YELLOW)
        d.point([18, 4], fill=YELLOW)
        d.point([13, 5], fill=BLACK)
        d.point([19, 5], fill=BLACK)
    else:
        # 受伤：X 眼睛
        d.line([12, 3, 14, 5], fill=BLACK)
        d.line([14, 3, 12, 5], fill=BLACK)
        d.line([17, 3, 19, 5], fill=BLACK)
        d.line([19, 3, 17, 5], fill=BLACK)
    # 角（红色）
    d.polygon([(11,2), (13,0), (15,2)], fill=RED)
    d.polygon([(16,2), (18,0), (20,2)], fill=RED)
    # 脚
    d.rectangle([7, 24, 12, 31], fill=BROWN_DARK)
    d.rectangle([19, 24, 24, 31], fill=BROWN_DARK)
    # 尾巴（经典库巴特征）
    d.polygon([(6,18), (2,14), (4,20)], fill=body_color)
    return img

print('[Bowser]')
save(draw_bowser(False), 'bowser_idle.png')
save(draw_bowser(True), 'bowser_hurt.png')

# ════════════════════════════════════════════════════════════
#  BRICK & QUESTION BLOCK  (16×16)
# ════════════════════════════════════════════════════════════
def draw_brick():
    img = Image.new('RGBA', (16, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=(180, 120, 60))
    # 砖缝
    d.line([(0,7), (15,7)], fill=(120, 80, 40), width=1)
    d.line([(7,0), (7,7)], fill=(120, 80, 40), width=1)
    d.line([(8,8), (8,15)], fill=(120, 80, 40), width=1)
    return img

def draw_question_block(frame=0):
    img = Image.new('RGBA', (16, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 方块底色（黄色，闪烁时变橙）
    bg = YELLOW if frame % 2 == 0 else ORANGE
    d.rectangle([0, 0, 15, 15], fill=bg)
    # 边框
    d.rectangle([0, 0, 15, 15], outline=(180, 120, 0), width=1)
    # ? 号
    d.rectangle([4, 2, 11, 4], fill=BLACK)   # 横
    d.rectangle([4, 2, 6, 10], fill=BLACK)   # 竖
    d.rectangle([4, 8, 11, 10], fill=BLACK)  # 底横
    d.point([9, 12], fill=BLACK)              # 点
    return img

print('[Blocks]')
save(draw_brick(), 'block_brick.png')
save(draw_question_block(0), 'block_question.png')
save(draw_question_block(1), 'block_question_blink.png')

# ════════════════════════════════════════════════════════════
#  ITEMS: MUSHROOM / STAR / COIN  (16×16)
# ════════════════════════════════════════════════════════════
def draw_mushroom():
    img = Image.new('RGBA', (16, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 菌盖（红色带白点）
    d.ellipse([1, 0, 14, 9], fill=RED)
    d.ellipse([3, 1, 5, 3], fill=WHITE)
    d.ellipse([9, 1, 11, 3], fill=WHITE)
    d.ellipse([6, 3, 9, 5], fill=WHITE)
    # 菌柄（米色）
    d.rectangle([4, 8, 11, 15], fill=(255, 230, 180))
    # 眼睛
    d.point([6, 10], fill=BLACK)
    d.point([9, 10], fill=BLACK)
    return img

def draw_star():
    img = Image.new('RGBA', (16, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 五角星（黄色）
    points = [(8,0), (10,5), (15,5), (11,9), (13,14), (8,11), (3,14), (5,9), (1,5), (6,5)]
    d.polygon(points, fill=YELLOW)
    d.polygon(points, outline=ORANGE, width=1)
    # 眼睛
    d.point([6, 6], fill=BLACK)
    d.point([9, 6], fill=BLACK)
    return img

def draw_coin(frame=0):
    img = Image.new('RGBA', (16, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 金币（椭圆，旋转动画用不同宽度）
    w = 10 if frame == 0 else (8 if frame == 1 else 12)
    ox = (16 - w) // 2
    d.ellipse([ox, 2, ox+w, 13], fill=GOLD)
    d.ellipse([ox+2, 4, ox+w-2, 11], fill=(255, 220, 100))
    # $ 符号
    d.rectangle([ox+3, 5, ox+w-3, 6], fill=(180, 120, 0))
    d.rectangle([ox+4, 7, ox+w-4, 9], fill=(180, 120, 0))
    return img

print('[Items]')
save(draw_mushroom(), 'mushroom.png')
save(draw_star(), 'star.png')
for f in range(3):
    save(draw_coin(f), f'coin_{f}.png' if f>0 else 'coin.png')

# ════════════════════════════════════════════════════════════
#  PIPE / GROUND / HILL / CLOUD
# ════════════════════════════════════════════════════════════
def draw_pipe_body(h=32):
    img = Image.new('RGBA', (32, h), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, h-1], fill=(40, 160, 40))
    d.rectangle([0, 0, 31, h-1], outline=(20, 80, 20), width=2)
    # 高光
    d.rectangle([2, 0, 5, h-1], fill=(80, 200, 80))
    return img

def draw_pipe_top():
    img = Image.new('RGBA', (40, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 8, 39, 15], fill=(40, 160, 40))
    d.rectangle([4, 0, 35, 15], fill=(40, 160, 40))
    d.rectangle([4, 0, 35, 7], fill=(80, 200, 80))  # 顶部高光
    d.rectangle([0, 0, 39, 15], outline=(20, 80, 20), width=2)
    return img

def draw_ground_top(w=16):
    img = Image.new('RGBA', (w, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 草地顶部（绿色）
    d.rectangle([0, 0, w-1, 5], fill=GREEN)
    d.rectangle([0, 2, w-1, 5], fill=(80, 200, 80))  # 高光
    # 泥土
    d.rectangle([0, 6, w-1, 15], fill=(180, 120, 60))
    # 泥土纹理
    for x in range(0, w, 4):
        d.line([(x, 8), (x+2, 10)], fill=(140, 90, 40))
    return img

def draw_ground_fill(w=16, h=16):
    img = Image.new('RGBA', (w, h), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w-1, h-1], fill=(180, 120, 60))
    # 纹理
    for y in range(2, h, 4):
        for x in range(0, w, 4):
            d.point([x, y], fill=(140, 90, 40))
    return img

def draw_hill():
    img = Image.new('RGBA', (64, 32), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 山丘主体（绿色三角形）
    d.polygon([(0,31), (32,0), (64,31)], fill=GREEN)
    # 山顶雪白（经典 SMB 山丘）
    d.polygon([(22,10), (32,0), (42,10), (38,10), (32,4), (26,10)], fill=WHITE)
    # 高光
    d.line([(2,30), (62,30)], fill=(80, 200, 80))
    return img

def draw_cloud():
    img = Image.new('RGBA', (48, 24), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 云朵（白色椭圆组合）
    d.ellipse([0, 8, 20, 23], fill=WHITE)
    d.ellipse([10, 0, 30, 18], fill=WHITE)
    d.ellipse([22, 6, 48, 23], fill=WHITE)
    # 阴影（浅灰）
    d.ellipse([14, 14, 26, 20], fill=(230, 230, 230))
    return img

print('[Scenery]')
save(draw_pipe_top(), 'pipe_top.png')
save(draw_pipe_body(32), 'pipe_body.png')
save(draw_ground_top(16), 'ground_top.png')
save(draw_ground_fill(16, 16), 'ground_fill.png')
save(draw_hill(), 'hill.png')
save(draw_cloud(), 'cloud.png')

# ════════════════════════════════════════════════════════════
#  WORD BLOCK (16×16) — 带 ? 的单词块
# ════════════════════════════════════════════════════════════
def draw_word_block():
    img = Image.new('RGBA', (16, 16), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 蓝色底（单词块特征色）
    d.rectangle([0, 0, 15, 15], fill=(80, 120, 220))
    d.rectangle([0, 0, 15, 15], outline=(40, 80, 180), width=1)
    # 书/字母图标
    d.rectangle([4, 2, 11, 13], fill=WHITE)
    d.rectangle([4, 2, 11, 4], fill=BLUE)
    d.line([(7,2), (7,13)], fill=BLUE, width=1)
    return img

print('[Word Block]')
save(draw_word_block(), 'word_block.png')

print('\n✅ 全部精灵图生成完成！')
