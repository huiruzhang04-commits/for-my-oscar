from PIL import Image
import os, glob

d = r'D:\Users\a4216\Downloads'
files = glob.glob(os.path.join(d, '*Yoshi*'))
img_path = files[0]
img = Image.open(img_path).convert('RGBA')
w, h = img.size
print(f'Image: {w}x{h}')

# 品红透明色
MAGENTA = (248, 0, 248)
pixels = img.load()

# === 1. 提取各区域素材到 assets/sprites/smw/ ===
out_dir = os.path.join(r'C:\Users\a4216\.cola\outputs\super-mario-word-game', 'assets', 'sprites', 'smw')
os.makedirs(out_dir, exist_ok=True)

def extract_and_save(box, name, ts=None):
    """裁剪区域，去品红背景，保存"""
    crop = img.crop(box).convert('RGBA')
    data = list(crop.getdata())
    cleaned = []
    for px in data:
        r, g, b, a = px
        if (r, g, b) == MAGENTA or (r > 240 and g < 20 and b > 240):
            cleaned.append((r, g, b, 0))
        else:
            cleaned.append((r, g, b, 255))
    crop.putdata(cleaned)
    bb = crop.getbbox()
    if bb:
        crop = crop.crop(bb)
    if ts:
        crop = crop.resize(ts, Image.NEAREST)
    path = os.path.join(out_dir, name)
    crop.save(path)
    print(f'  {name}: {crop.size}')
    return crop

print('=== Extracting SMW sprites ===')

# --- 管道: 找绿色管道区域 ---
# 从图中看管道在 x~2900 附近, y~340-400
pipe_crop = extract_and_save((2896, 336, 2976, 416), 'smw_pipe.png', (128, 64))

# --- 地面瓦片: 取一段纯地面 ---
ground_crop = extract_and_save((100, 392, 500, 432), 'smw_ground.png')

# --- 草地顶部: 绿色草地线 ---
grass_crop = extract_and_save((100, 376, 500, 400), 'smw_grass_top.png')

# --- 灌木丛: 圆形绿色灌木 ---
bush_crop = extract_and_save((60, 344, 160, 388), 'smw_bush.png', (96, 44))

# --- 小山丘: 远景浅绿山丘 ---
hill_small_crop = extract_and_save((200, 332, 340, 380), 'smw_hill_small.png', (140, 48))

# --- 大山丘: 中景山丘 ---
hill_large_crop = extract_and_save((1800, 308, 2100, 388), 'smw_hill_large.png', (300, 80))

# --- 问号砖块: 黄色方块 ---
# 在 x~700 附近有问号块
qblock_crop = extract_and_save((704, 352, 736, 384), 'smw_question_block.png', (32, 32))

# --- 棕色砖块平台 ---
brick_crop = extract_and_save((2240, 352, 2320, 384), 'smw_brick_platform.png')

# --- 金币: 黄色椭圆/圆形 ---
coin_crop = extract_and_save((3616, 288, 3632, 312), 'smw_coin.png', (16, 16))

# --- 阶梯台阶: 单个棕色台阶 ---
step_crop = extract_and_save((2224, 368, 2256, 400), 'smw_step.png', (32, 32))

print('\n=== Done extracting ===')

# === 2. 生成纯背景图（去掉所有游戏元素）===
# 只保留: 天空 + 山丘 + 灌木丛
# 去掉: 地面、管道、砖块、金币、阶梯、问号块

bg = img.copy().convert('RGBA')
bg_data = list(bg.getdata())

# 定义要保留的颜色范围（天空/山丘/灌木）
def is_background_element(px):
    r, g, b = px[:3]
    # 品红 = 完全透明
    if (r, g, b) == MAGENTA:
        return True
    # 天空蓝色区域 (如果有的话)
    if r < 50 and g < 50 and b < 50:
        return True  # 黑色边也保留为透明
    # 浅绿色 - 山丘/灌木 (保留)
    if g > 150 and r < 100 and b < 100:
        return True
    # 深绿色 - 灌木丛深色部分 (保留)
    if g > 100 and r < 80 and b < 80:
        return True
    # 棕色 - 地面/土坡/砖块/管道 (去掉!)
    if r > 150 and g > 80 and b < 150 and g < 220:
        return False
    # 黄色 - 金币/问号块 (去掉!)
    if r > 200 and g > 180 and b < 100:
        return False
    # 白色 - 高光/问号 (去掉!)
    if r > 220 and g > 220 and b > 220:
        return False
    # 默认保留
    return True

cleaned_bg = []
for px in bg_data:
    r, g, b, a = px
    if is_background_element(px):
        cleaned_bg.append((r, g, b, 255 if (r,g,b) != MAGENTA else 0))
    else:
        cleaned_bg.append((r, g, b, 0))  # 游戏元素变透明

bg.putdata(cleaned_bg)

bg_path = os.path.join(out_dir, 'smw_background_clean.png')
bg.save(bg_path)
print(f'\nClean background saved: {bg_path} ({bg.size})')

# 预览一下背景效果
preview_path = os.path.join(out_dir, 'smw_bg_preview.png')
# 缩小预览
bg_preview = bg.resize((w // 4, h // 4), Image.NEAREST)
bg_preview.save(preview_path)
print(f'Preview saved: {preview_path} ({bg_preview.size})')
