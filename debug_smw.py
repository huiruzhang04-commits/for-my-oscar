from PIL import Image
import os, glob

d = r'D:\Users\a4216\Downloads'
files = glob.glob(os.path.join(d, '*Yoshi*'))
img = Image.open(files[0]).convert('RGBA')
w, h = img.size
out_dir = r'C:\Users\a4216\.cola\outputs\super-mario-word-game\assets\sprites\smw'

# 截取几个关键区域用于人工确认坐标
regions = {
    'zone_pipe': (2880, 330, 3000, 420),       # 管道区域
    'zone_ground1': (80, 380, 600, 432),        # 左侧地面
    'zone_platforms': (2200, 340, 2360, 405),   # 阶梯平台
    'zone_qblock': (690, 345, 750, 395),        # 问号块
    'zone_coins': (2740, 310, 2770, 340),       # 金币列
    'zone_bushes': (40, 340, 180, 400),         # 灌木丛
    'zone_hills': (180, 320, 360, 395),         # 山丘
    'zone_hill2': (1780, 300, 2150, 400),       # 大山丘
}

for name, box in regions.items():
    crop = img.crop(box)
    path = os.path.join(out_dir, f'debug_{name}.png')
    crop.save(path)
    print(f'{name} {box}: {crop.size}')
