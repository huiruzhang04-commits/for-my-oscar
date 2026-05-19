import re

p = r'C:\Users\a4216\.cola\outputs\super-mario-word-game\js\levels\LevelManager.js'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

# L3 配置（纯 ASCII，无中文，避免编码问题）
L3 = """        'L3': {
            platforms: [
                // ground
                { x: 0, y: 420, width: 6000, height: 120, type: 'ground' },
                // intro area
                { x: 200, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 350, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                // after word 1 (cow)
                { x: 900, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 1000, y: 280, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                { x: 1200, y: 240, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.2, moveRange: 100 },
                // before word 2 (car)
                { x: 1500, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'star' },
                // star invincible segment
                { x: 2000, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 2200, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.5, moveRange: 120 },
                // before word 3 (cake)
                { x: 2500, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                { x: 2600, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                { x: 2700, y: 260, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                // pipe exploration
                { x: 3200, y: 360, width: 64, height: 60, type: 'pipe' },
                { x: 3500, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                // before word 4 (clock)
                { x: 3800, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 3900, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.2, moveRange: 100 },
                { x: 4000, y: 260, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                // before word 5 (candy)
                { x: 4500, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                { x: 4600, y: 300, width: 64, height: 32, type: 'brick', hasItem: true, item: 'star' },
                // boss prep
                { x: 5000, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 5200, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
            ],
            enemies: [
                { x: 450, y: 392, type: 'goomba' },
                { x: 1100, y: 392, type: 'goomba' },
                { x: 1300, y: 392, type: 'goomba' },
                { x: 1900, y: 392, type: 'goomba' },
                { x: 2000, y: 392, type: 'goomba' },
                { x: 2100, y: 392, type: 'goomba' },
                { x: 2300, y: 392, type: 'goomba' },
                { x: 2400, y: 392, type: 'koopa' },
                { x: 2800, y: 392, type: 'goomba' },
                { x: 2900, y: 392, type: 'koopa' },
                { x: 3300, y: 392, type: 'goomba' },
                { x: 3800, y: 392, type: 'goomba' },
                { x: 3900, y: 392, type: 'koopa' },
                { x: 4000, y: 392, type: 'goomba' },
                { x: 4200, y: 392, type: 'koopa' },
                { x: 4400, y: 392, type: 'goomba' },
                { x: 4600, y: 392, type: 'koopa' },
            ],
            items: [],
            hasBoss: true,
            triggerPoints: [
                { x: 800, type: 'word', wordIndex: 0 },
                { x: 1800, type: 'word', wordIndex: 1 },
                { x: 2800, type: 'word', wordIndex: 2 },
                { x: 3800, type: 'word', wordIndex: 3 },
                { x: 4800, type: 'word', wordIndex: 4 },
                { x: 5300, type: 'boss' },
                { x: 5800, type: 'end' },
            ]
        },
        'default': {"""

# 在 'default': { 之前插入 L3 配置
marker = "        'default': {"
if marker in content:
    content = content.replace(marker, L3 + marker, 1)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    print('done: L3 config inserted')
else:
    print('error: marker not found')
    # debug
    idx = content.find("default")
    print('context:', content[idx-20:idx+50] if idx != -1 else 'not found')
