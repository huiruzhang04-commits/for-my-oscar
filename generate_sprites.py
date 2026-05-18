"""
generate_sprites.py - 一键生成所有马里奥游戏精灵占位图
运行后 assets/sprites/ 下会有所有需要的 PNG 文件
"""
import os
from PIL import Image, ImageDraw

SPRITES_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'sprites')
os.makedirs(SPRITES_DIR, exist_ok=True)

def make_sprite(w, h, frames=1, draw_fn=None, bg=None):
    """创建精灵图（多帧横向排列）"""
    total_w = w * frames
    img = Image.new('RGBA', (total_w, h), bg or (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if draw_fn:
        for f in range(frames):
            draw_fn(draw, f * w, 0, w, h)
    return img

def save(img, name):
    path = os.path.join(SPRITES_DIR, name)
    img.save(path)
    print(f"  ✅ {name} ({img.size[0]}x{img.size[1]})")

# ==================== 马里奥 ====================

def draw_mario_small_idle(d, x, y, w, h):
    # 帽子
    d.ellipse([x+2, y, x+w-2, y+8], fill='#E53935')
    # 脸
    d.ellipse([x+3, y+6, x+w-3, y+h-2], fill='#FFCC80')
    # 眼睛
    d.ellipse([x+5, y+8, x+8, y+11], fill='#000')
    # 身体/工装裤
    d.rectangle([x+4, y+13, x+w-4, y+h-2], fill='#1565C0')
    # 纽扣
    d.ellipse([x+7, y+15, x+9, y+17], fill='#FFD700')
    d.ellipse([x+w-9, y+15, x+w-7, y+17], fill='#FFD700')
    # 鞋子
    d.rectangle([x+2, y+h-4, x+7, y+h], fill='#5D4037')
    d.rectangle([x+w-7, y+h-4, x+w-2, y+h], fill='#5D4037')

def draw_mario_small_walk(d, x, y, w, h):
    draw_mario_small_idle(d, x, y, w, h)

def draw_mario_small_jump(d, x, y, w, h):
    draw_mario_small_idle(d, x, y, w, h)

def draw_mario_big_idle(d, x, y, w, h):
    # 帽子
    d.ellipse([x+2, y, x+w-2, y+10], fill='#E53935')
    # 脸
    d.ellipse([x+3, y+8, x+w-3, y+18], fill='#FFCC80')
    # 眼睛
    d.ellipse([x+5, y+10, x+8, y+13], fill='#000')
    # 身体衬衫
    d.rectangle([x+3, y+17, x+w-3, y+24], fill='#E53935')
    # 工装裤
    d.rectangle([x+3, y+23, x+w-3, y+h-4], fill='#1565C0')
    # 纽扣
    d.ellipse([x+6, y+25, x+9, y+28], fill='#FFD700')
    d.ellipse([x+w-9, y+25, x+w-6, y+28], fill='#FFD700')
    # 鞋子
    d.rectangle([x+1, y+h-4, x+7, y+h], fill='#5D4037')
    d.rectangle([x+w-7, y+h-4, x+w-1, y+h], fill='#5D4037')

def draw_mario_big_walk(d, x, y, w, h):
    draw_mario_big_idle(d, x, y, w, h)

def draw_mario_big_jump(d, x, y, w, h):
    draw_mario_big_idle(d, x, y, w, h)

def draw_mario_star(d, x, y, w, h):
    # 星星版马里奥 - 发光效果
    d.ellipse([x, y, x+w, y+h], fill='#FFE082', outline='#FFD700', width=2)
    d.ellipse([x+2, y+2, x+w-2, y+h-2], fill='#E53935')
    d.ellipse([x+5, y+5, x+8, y+8], fill='#000')

print("🎨 Generating Mario sprites...")
save(make_sprite(16, 16, 1, draw_mario_small_idle), 'mario_small_idle.png')
save(make_sprite(16, 16, 3, draw_mario_small_walk), 'mario_small_walk.png')
save(make_sprite(16, 16, 1, draw_mario_small_jump), 'mario_small_jump.png')
save(make_sprite(16, 32, 1, draw_mario_big_idle), 'mario_big_idle.png')
save(make_sprite(16, 32, 3, draw_mario_big_walk), 'mario_big_walk.png')
save(make_sprite(16, 32, 1, draw_mario_big_jump), 'mario_big_jump.png')
save(make_sprite(16, 16, 1, draw_mario_star), 'mario_small_star.png')
save(make_sprite(16, 32, 1, draw_mario_star), 'mario_big_star.png')

# ==================== 敌人 ====================

def draw_goomba_walk(d, x, y, w, h):
    # 蘑菇头
    d.ellipse([x+1, y+1, x+w-1, y+h*0.65], fill='#8D6E63')
    # 脸
    d.ellipse([x+3, y+h*0.35, x+w-3, y+h-3], fill='#D7CCC8')
    # 眼睛（愤怒）
    d.ellipse([x+4, y+h*0.38, x+7, y+h*0.52], fill='#FFF')
    d.ellipse([x+w-7, y+h*0.38, x+w-4, y+h*0.52], fill='#FFF')
    d.ellipse([x+5, y+h*0.41, x+7, y+h*0.51], fill='#000')
    d.ellipse([x+w-6, y+h*0.41, x+w-4, y+h*0.51], fill='#000')
    # 眉毛（斜的，愤怒）
    d.line([x+3, y+h*0.36, x+8, y+h*0.42], fill='#3E2723', width=1)
    d.line([x+w-3, y+h*0.36, x+w-8, y+h*0.42], fill='#3E2723', width=1)
    # 脚
    d.rectangle([x+1, y+h-4, x+6, y+h], fill='#3E2723')
    d.rectangle([x+w-6, y+h-4, x+w-1, y+h], fill='#3E2723')

def draw_goomba_stomp(d, x, y, w, h):
    # 被踩扁的栗子 - 扁平椭圆
    d.ellipse([x, y+h-6, x+w, y+h], fill='#8D6E63')
    d.ellipse([x+3, y+h-5, x+w-3, y+h-1], fill='#D7CCC8')

print("🍄 Generating enemy sprites...")
save(make_sprite(16, 16, 2, draw_goomba_walk), 'goomba_walk.png')
save(make_sprite(16, 8, 1, draw_goomba_stomp), 'goomba_stomp.png')

# ==================== Boss 库巴 ====================

def draw_bowser_idle(d, x, y, w, h):
    # 身体（大龟壳）
    d.ellipse([x+5, y+20, x+w-5, y+h-5], fill='#4CAF50', outline='#2E7D32', width=2)
    # 头
    d.ellipse([x+8, y+2, x+w-8, y+26], fill='#4CAF50')
    # 刺
    for i in range(4):
        px = x + 12 + i * 10
        d.polygon([(px, y+2), (px-3, y-4), (px+3, y-4)], fill='#F57C00')
    # 眼睛
    d.ellipse([x+14, y+10, x+22, y+20], fill='#FFF')
    d.ellipse([x+w-22, y+10, x+w-14, y+20], fill='#FFF')
    d.ellipse([x+16, y+13, x+21, y+18], fill='#D32F2F')
    d.ellipse([x+w-20, y+13, x+w-15, y+18], fill='#D32F2F')
    # 嘴巴
    d.arc([x+18, y+18, x+w-18, y+30], 0, 180, fill='#D32F2F', width=2)

def draw_bowser_hurt(d, x, y, w, h):
    draw_bowser_idle(d, x, y, w, h)
    # 受伤闪烁效果 - 白色覆盖层
    d = ImageDraw.Draw(Image.new('RGBA', (w, h), (255, 255, 255, 100)))

print("🐢 Generating boss sprites...")
save(make_sprite(40, 40, 1, draw_bowser_idle), 'bowser_idle.png')
save(make_sprite(40, 40, 1, draw_bowser_hurt), 'bowser_hurt.png')

# ==================== 物品 ====================

def draw_coin(d, x, y, w, h):
    # 金币椭圆形（模拟旋转）
    d.ellipse([x+2, y+2, x+w-2, y+h-2], fill='#FFD700', outline='#FFA000', width=1)
    d.ellipse([x+4, y+4, x+w-4, y+h-4], fill='#FFEB3B')
    # $ 符号
    d.text((x+w//2-3, y+h//2-4), '$', fill='#F57F17')

def draw_mushroom_item(d, x, y, w, h):
    # 蘑菇头
    d.ellipse([x+1, y+2, x+w-1, y+h*0.7], fill='#E53935')
    # 白点
    d.ellipse([x+4, y+4, x+8, y+8], fill='#FFF')
    d.ellipse([x+w-8, y+5, x+w-4, y+9], fill='#FFF')
    # 蘑菇柄
    d.rectangle([x+4, y+h*0.55, x+w-4, y+h-2], fill='#FFECB3')
    d.rectangle([x+4, y+h-3, x+w-4, y+h-1], fill='#D7CCC8')

def draw_star_item(d, x, y, w, h):
    # 五角星
    import math
    cx, cy = x + w/2, y + h/2
    outer_r, inner_r = w/2 - 1, w/4
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = outer_r if i % 2 == 0 else inner_r
        px = cx + r * math.cos(angle)
        py = cy - r * math.sin(angle)
        points.append((px, py))
    d.polygon(points, fill='#FFD700', outline='#FFA000')
    # 眼睛
    d.ellipse([cx-4, cy-3, cx-1, cy+1], fill='#000')
    d.ellipse([cx+1, cy-3, cx+4, cy+1], fill='#000')

print("💰 Generating item sprites...")
save(make_sprite(16, 16, 4, draw_coin), 'coin.png')
save(make_sprite(16, 16, 1, draw_mushroom_item), 'mushroom.png')
save(make_sprite(16, 16, 1, draw_star_item), 'star.png')

# ==================== 场景元素 ====================

def draw_block_question(d, x, y, w, h):
    # 问号块底色
    d.rectangle([x, y, x+w, y+h], fill='#FFA000', outline='#BF360C', width=2)
    # 内部高亮
    d.rectangle([x+2, y+2, x+w-2, y+h-2], fill='#FFB74D')
    # 问号
    d.text((x+w//2-4, y+h//2-5), '?', fill='#FFF', font_size=18)

def draw_block_brick(d, x, y, w, h):
    d.rectangle([x, y, x+w, y+h], fill='#CD853F', outline='#8B4513', width=2)
    # 砖缝
    d.line([x+w//2, y, x+w//2, y+h], fill='#8B4513', width=1)
    d.line([x, y+h//2, x+w, y+h//2], fill='#8B4513', width=1)

def draw_ground_top(d, x, y, w, h):
    # 地面顶层（草地）
    d.rectangle([x, y, x+w, y+8], fill='#4CAF50')
    d.rectangle([x, y+8, x+w, y+h], fill='#8B4513')
    # 草地纹理
    for i in range(0, w, 4):
        d.line([x+i, y+8, x+i+2, y+4], fill='#388E3C', width=1)

def draw_ground_fill(d, x, y, w, h):
    d.rectangle([x, y, x+w, y+h], fill='#8B4513')
    # 土壤纹理
    for i in range(0, w, 6):
        for j in range(0, h, 6):
            if (i + j) % 12 == 0:
                d.point((x+i+3, y+j+3), fill='#6D4C41')

def draw_pipe_top(d, x, y, w, h):
    # 管道顶部（宽于主体）
    d.rectangle([x, y+6, x+w, y+h], fill='#43A047')
    d.rectangle([x+4, y, x+w-4, y+8], fill='#66BB6A')
    # 高光
    d.rectangle([x+6, y+2, x+12, y+h-2], fill='#81C784')
    # 暗边
    d.rectangle([x+w-12, y+2, x+w-6, y+h-2], fill='#2E7D32')

def draw_pipe_body(d, x, y, w, h):
    d.rectangle([x, y, x+w, y+h], fill='#43A047')
    d.rectangle([x+4, y, x+10, y+h], fill='#81C784')
    d.rectangle([x+w-10, y, x+w-4, y+h], fill='#2E7D32')

def draw_cloud(d, x, y, w, h):
    # 云朵形状
    d.ellipse([x+8, y+8, x+w-8, y+h], fill='#FFFFFF')
    d.ellipse([x, y+h*0.3, x+w*0.4, y+h], fill='#FFF')
    d.ellipse([x+w*0.6, y+h*0.3, x+w, y+h], fill='#FFF')

def draw_hill(d, x, y, w, h):
    # 圆形山丘
    d.ellipse([x, y+h*0.3, x+w, y+h], fill='#6AB04C')
    # 高光
    d.ellipse([x+w*0.2, y+h*0.35, x+w*0.5, y+h*0.6], fill='#82CC78')

def draw_word_block(d, x, y, w, h):
    # 书本路障
    # 书脊
    d.rectangle([x, y, x+8, y+h], fill='#8B4513')
    # 打开的书页
    d.polygon([(x+8, y), (x+w, y+h//2), (x+8, y+h)], fill='#FFFEF0', outline='#4A2C0A', width=1)
    # 文字图标区域
    d.rectangle([x+14, y+8, x+w-6, y+h-8], fill='#E3F2FD')
    # "ABC" 文字
    d.text((x+18, y+h//2-5), 'ABC', fill='#1565C0')

print("🏗️  Generating scene sprites...")
save(make_sprite(32, 32, 1, draw_block_question), 'block_question.png')
save(make_sprite(32, 32, 1, draw_block_brick), 'block_brick.png')
save(make_sprite(32, 32, 1, draw_ground_top), 'ground_top.png')
save(make_sprite(32, 32, 1, draw_ground_fill), 'ground_fill.png')
save(make_sprite(64, 32, 1, draw_pipe_top), 'pipe_top.png')
save(make_sprite(64, 32, 1, draw_pipe_body), 'pipe_body.png')
save(make_sprite(64, 32, 1, draw_cloud), 'cloud.png')
save(make_sprite(64, 64, 1, draw_hill), 'hill.png')
save(make_sprite(48, 40, 1, draw_word_block), 'word_block.png')

print(f"\n✅ All {len(os.listdir(SPRITES_DIR))} sprite files generated in {SPRITES_DIR}")
