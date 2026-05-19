#!/usr/bin/env python3
"""Fix: 确保菜单在游戏开始时一定被隐藏 - 双保险策略"""

import re

# 1. 修改 GameEngine.js - 在 startLevel() 开头也隐藏菜单
with open('js/engine/GameEngine.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 在 startLevel(levelId) { 的下一行插入菜单隐藏代码
old_start = '    startLevel(levelId) {\n        this.currentLevel = levelId;'
new_start = '''    startLevel(levelId) {
        // 双保险：确保菜单一定被隐藏
        const menu = document.getElementById('main-menu');
        if (menu) {
            menu.classList.add('hidden');
            menu.style.display = 'none';
            console.log('Main menu force-hidden in startLevel');
        }
        this.currentLevel = levelId;'''

if old_start in content:
    content = content.replace(old_start, new_start)
    print('[OK] startLevel() 已添加双保险隐藏菜单')
else:
    print('[WARN] 未找到 startLevel 特征字符串，手动检查')
    # 尝试找到 startLevel 函数
    idx = content.find('startLevel(levelId)')
    if idx != -1:
        print(f'  找到 startLevel at pos {idx}')
        print(f'  上下文: {repr(content[idx:idx+200])}')

# 同时修改 click 处理器 - 用最激进的方式隐藏
old_click = '''            // 直接操作 DOM，不依赖 this.menuUI（避免手机端 this 指向问题）
            const menu = document.getElementById('main-menu');
            if (menu) {
                menu.classList.add('hidden');
                console.log('Main menu hidden directly');
            } else {
                console.error('main-menu element not found!');
            }'''
new_click = '''            // 最激进方式隐藏菜单（桌面端和移动端双保险）
            const menu = document.getElementById('main-menu');
            if (menu) {
                menu.classList.add('hidden');
                menu.style.display = 'none';
                menu.style.visibility = 'hidden';
                menu.style.pointerEvents = 'none';
                menu.setAttribute('aria-hidden', 'true');
                console.log('Main menu force-hidden (multiple methods)');
            } else {
                console.error('main-menu element not found!');
            }'''

if old_click in content:
    content = content.replace(old_click, new_click)
    print('[OK] click 处理器已升级为激进隐藏方式')
else:
    print('[WARN] 未找到 click 处理器特征字符串')

with open('js/engine/GameEngine.js', 'w', encoding='utf-8') as f:
    f.write(content)

# 2. 修改 CSS - 给 .menu-screen.hidden 加 !important
with open('css/game.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_css = '.menu-screen.hidden {\n    display: none !important;\n}'
new_css = '''.menu-screen.hidden {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}'''

if '.menu-screen.hidden' in css:
    # 找到并替换整个规则
    css = re.sub(r'\.menu-screen\.hidden\s*\{[^}]*\}', new_css, css)
    print('[OK] CSS .menu-screen.hidden 已加 !important')
else:
    # 不存在则追加
    css += '\n' + new_css
    print('[OK] CSS .menu-screen.hidden 已追加')

with open('css/game.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('[OK] 所有修改完成！')
