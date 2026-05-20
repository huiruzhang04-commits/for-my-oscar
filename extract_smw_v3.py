from PIL import Image
import os, glob

d = r'D:\Users\a4216\Downloads'
files = glob.glob(os.path.join(d, '*Yoshi*'))
img = Image.open(files[0]).convert('RGBA')
w, h = img.size
out_dir = r'C:\Users\a4216\.cola\outputs\super-mario-word-game\assets\sprites\smw'

def extract_by_color(box, keep_fn, name, ts=None):
    """裁剪区域后按颜色函数决定保留/透明"""
    c = img.crop(box).convert('RGBA')
    data = list(c.getdata())
    cleaned = []
    for px in data:
        r, g, b, a = px
        if keep_fn(r, g, b):
            cleaned.append((r, g, b, 255))
        else:
            cleaned.append((r, g, b, 0))
    c.putdata(cleaned)
    bb = c.getbbox()
    if bb:
        c = c.crop(bb)
    if ts and c.size[0] > 0 and c.size[1] > 0:
        c = c.resize(ts, Image.NEAREST)
    path = os.path.join(out_dir, name)
    c.save(path)
    print(f'  {name}: {c.size}')
    return c

print('=== SMW v3 精确颜色提取 ===')

# 管道: 深绿色主体 + 白色高光 + 黑色轮廓
def is_pipe_px(r, g, b):
    # 深绿 (管道身体)
    if 0 <= r <= 40 and 120 <= g <= 200 and 0 <= b <= 60:
        return True
    # 白色高光
    if r >= 220 and g >= 220 and b >= 220:
        return True
    # 黑色轮廓/阴影
    if r <= 30 and g <= 30 and b <= 30:
        return True
    return False

extract_by_color((2920, 336, 3000, 420), is_pipe_px, 'smw_pipe.png', (128, 64))

# 问号块: 黄色 + 棕色边框 + 白色问号 + 黑色轮廓
def is_qblock_px(r, g, b):
    # 黄色主体
    if r >= 220 and g >= 200 and b < 100:
        return True
    # 棕色边框
    if 140 <= r <= 200 and 100 <= g <= 160 and 40 <= b <= 100:
        return True
    # 白色问号/高光
    if r >= 230 and g >= 230 and b >= 200:
        return True
    # 黑色轮廓
    if r <= 35 and g <= 35 and b <= 35:
        return True
    return False

extract_by_color((695, 348, 745, 390), is_qblock_px, 'smw_question_block.png', (32, 32))

# 金币: 亮黄色
def is_coin_px(r, g, b):
    if r >= 240 and g >= 230 and b < 80:
        return True
    # 金币阴影
    if 180 <= r <= 220 and 170 <= g <= 210 and 0 <= b <= 60:
        return True
    return False

extract_by_color((2744, 318, 2760, 334), is_coin_px, 'smw_coin.png', (16, 16))

# 砖块平台: 棕色砖纹
def is_brick_px(r, g, b):
    # 棕色主体
    if 160 <= r <= 220 and 90 <= g <= 160 and 40 <= b <= 110:
        return True
    # 深棕色线条(砖缝)
    if 120 <= r <= 160 and 60 <= g <= 100 and 20 <= b <= 70:
        return True
    # 高光
    if r >= 230 and g >= 200 and b >= 150:
        return True
    # 轮廓
    if r <= 35 and g <= 35 and b <= 35:
        return True
    return False

extract_by_color((2235, 350, 2325, 390), is_brick_px, 'smw_brick.png', (80, 32))

# 地面瓦片: 浅棕色带点状纹理
def is_ground_px(r, g, b):
    # 浅棕
    if 190 <= r <= 235 and 155 <= g <= 200 and 80 <= b <= 130:
        return True
    # 深棕点
    if 160 <= r <= 195 and 120 <= g <= 160 and 50 <= b <= 100:
        return True
    # 深色点
    if 140 <= r <= 170 and 100 <= g <= 140 and 40 <= b <= 85:
        return True
    return False

extract_by_color((100, 396, 500, 432), is_ground_px, 'smw_ground_tile.png')

# 草地顶部: 绿色线
def is_grass_px(r, g, b):
    if g >= 160 and r <= 80 and b <= 80:
        return True
    return False

extract_by_color((100, 382, 500, 404), is_grass_px, 'smw_grass_top.png')

# 灌木丛: 多层绿色圆形
def is_bush_px(r, g, b):
    # 亮绿
    if g >= 180 and r <= 60 and b <= 60:
        return True
    # 中绿
    if g >= 120 and r <= 80 and 0 <= b <= 80:
        return True
    # 深绿(阴影)
    if g >= 60 and r <= 50 and 0 <= b <= 50:
        return True
    return False

extract_by_color((52, 342, 172, 392), is_bush_px, 'smw_bush.png', (120, 50))

# 小山丘: 浅绿色圆弧
def is_hill_s_px(r, g, b):
    if g >= 160 and r <= 100 and b <= 100:
        return True
    if g >= 120 and 80 <= r <= 130 and 50 <= b <= 110:
        return True
    return False

extract_by_color((195, 330, 345, 382), is_hill_s_px, 'smw_hill_small.png', (150, 52))

# 大山丘
def is_hill_l_px(r, g, b):
    if g >= 140 and r <= 120 and b <= 120:
        return True
    if g >= 100 and 80 <= r <= 150 and 50 <= b <= 110:
        return True
    return False

extract_by_color((1795, 305, 2105, 395), is_hill_l_px, 'smw_hill_large.png', (310, 90))

# 台阶
def is_step_px(r, g, b):
    return is_ground_px(r, g, b) or is_brick_px(r, g, b)

extract_by_color((2220, 366, 2260, 402), is_step_px, 'smw_step.png', (32, 36))

print('\nDone!')
