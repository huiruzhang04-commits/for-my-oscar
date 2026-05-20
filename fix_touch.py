#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复手机端触摸按钮 - 用 touchstart 替代 pointerdown"""

# 读取 index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到触摸初始化代码块并替换
old_block = """                // 左按钮：用 pointerdown 替代 touchstart（无300ms延迟，跨设备兼容）
                if (leftBtn) {
                    leftBtn.addEventListener('pointerdown', (e) => {
                        e.preventDefault();
                        input.setKeyDown('ArrowLeft');
                    });
                    leftBtn.addEventListener('touchend', (e) => {
                        e.preventDefault();
                        input.setKeyUp('ArrowLeft');
                    });
                    leftBtn.addEventListener('touchcancel', (e) => {
                        input.setKeyUp('ArrowLeft');
                    });
                }

                // 右按钮
                if (rightBtn) {
                    rightBtn.addEventListener('pointerdown', (e) => {
                        e.preventDefault();
                        input.setKeyDown('ArrowRight');
                    });
                    rightBtn.addEventListener('touchend', (e) => {
                        e.preventDefault();
                        input.setKeyUp('ArrowRight');
                    });
                    rightBtn.addEventListener('touchcancel', (e) => {
                        input.setKeyUp('ArrowRight');
                    });
                }

                // 跳跃按钮
                if (jumpBtn) {
                    jumpBtn.addEventListener('pointerdown', (e) => {
                        e.preventDefault();
                        input.setKeyDown('Space');
                        input.justPressed['Space'] = true;
                    });
                    jumpBtn.addEventListener('touchend', (e) => {
                        e.preventDefault();
                        input.setKeyUp('Space');
                    });
                    jumpBtn.addEventListener('touchcancel', (e) => {
                        input.setKeyUp('Space');
                    });
                }

                // 发射火球按钮
                if (fireBtn) {
                    fireBtn.addEventListener('pointerdown', (e) => {
                        e.preventDefault();
                        input.setKeyDown('KeyF');
                        input.justPressed['KeyF'] = true;
                    });
                    fireBtn.addEventListener('touchend', (e) => {
                        e.preventDefault();
                        input.setKeyUp('KeyF');
                    });
                    fireBtn.addEventListener('touchcancel', (e) => {
                        input.setKeyUp('KeyF');
                    });
                }"""

new_block = """                // 左按钮：touchstart + pointerdown 双兼容（手机端最稳）
                if (leftBtn) {
                    const onLeftStart = (e) => {
                        e.preventDefault();
                        input.setKeyDown('ArrowLeft');
                    };
                    leftBtn.addEventListener('touchstart', onLeftStart, {passive: false});
                    leftBtn.addEventListener('pointerdown', onLeftStart);
                    const onLeftEnd = (e) => {
                        e.preventDefault();
                        input.setKeyUp('ArrowLeft');
                    };
                    leftBtn.addEventListener('touchend', onLeftEnd, {passive: false});
                    leftBtn.addEventListener('touchcancel', onLeftEnd);
                }

                // 右按钮
                if (rightBtn) {
                    const onRightStart = (e) => {
                        e.preventDefault();
                        input.setKeyDown('ArrowRight');
                    };
                    rightBtn.addEventListener('touchstart', onRightStart, {passive: false});
                    rightBtn.addEventListener('pointerdown', onRightStart);
                    const onRightEnd = (e) => {
                        e.preventDefault();
                        input.setKeyUp('ArrowRight');
                    };
                    rightBtn.addEventListener('touchend', onRightEnd, {passive: false});
                    rightBtn.addEventListener('touchcancel', onRightEnd);
                }

                // 跳跃按钮
                if (jumpBtn) {
                    const onJumpStart = (e) => {
                        e.preventDefault();
                        input.setKeyDown('Space');
                        input.justPressed['Space'] = true;
                    };
                    jumpBtn.addEventListener('touchstart', onJumpStart, {passive: false});
                    jumpBtn.addEventListener('pointerdown', onJumpStart);
                    const onJumpEnd = (e) => {
                        e.preventDefault();
                        input.setKeyUp('Space');
                    };
                    jumpBtn.addEventListener('touchend', onJumpEnd, {passive: false});
                    jumpBtn.addEventListener('touchcancel', onJumpEnd);
                }

                // 发射火球按钮
                if (fireBtn) {
                    const onFireStart = (e) => {
                        e.preventDefault();
                        input.setKeyDown('KeyF');
                        input.justPressed['KeyF'] = true;
                    };
                    fireBtn.addEventListener('touchstart', onFireStart, {passive: false});
                    fireBtn.addEventListener('pointerdown', onFireStart);
                    const onFireEnd = (e) => {
                        e.preventDefault();
                        input.setKeyUp('KeyF');
                    };
                    fireBtn.addEventListener('touchend', onFireEnd, {passive: false});
                    fireBtn.addEventListener('touchcancel', onFireEnd);
                }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    print('[OK] touchstart + pointerdown 双绑定已添加')
else:
    print('[WARN] 未找到触摸初始化代码块，请手动检查')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('[OK] index.html 修改完成')
