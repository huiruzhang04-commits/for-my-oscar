"""
从 SMM2 SMW 编辑器精灵表裁剪关键素材
源图: Nintendo Switch - Super Mario Maker 2 - Super Mario World - Editor Icons (SMW).png
尺寸: 5181x11764
"""
from PIL import Image
import os

# 源图路径（用户提供的精灵表）
SOURCE_PATH = r"D:\Users\a4216\Downloads\Nintendo Switch - Super Mario Maker 2 - Super Mario World - Editor Icons (SMW).png"

# 输出目录
OUTPUT_DIR = "assets/sprites/smw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def crop_and_save(img, box, name, target_size=None):
    """裁剪并保存精灵"""
    cropped = img.crop(box)
    
    # 去除白色背景（可选）
    cropped = cropped.convert("RGBA")
    datas = cropped.getdata()
    newData = []
    for item in datas:
        # 接近白色的像素设为透明
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    cropped.putdata(newData)
    
    if target_size:
        cropped = cropped.resize(target_size, Image.NEAREST)
    
    output_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    cropped.save(output_path)
    print(f"  ✓ {name}: {cropped.size}")
    return output_path

def main():
    print("加载精灵表...")
    img = Image.open(SOURCE_PATH)
    print(f"  尺寸: {img.size}")
    
    # 根据精灵表布局，定义裁剪区域
    # 注意：这张图有多个重复的图块集，我们取第一行
    
    # 假设每个图标是 32x32，每行约 150 个图标
    # 需要用户帮忙确认具体坐标
    
    crops = []
    
    # 管道（绿色，带箭头）- 大约在第一行
    # 根据截图估算：管道图标大约 32x64 或 64x64
    crops.append(("smw_pipe_warp", (0, 0, 64, 96), (128, 64)))  # 估算坐标
    
    # 问号块（黄色）
    crops.append(("smw_question_block", (96, 0, 128, 32), (32, 32)))
    
    # 砖块（棕色）
    crops.append(("smw_brick", (128, 0, 160, 32), (32, 32)))
    
    # 金币
    crops.append(("smw_coin", (160, 0, 192, 32), (32, 32)))
    
    # 栗宝宝（Goomba）
    crops.append(("smw_goomba", (320, 0, 352, 32), (32, 32)))
    
    # 蘑菇
    crops.append(("smw_mushroom", (384, 0, 416, 32), (32, 32)))
    
    # 星星
    crops.append(("smw_star", (416, 0, 448, 32), (32, 32)))
    
    print("\n⚠️ 坐标是估算的，需要验证！")
    print("建议：先用 debug 模式生成标记图确认位置")
    
    # 实际裁剪前，先输出整个第一行供分析
    first_row = img.crop((0, 0, img.width, 64))
    first_row.save(os.path.join(OUTPUT_DIR, "debug_first_row.png"))
    print(f"\n已保存第一行到 {OUTPUT_DIR}/debug_first_row.png")
    print("请查看此图确认图标位置")

if __name__ == "__main__":
    main()
