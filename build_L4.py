import re

# ===== 1. 修改 words.js =====
p_words = r'C:\Users\a4216\.cola\outputs\super-mario-word-game\js\data\words.js'
with open(p_words, 'r', encoding='utf-8') as f:
    content = f.read()

L4_data = """
      L4: {
        letter: "Dd",
        words: [
          {
            word: "dad",
            phonetic: "/dæd/",
            icon: "\ud83d\udc68",
            sentence: "It is a ___.",
            options: ["爸爸", "鸭子", "桌子", "门"],
            answer: "爸爸"
          },
          {
            word: "duck",
            phonetic: "/dʌk/",
            icon: "\ud83e\udda6",
            sentence: "It is a ___.",
            options: ["门", "爸爸", "鸭子", "桌子"],
            answer: "鸭子"
          },
          {
            word: "desk",
            phonetic: "/desk/",
            icon: "\ud83e\udea1",
            sentence: "It is a ___.",
            options: ["鸭子", "门", "爸爸", "桌子"],
            answer: "桌子"
          },
          {
            word: "door",
            phonetic: "/dɔː/",
            icon: "\ud83d\udeaa",
            sentence: "It is a ___.",
            options: ["桌子", "狗", "鸭子", "门"],
            answer: "门"
          },
          {
            word: "dog",
            phonetic: "/dɒɡ/",
            icon: "\ud83d\udc15",
            sentence: "It is a ___.",
            options: ["门", "桌子", "爸爸", "狗"],
            answer: "狗"
          }
        ]
      }
"""

# 在 L3 后面插入 L4
marker = '      }\n    }\n  }'
if marker in content:
    content = content.replace(marker, '      },\n' + L4_data + '\n    }\n  }', 1)
    with open(p_words, 'w', encoding='utf-8') as f:
        f.write(content)
    print('[OK] words.js L4 added')
else:
    print('[ERR] marker not found in words.js')

# ===== 2. 修改 LevelManager.js =====
p_lm = r'C:\Users\a4216\.cola\outputs\super-mario-word-game\js\levels\LevelManager.js'
with open(p_lm, 'r', encoding='utf-8') as f:
    content = f.read()

# --- 2a. 添加 L4 Boss 题目 ---
boss_L4 = """
    L4: [
        {
            question: 'It is a ___.',
            options: ['dad', 'duck', 'apple', 'cat'],
            answer: 'dad'
        },
        {
            question: 'The ___ is sleeping on the sofa.',
            options: ['dog', 'desk', 'door', 'duck'],
            answer: 'cat'
        },
        {
            question: 'It is a ___.',
            options: ['door', 'cow', 'car', 'clock'],
            answer: 'door'
        }
    ],
"""

marker_boss = "    L3: ["
if marker_boss in content:
    content = content.replace(marker_boss, boss_L4 + "    L3: [", 1)
    print('[OK] BOSS_QUESTIONS L4 added')
else:
    print('[ERR] BOSS_QUESTIONS marker not found')

# --- 2b. 添加 L4 关卡配置到 configs 对象 ---
L4_config = """
        'L4': {
            platforms: [
                // 地面（7000px 宽）
                { x: 0, y: 420, width: 7000, height: 120, type: 'ground' },
                // === 开场回顾区（0-8秒）===
                { x: 200, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 350, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                { x: 500, y: 392, type: 'goomba' },
                // === 第一个词（dad）后（8秒）===
                { x: 900, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                // === 游戏段A：管道探索教学（8-25秒）===
                { x: 1200, y: 280, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                // 第一个发光管道（教学）
                { x: 1500, y: 360, width: 64, height: 60, type: 'pipe', hasHiddenArea: true },
                { x: 1700, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 1900, y: 392, type: 'goomba' },
                // === 第二个词（duck）前（25秒）===
                { x: 2200, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'star' },
                // === 游戏段B：管道探索实战（25-45秒）===
                { x: 2400, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.2, moveRange: 100 },
                { x: 2600, y: 240, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                // 第二个发光管道（实战）
                { x: 2800, y: 360, width: 64, height: 60, type: 'pipe', hasHiddenArea: true },
                // 无敌段
                { x: 3000, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'star' },
                { x: 3100, y: 392, type: 'goomba' },
                { x: 3200, y: 392, type: 'goomba' },
                { x: 3300, y: 392, type: 'goomba' },
                { x: 3400, y: 392, type: 'koopa' },
                // === 第三个词（desk）前（45秒）===
                { x: 3700, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                // === 游戏段C：综合挑战（45-62秒）===
                { x: 3900, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.5, moveRange: 120 },
                // 第三个发光管道（综合）
                { x: 4100, y: 360, width: 64, height: 60, type: 'pipe', hasHiddenArea: true },
                { x: 4300, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 4400, y: 392, type: 'goomba' },
                { x: 4500, y: 392, type: 'koopa' },
                // === 第四个词（door）前（62秒）===
                { x: 4800, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'star' },
                // === 游戏段D：最终综合（62-75秒）===
                { x: 5000, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.2, moveRange: 100 },
                { x: 5200, y: 260, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                { x: 5300, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                { x: 5400, y: 392, type: 'goomba' },
                { x: 5500, y: 392, type: 'koopa' },
                // === 第五个词（dog）前（75秒）===
                { x: 5800, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                // === Boss准备段（75秒+）===
                { x: 6000, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'star' },
                { x: 6200, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
            ],
            enemies: [
                // 开场敌人
                { x: 500, y: 392, type: 'goomba' },
                // 第一个词后
                { x: 1100, y: 392, type: 'goomba' },
                // 管道探索教学段
                { x: 1900, y: 392, type: 'goomba' },
                // 星星无敌段
                { x: 3100, y: 392, type: 'goomba' },
                { x: 3200, y: 392, type: 'goomba' },
                { x: 3300, y: 392, type: 'goomba' },
                { x: 3400, y: 392, type: 'koopa' },
                // 综合挑战段
                { x: 4400, y: 392, type: 'goomba' },
                { x: 4500, y: 392, type: 'koopa' },
                // 最终综合段
                { x: 5400, y: 392, type: 'goomba' },
                { x: 5500, y: 392, type: 'koopa' },
                // Boss准备段
                { x: 6000, y: 392, type: 'koopa' },
                { x: 6200, y: 392, type: 'goomba' },
                { x: 6400, y: 392, type: 'koopa' },
            ],
            items: [],
            hasBoss: true,
            triggerPoints: [
                { x: 800, type: 'word', wordIndex: 0 },
                { x: 2200, type: 'word', wordIndex: 1 },
                { x: 3700, type: 'word', wordIndex: 2 },
                { x: 4800, type: 'word', wordIndex: 3 },
                { x: 5800, type: 'word', wordIndex: 4 },
                { x: 6500, type: 'boss' },
                { x: 6900, type: 'end' },
            ]
        },
"""

marker_L4 = "        'L3': {"
if marker_L4 in content:
    content = content.replace(marker_L4, L4_config + "        'L3': {", 1)
    print('[OK] L4 config added to configs')
else:
    print('[ERR] L4 config marker not found')

# 写入文件
with open(p_lm, 'w', encoding='utf-8') as f:
    f.write(content)

print('[DONE] All L4 changes applied')
