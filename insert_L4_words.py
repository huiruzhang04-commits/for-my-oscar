import re

man = chr(0x1F468)
duck = chr(0x1F986)
desk_char = chr(0x1FA91)
door = chr(0x1F6AA)
dog = chr(0x1F415)

p = r'C:\Users\a4216\.cola\outputs\super-mario-word-game\js\data\words.js'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

# 精确标记：L3 结束 } + levels 结束 } + world1 结束 } + WORDS_DATA 结束
marker = '      }\n    }\n  }\n};'
L4_block = (
    '      },\n'
    '      L4: {\n'
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
    '    }\n  }\n};'
)

if marker in c:
    c = c.replace(marker, L4_block, 1)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print('[OK] L4 added to words.js')
    # 验证大小
    print('new size:', len(c))
else:
    print('[ERR] marker not found')
    # debug: 找实际末尾
    print(repr(c[-200:]))
