const fs = require('fs');
const p = 'C:/Users/a4216/.cola/outputs/super-mario-word-game/js/levels/LevelManager.js';
let content = fs.readFileSync(p, 'utf8');

// 精确匹配 getNextLevel() 方法的结束部分
const marker = '        return `L${nextNum}`;\n    }\n}';
const idx = content.indexOf(marker);
console.log('marker index:', idx);

if (idx !== -1) {
    // 插入 _getL3Config() 方法
    const before = content.substring(0, idx + marker.length);
    const after = content.substring(idx + marker.length);
    
    const newMethod = `        return `L${nextNum}`;
    }

    // L3 配置（草地王国 - 字母Cc）
    _getL3Config() {
        return {
            platforms: [
                // 地面（6000px 宽）
                { x: 0, y: 420, width: 6000, height: 120, type: 'ground' },
                // === 开场：回顾区（0-800px）===
                { x: 200, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 350, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                // === 第一个词（cow）后（800-1800px）===
                { x: 900, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 1000, y: 280, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                { x: 1200, y: 240, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.2, moveRange: 100 },
                // === 第二个词（car）前（1800px）===
                { x: 1500, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'star' },
                // === 星星无敌段（1800-2800px）===
                { x: 2000, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 2200, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.5, moveRange: 120 },
                // === 第三个词（cake）前（2800px）===
                { x: 2500, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                { x: 2600, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                { x: 2700, y: 260, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                // === 管道探索（2800-3800px）===
                { x: 3200, y: 360, width: 64, height: 60, type: 'pipe' },
                { x: 3500, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                // === 第四个词（clock）前（3800px）===
                { x: 3800, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 3900, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.2, moveRange: 100 },
                { x: 4000, y: 260, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                // === 第五个词（candy）前（4800px）===
                { x: 4500, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                { x: 4600, y: 300, width: 64, height: 32, type: 'brick', hasItem: true, item: 'star' },
                // === Boss准备段（4800-5300px）===
                { x: 5000, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                { x: 5200, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
            ],
            enemies: [
                // 开场后第一个敌人（回忆踩敌人）
                { x: 450, y: 392, type: 'goomba' },
                // 第一个词后（cow）- 平台下敌人
                { x: 1100, y: 392, type: 'goomba' },
                { x: 1300, y: 392, type: 'goomba' },
                // 星星无敌段 - 三个Goomba排一排
                { x: 1900, y: 392, type: 'goomba' },
                { x: 2000, y: 392, type: 'goomba' },
                { x: 2100, y: 392, type: 'goomba' },
                // 无敌结束后 - 恢复正常难度
                { x: 2300, y: 392, type: 'goomba' },
                { x: 2400, y: 392, type: 'koopa' },
                // 第三个词后（cake）- 移动平台上方敌人
                { x: 2800, y: 392, type: 'goomba' },
                { x: 2900, y: 392, type: 'koopa' },
                // 管道后
                { x: 3300, y: 392, type: 'goomba' },
                // 综合段
                { x: 3800, y: 392, type: 'goomba' },
                { x: 3900, y: 392, type: 'koopa' },
                { x: 4000, y: 392, type: 'goomba' },
                // Boss准备段
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
        };
    }
`;
    
    const newContent = before + newMethod + after;
    fs.writeFileSync(p, newContent, 'utf8');
    console.log('done: _getL3Config() added');
} else {
    console.log('error: marker not found');
}
