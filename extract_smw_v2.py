from PIL import Image
import os, glob

d = r'D:\Users\a4216\Downloads'
files = glob.glob(os.path.join(d, '*Yoshi*'))
img = Image.open(files[0]).convert('RGBA')
w, h = img.size
MAGENTA = (248, 0, 248)
out_dir = r'C:\Users\a4216\.cola\outputs\super-mario-word-game\assets\sprites\smw'

def clean_crop(box):
    """裁剪+去品红背景"""
    c = img.crop(box).convert('RGBA')
    data = list(c.getdata())
    cleaned = []
    for px in data:
        r, g, b, a = px
        if (r > 240 and g < 20 and b > 240):
            cleaned.append((r, g, b, 0))
        else:
            cleaned.append((r, g, b, 255))
    c.putdata(cleaned)
    bb = c.getbbox()
    return c.crop(bb) if bb else c

def save(crop, name, ts=None):
    if ts:
        crop = crop.resize(ts, Image.NEAREST)
    path = os.path.join(out_dir, name)
    crop.save(path)
    print(f'  OK {name}: {crop.size}')

print('=== 1. 精确提取 SMW 精灵 ===')

# 管道 - 从debug看: x=2936-2984, y=352-416 (纯管道部分)
pipe = clean_crop((2936, 352, 2984, 416))
save(pipe, 'smw_pipe.png', (128, 64))

# 管道顶部(宽口) - x=2928-2992, y=336-360
pipe_top = clean_crop((2928, 336, 2992, 368))
save(pipe_top, 'smw_pipe_top.png', (128, 32))

# 地面瓦片 - 取一段纯地面 x=100-500, y=400-432
ground = clean_crop((100, 400, 500, 432))
save(ground, 'smw_ground_tile.png')

# 草地顶部线 - x=100-500, y=384-404
grass_top = clean_crop((100, 384, 500, 404))
save(grass_top, 'smw_grass_top.png')

# 灌木丛(圆形) - x=56-168, y=344-388
bush = clean_crop((56, 344, 168, 388))
save(bush, 'smw_bush.png', (112, 44))

# 小山丘 - x=200-340, y=332-380
hill_s = clean_crop((200, 332, 340, 380))
save(hill_s, 'smw_hill_small.png', (140, 48))

# 大山丘 - x=1800-2100, y=308-392
hill_l = clean_crop((1800, 308, 2100, 392))
save(hill_l, 'smw_hill_large.png', (300, 84))

# 问号块 - x=704-736, y=352-384
qblock = clean_crop((704, 352, 736, 384))
save(qblock, 'smw_question_block.png', (32, 32))

# 棕色砖块 - x=2240-2320, y=352-384 (阶梯平台)
brick = clean_crop((2240, 352, 2320, 384))
save(brick, 'smw_brick.png', (80, 32))

# 金币 - x=2746-2756, y=320-332 (单个金币)
coin = clean_crop((2746, 320, 2757, 332))
save(coin, 'smw_coin.png', (16, 16))

# 单个台阶 - x=2224-2256, y=368-400
step = clean_crop((2224, 368, 2256, 400))
save(step, 'smw_step.png', (32, 32))

print('\n=== 2. 生成干净背景图 ===')
# 策略: 按颜色分类像素
# 保留: 品红(透明)、绿色系(山丘/灌木)
# 去掉: 棕色系(地面/砖块/管道)、黄色(金币/问号)、白色(高光)

bg = Image.new('RGBA', (w, h), (0, 0, 0, 0))
bg_data = []

for y in range(h):
    for x in range(w):
        r, g, b, a = img.getpixel((x, y))
        
        # 品红 -> 透明
        if r > 240 and g < 20 and b > 240:
            bg_data.append((0, 0, 0, 0))
        # 绿色系 -> 保留 (山丘/灌木丛)
        elif g > 80 and r < 160 and b < 160:
            bg_data.append((r, g, b, 255))
        # 其他所有颜色 -> 透明 (地面/管道/砖块/金币/问号等)
        else:
            bg_data.append((0, 0, 0, 0))

bg.putdata(bg_data)

bg_path = os.path.join(out_dir, 'smw_background_clean.png')
bg.save(bg_path)
print(f'  Background: {bg.size}')

# 缩小预览
preview = bg.resize((w // 4, h // 4), Image.NEAREST)
preview_path = os.path.join(out_dir, 'smw_bg_preview2.png')
preview.save(preview_path)
print(f'  Preview: {preview.size}')
print('\nDone!')
