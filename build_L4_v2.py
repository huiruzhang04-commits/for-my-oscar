import re

# Emoji chars via chr() to avoid surrogate issues
man = chr(0x1F468)      # 👨 dad
duck = chr(0x1F986)     # 🦆 duck
desk = chr(0x1FA91)     # 🪑 desk
door = chr(0x1F6AA)     # 🚪 door
dog = chr(0x1F415)      # 🐕 dog

# ===== 1. 修改 words.js =====
p_words = r'C:\Users\a4216\.cola\outputs\super-mario-word-game\js\data\words.js'
with open(p_words, 'r', encoding='utf-8') as f:
    content = f.read()

L4_data = """      L4: {
        letter: "Dd",
        words: [
          {
            word: "dad",
            phonetic: "/dad/",
            icon: "{0}",
            sentence: "It is a ___.",
            options: ["爸爸", "鸭子", "桌子", "门"],
            answer: "爸爸"
          },
          {
            word: "duck",
            phonetic: "/dak/",
            icon: "{1}",
            sentence: "It is a ___.",
            options: ["门", "爸爸", "鸭子", "桌子"],
            answer: "鸭子"
          },
          {
            word: "desk",
            phonetic: "/desk/",
            icon: "{2}",
            sentence: "It is a ___.",
            options: ["鸭子", "门", "爸爸", "桌子"],
            answer: "桌子"
          },
          {
            word: "door",
            phonetic: "/do:(r)/",
            icon: "{3}",
            sentence: "It is a ___.",
            options: ["桌子", "狗", "鸭子", "门"],
            answer: "门"
          },
          {
            word: "dog",
            phonetic: "/dog/",
            icon: "{4}",
            sentence: "It is a ___.",
            options: ["门", "桌子", "爸爸", "狗"],
            answer: "狗"
          }
        ]
      }},""".format(man, duck, desk, door, dog)

# 在 L3 的 } 后面、world1 结束前插入 L4
# 找 L3 的最后一个 } 然后加逗号
marker = '          }\n        ]\n      }\n    }\n  }'
replacement = '          }\n        ]\n      },\n' + L4_data + '\n    }\n  }'
if marker in content:
    content = content.replace(marker, replacement, 1)
    with open(p_words, 'w', encoding='utf-8') as f:
        f.write(content)
    print('[OK] words.js L4 added')
else:
    print('[ERR] words.js marker not found, trying alt...')
    # 备用：找 L3 结尾
    marker2 = '          }\n        ]\n      }\n    }\n  }'
    if marker2 in content:
        print('[OK] found via alt marker')
