class LevelManager {
    constructor() {
        this.currentLevel = null;
        this.platforms = [];
        this.enemies = [];
        this.items = [];
        this.boss = null;
    }

    loadLevel(levelId) {
        this.currentLevel = levelId;
        this.platforms = [];
        this.enemies = [];
        this.items = [];

        const levelConfig = this.getLevelConfig(levelId);
        // 只有 hasBoss:true 的关卡才创建 Boss
        this.boss = levelConfig.hasBoss ? new Boss() : null;

        this.buildLevel(levelConfig);

        return {
            playerStart: { x: 50, y: 388 },
            platforms: this.platforms,
            enemies: this.enemies,
            items: this.items,
            boss: this.boss,
            world: this.getWorldForLevel(levelId),
            levelData: this.getLevelData(levelId)
        };
    }

    getLevelConfig(levelId) {
        const configs = {
            'L1': {
                platforms: [
                    // 地面(安全边界) — 高度 640→540，Y 从 520 改为 420
                    { x: 0, y: 420, width: 2800, height: 120, type: 'ground' },

                    // === 开场:安全探索区 ===
                    { x: 200, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    { x: 300, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },

                    // === 第一个单词后 ===
                    { x: 450, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },

                    // === 管道障碍(单个,容易跳)===
                    { x: 650, y: 360, width: 64, height: 60, type: 'pipe' },

                    // === 敌人区砖块 ===
                    { x: 850, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },

                    // === 星星砖块(高处)===
                    { x: 1100, y: 280, width: 64, height: 32, type: 'brick', hasItem: true, item: 'star' },

                    // === 综合挑战区 ===
                    { x: 1400, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    { x: 1550, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },

                    // === 最终管道 ===
                    { x: 1750, y: 360, width: 64, height: 60, type: 'pipe' },

                    // === 通关前奖励 ===
                    { x: 1950, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    { x: 2100, y: 340, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                ],
                enemies: [
                    { x: 720, y: 392, type: 'goomba' },           // 管道后第一个敌人（地面顶部420 - 敌人高28 = 392）
                    { x: 920, y: 392, type: 'goomba' },           // 第二个敌人
                    { x: 1200, y: 392, type: 'goomba' },          // 星星后敌人
                    { x: 1350, y: 392, type: 'goomba' },          // 无敌区敌人
                    { x: 1500, y: 392, type: 'goomba' },          // 综合区敌人1
                    { x: 1650, y: 392, type: 'goomba' },          // 综合区敌人2
                ],
                items: [],
                hasBoss: false,
                triggerPoints: [
                    { x: 350, type: 'word', wordIndex: 0 },   // apple - 开场后
                    { x: 750, type: 'word', wordIndex: 1 },   // cat - 第一个敌人后
                    { x: 1250, type: 'word', wordIndex: 2 },  // bat - 星星后
                    { x: 1650, type: 'word', wordIndex: 3 },  // bag - 综合区后
                    { x: 2300, type: 'end' },                 // 通关
                ]
            },
            'default': {
                // 默认关卡模板（L3-L26 未实现时占位）
                platforms: [
                    { x: 0, y: 420, width: 960, height: 120, type: 'ground' },
                ],
                enemies: [],
                items: [],
                hasBoss: false,
                triggerPoints: []
            }
        };

        // 如果找不到具体配置，用默认模板（防止 L3+ 报错）
        if (configs[levelId]) {
            return configs[levelId];
        }

        // L2 单独配置（草地王国）
        if (levelId === 'L2') {
            return this._getL2Config();
        }

        return configs['default'];
    }

    // L2 配置（草地王国）
    _getL2Config() {
        return {
                platforms: [
                    // 地面（拉宽到5000px）
                    // 地面（拉宽到5000px）— 高度 640→540，Y 从 520 改为 420
                    { x: 0, y: 420, width: 5000, height: 120, type: 'ground' },
                    // 开场砖块区
                    { x: 150, y: 340, width: 96, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                    { x: 350, y: 300, width: 96, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    // 第一个移动平台（13-18秒段）
                    { x: 600, y: 320, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                    // 第一个词（baby）触发点附近
                    { x: 800, y: 260, width: 96, height: 32, type: 'brick', hasItem: true, item: 'star' },
                    // 第二个移动平台（28-33秒段，一高一低）
                    { x: 1400, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.2, moveRange: 100 },
                    { x: 1600, y: 240, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1, moveRange: 80 },
                    // 第二个词（banana）触发点附近
                    { x: 1800, y: 340, width: 96, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                    // 管道障碍段
                    { x: 2200, y: 360, width: 64, height: 60, type: 'pipe' },
                    { x: 2400, y: 320, width: 96, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    // 第三个移动平台（48-53秒段）
                    { x: 2600, y: 300, width: 96, height: 32, type: 'platform', moving: true, moveAxis: 'x', moveSpeed: 1.5, moveRange: 120 },
                    // 第三个词（ball）触发点附近
                    { x: 3000, y: 340, width: 96, height: 32, type: 'brick', hasItem: true, item: 'star' },
                    // Boss准备段 - 蘑菇+星星补给
                    { x: 3500, y: 320, width: 96, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                    { x: 3800, y: 280, width: 96, height: 32, type: 'brick', hasItem: true, item: 'star' },
                    { x: 4200, y: 340, width: 96, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                    // 第四个词（boy）触发点附近
                    { x: 4500, y: 300, width: 96, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                ],
                enemies: [
                    { x: 250, y: 392, type: 'goomba' },
                    { x: 500, y: 392, type: 'goomba' },
                    { x: 900, y: 392, type: 'goomba' },
                    { x: 1100, y: 392, type: 'koopa' },
                    { x: 1500, y: 392, type: 'goomba' },
                    { x: 1900, y: 392, type: 'goomba' },
                    { x: 2300, y: 392, type: 'koopa' },
                    { x: 2700, y: 392, type: 'goomba' },
                    { x: 3100, y: 392, type: 'goomba' },
                    { x: 3500, y: 392, type: 'koopa' },
                    { x: 3900, y: 392, type: 'goomba' },
                    { x: 4300, y: 392, type: 'goomba' },
                ],
                items: [],
                hasBoss: true,
                triggerPoints: [
                    { x: 700, type: 'word', wordIndex: 0 },
                    { x: 1700, type: 'word', wordIndex: 1 },
                    { x: 2900, type: 'word', wordIndex: 2 },
                    { x: 4200, type: 'word', wordIndex: 3 },
                    { x: 4600, type: 'boss' },
                    { x: 4900, type: 'end' },
                ]
        };
    }

    buildLevel(config) {
        config.platforms.forEach(p => {
            if (p.type === 'brick' && !p.moving) {
                this.platforms.push(new Brick(p.x, p.y, p.hasItem, p.item));
            } else {
                const platform = new Platform(p.x, p.y, p.width, p.height, p.type);
                if (p.moving) {
                    platform.moving = true;
                    platform.moveAxis = p.moveAxis || 'x';
                    platform.moveSpeed = p.moveSpeed || 1;
                    platform.moveRange = p.moveRange || 100;
                }
                this.platforms.push(platform);
            }
        });

        config.enemies.forEach(e => {
            if (e.type === 'goomba') {
                this.enemies.push(new Goomba(e.x, e.y));
            } else if (e.type === 'koopa') {
                this.enemies.push(new Koopa(e.x, e.y));
            }
        });

        config.items.forEach(i => {
            if (i.type === 'coin') {
                this.items.push(new Coin(i.x, i.y));
            } else if (i.type === 'mushroom') {
                this.items.push(new Mushroom(i.x, i.y));
            } else if (i.type === 'star') {
                this.items.push(new Star(i.x, i.y));
            }
        });
    }

    getWorldForLevel(levelId) {
        const match = levelId.match(/L(\d+)/);
        if (!match) return 1;
        const levelNum = parseInt(match[1]);

        if (levelNum >= 1 && levelNum <= 5) return 1;
        if (levelNum >= 6 && levelNum <= 10) return 2;
        if (levelNum >= 11 && levelNum <= 16) return 3;
        if (levelNum >= 17 && levelNum <= 21) return 4;
        if (levelNum >= 22 && levelNum <= 26) return 5;
        return 1;
    }

    getLevelData(levelId) {
        const match = levelId.match(/L(\d+)/);
        if (!match) return null;
        const levelNum = parseInt(match[1]);

        if (levelNum >= 1 && levelNum <= 5) {
            return WORDS_DATA.world1.levels[levelId];
        } else if (levelNum >= 6 && levelNum <= 10) {
            return WORDS_DATA.world2.levels[levelId];
        } else if (levelNum >= 11 && levelNum <= 16) {
            return WORDS_DATA.world3.levels[levelId];
        } else if (levelNum >= 17 && levelNum <= 21) {
            return WORDS_DATA.world4.levels[levelId];
        } else if (levelNum >= 22 && levelNum <= 26) {
            return WORDS_DATA.world5.levels[levelId];
        }
        return null;
    }

    getBossQuestions(levelId) {
        return BOSS_QUESTIONS[levelId] || [];
    }

    spawnItem(type, x, y) {
        if (type === 'mushroom') {
            this.items.push(new Mushroom(x, y));
        } else if (type === 'star') {
            this.items.push(new Star(x, y));
        } else if (type === 'coin') {
            this.items.push(new Coin(x, y));
        }
    }

    getNextLevel(currentLevelId) {
        const match = currentLevelId.match(/L(\d+)/);
        if (!match) return null;
        const currentNum = parseInt(match[1]);
        const nextNum = currentNum + 1;

        if (nextNum > 26) return null;

        return `L${nextNum}`;
    }
}

// Boss 战问题配置
const BOSS_QUESTIONS = {
    L1: [
        {
            question: 'I want to eat an ___.',
            options: ['apple', 'baby', 'ball', 'bag'],
            answer: 'apple'
        },
        {
            question: 'It is a ___.',
            options: ['banana', 'bat', 'cat', 'boy'],
            answer: 'banana'
        },
        {
            question: 'The ___ is sleeping on the sofa.',
            options: ['boy', 'bag', 'cat', 'baby'],
            answer: 'cat'
        }
    ],
    L2: [
        {
            question: 'I want to eat an ___.',
            options: ['apple', 'baby', 'ball', 'bag'],
            answer: 'apple'
        },
        {
            question: 'It is a ___.',
            options: ['banana', 'bat', 'cat', 'boy'],
            answer: 'banana'
        },
        {
            question: 'The ___ is sleeping on the sofa.',
            options: ['boy', 'bag', 'cat', 'baby'],
            answer: 'cat'
        }
    ],
    L3: [
        { question: 'L3 boss placeholder', options: ['A', 'B', 'C', 'D'], answer: 'A' }
    ]
};

