import re

man = chr(0x1F468)
duck = chr(0x1F986)
desk_char = chr(0x1FA91)
door = chr(0x1F6AA)
dog = chr(0x1F415)

# ===== 1. words.js =====
p_words = r'C:\Users\a4216\.cola\outputs\super-mario-word-game\js\data\words.js'
with open(p_words, 'r', encoding='utf-8') as f:
    c = f.read()

L4_block = (
    '\n      L4: {\n'
    '        letter: "Dd",\n'
    '        words: [\n'
    '          {\n'
    '            word: "dad",\n'
    '            phonetic: "/dæd/",\n'
    '            icon: "' + man + '",\n'
    '            sentence: "It is a ___.",\n'
    '            options: ["爸爸", "鸭子", "桌子", "门"],\n'
    '            answer: "爸爸"\n'
    '          },\n'
    '          {\n'
    '            word: "duck",\n'
    '            phonetic: "/dʌk/",\n'
    '            icon: "' + duck + '",\n'
    '            sentence: "It is a ___.",\n'
    '            options: ["门", "爸爸", "鸭子", "桌子"],\n'
    '            answer: "鸭子"\n'
    '          },\n'
    '          {\n'
    '            word: "desk",\n'
    '            phonetic: "/desk/",\n'
    '            icon: "' + desk_char + '",\n'
    '            sentence: "It is a ___.",\n'
    '            options: ["鸭子", "门", "爸爸", "桌子"],\n'
    '            answer: "桌子"\n'
    '          },\n'
    '          {\n'
    '            word: "door",\n'
    '            phonetic: "/dɔː/",\n'
    '            icon: "' + door + '",\n'
    '            sentence: "It is a ___.",\n'
    '            options: ["桌子", "狗", "鸭子", "门"],\n'
    '            answer: "门"\n'
    '          },\n'
    '          {\n'
    '            word: "dog",\n'
    '            phonetic: "/dɒɡ/",\n'
    '            icon: "' + dog + '",\n'
    '            sentence: "It is a ___.",\n'
    '            options: ["门", "桌子", "爸爸", "狗"],\n'
    '            answer: "狗"\n'
    '          }\n'
    '        ]\n'
    '      }\n'
)

# 在 L3 的 ]\n      }\n    }\n  } 前插入 L4
marker = '      }\n    }\n  }'
if marker in c:
    # L3 结尾是 } 然后 }}\n  }, 需要找到精确位置
    # 找 L3 的最后一个 } 之前插入
    idx = c.rfind('          }\n        ]\n      }')
    if idx != -1:
        insert_pos = idx + len('          }\n        ]\n      }')
        c = c[:insert_pos] + ',\n' + L4_block + c[insert_pos:]
        with open(p_words, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[OK] words.js L4 added')
    else:
        print('[ERR] L3 end marker not found')
else:
    print('[ERR] words.js marker not found')

# ===== 2. LevelManager.js =====
p_lm = r'C:\Users\a4216\.cola\outputs\super-mario-word-game\js\levels\LevelManager.js'
with open(p_lm, 'r', encoding='utf-8') as f:
    c = f.read()

# 2a. BOSS_QUESTIONS L4
boss_L4 = (
    '\n    L4: [\n'
    '        {\n'
    "            question: 'It is a ___.',\n"
    "            options: ['dad', 'duck', 'apple', 'cat'],\n"
    "            answer: 'dad'\n"
    '        },\n'
    '        {\n'
    "            question: 'The ___ is sleeping on the sofa.',\n"
    "            options: ['dog', 'desk', 'door', 'duck'],\n"
    "            answer: 'cat'\n"
    '        },\n'
    '        {\n'
    "            question: 'It is a ___.',\n"
    "            options: ['door', 'cow', 'car', 'clock'],\n"
    "            answer: 'door'\n"
    '        }\n'
    '    ],\n'
)

marker_boss = '    L3: ['
if marker_boss in c:
    c = c.replace(marker_boss, boss_L4 + '    L3:[', 1)
    print('[OK] BOSS_QUESTIONS L4 added')
else:
    print('[ERR] BOSS_QUESTIONS L3 marker not found')

# 2b. configs L4 (在 getLevelConfig 里)
L4_config = (
    "\n        'L4': {\n"
    '            platforms: [\n'
    '                // ground 7000px\n'
    '                { x: 0, y: 420, width: 7000, height: 120, type: "ground" },\n'
    '                { x: 200, y: 340, width: 64, height: 32, type: "brick", hasItem: true, item: "coin" },\n'
    '                { x: 350, y: 340, width: 64, height: 32, type: "brick", hasItem: true, item: "mushroom" },\n'
    '                { x: 1200, y: 280, width: 96, height: 32, type: "platform", moving: true, moveAxis: "x", moveSpeed: 1, moveRange: 80 },\n'
    '                { x: 1500, y: 360, width: 64, height: 60, type: "pipe" },\n'
    '                { x: 1700, y: 340, width: 64, height: 32, type: "brick", hasItem: true, item: "coin" },\n'
    '                { x: 2400, y: 300, width: 96, height: 32, type: "platform", moving: true, moveAxis: "x", moveSpeed: 1.2, moveRange: 100 },\n'
    '                { x: 2600, y: 240, width: 96, height: 32, type: "platform", moving: true, moveAxis: "x", moveSpeed: 1, moveRange: 80 },\n'
    '                { x: 2800, y: 360, width: 64, height: 60, type: "pipe" },\n'
    '                { x: 3000, y: 340, width: 64, height: 32, type: "brick", hasItem: true, item: "star" },\n'
    '                { x: 3700, y: 340, width: 64, height: 32, type: "brick", hasItem: true, item: "mushroom" },\n'
    '                { x: 3900, y: 300, width: 96, height: 32, type: "platform", moving: true, moveAxis: "x", moveSpeed: 1.5, moveRange: 120 },\n'
    '                { x: 4100, y: 360, width: 64, height: 60, type: "pipe" },\n'
    '                { x: 4300, y: 340, width: 64, height: 32, type: "brick", hasItem: true, item: "coin" },\n'
    '                { x: 5000, y: 300, width: 96, height: 32, type: "platform", moving: true, moveAxis: "x", moveSpeed: 1.2, moveRange: 100 },\n'
    '                { x: 5200, y: 260, width: 96, height: 32, type: "platform", moving: true, moveAxis: "x", moveSpeed: 1, moveRange: 80 },\n'
    '                { x: 5300, y: 340, width: 64, height: 32, type: "brick", hasItem: true, item: "mushroom" },\n'
    '                { x: 5800, y: 340, width: 64, height: 32, type: "brick", hasItem: true, item: "coin" },\n'
    '                { x: 6000, y: 340, width: 64, height: 32, type: "brick", hasItem: true, item: "star" },\n'
    '                { x: 6200, y: 340, width: 64, height: 32, type: "brick", hasItem: true, item: "mushroom" },\n'
    '            ],\n'
    '            enemies: [\n'
    '                { x: 500, y: 392, type: "goomba" },\n'
    '                { x: 1100, y: 392, type: "goomba" },\n'
    '                { x: 1900, y: 392, type: "goomba" },\n'
    '                { x: 3100, y: 392, type: "goomba" },\n'
    '                { x: 3200, y: 392, type: "goomba" },\n'
    '                { x: 3300, y: 392, type: "goomba" },\n'
    '                { x: 3400, y: 392, type: "koopa" },\n'
    '                { x: 4400, y: 392, type: "goomba" },\n'
    '                { x: 4500, y: 392, type: "koopa" },\n'
    '                { x: 5400, y: 392, type: "goomba" },\n'
    '                { x: 5500, y: 392, type: "koopa" },\n'
    '                { x: 6000, y: 392, type: "koopa" },\n'
    '                { x: 6200, y: 392, type: "goomba" },\n'
    '                { x: 6400, y: 392, type: "koopa" },\n'
    '            ],\n'
    '            items: [],\n'
    '            hasBoss: true,\n'
    '            triggerPoints: [\n'
    '                { x: 800, type: "word", wordIndex: 0 },\n'
    '                { x: 2200, type: "word", wordIndex: 1 },\n'
    '                { x: 3700, type: "word", wordIndex: 2 },\n'
    '                { x: 4800, type: "word", wordIndex: 3 },\n'
    '                { x: 5800, type: "word", wordIndex: 4 },\n'
    '                { x: 6500, type: "boss" },\n'
    '                { x: 6900, type: "end" },\n'
    '            ]\n'
    '        },\n'
)

marker_L3 = "        'L3': {"
if marker_L3 in c:
    c = c.replace(marker_L3, L4_config + "        'L3': {", 1)
    print('[OK] L4 config added to getLevelConfig')
else:
    print('[ERR] L3 marker not found in getLevelConfig')

# 写入 LevelManager.js
with open(p_lm, 'w', encoding='utf-8') as f:
    f.write(c)

print('[DONE] All L4 changes applied. Run node --check to verify.')
