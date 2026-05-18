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
        this.boss = new Boss();

        const levelConfig = this.getLevelConfig(levelId);
        this.buildLevel(levelConfig);

        return {
            playerStart: { x: 50, y: 488 },
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
                    // 地面（安全边界）
                    { x: 0, y: 520, width: 2800, height: 120, type: 'ground' },
                    
                    // === 开场：安全探索区 ===
                    { x: 200, y: 440, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    { x: 300, y: 440, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                    
                    // === 第一个单词后 ===
                    { x: 450, y: 440, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    
                    // === 管道障碍（单个，容易跳）===
                    { x: 650, y: 460, width: 64, height: 60, type: 'pipe' },
                    
                    // === 敌人区砖块 ===
                    { x: 850, y: 440, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    
                    // === 星星砖块（高处）===
                    { x: 1100, y: 380, width: 64, height: 32, type: 'brick', hasItem: true, item: 'star' },
                    
                    // === 综合挑战区 ===
                    { x: 1400, y: 440, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    { x: 1550, y: 440, width: 64, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                    
                    // === 最终管道 ===
                    { x: 1750, y: 460, width: 64, height: 60, type: 'pipe' },
                    
                    // === 通关前奖励 ===
                    { x: 1950, y: 440, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    { x: 2100, y: 440, width: 64, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                ],
                enemies: [
                    { x: 720, y: 492, type: 'goomba' },           // 管道后第一个敌人
                    { x: 920, y: 492, type: 'goomba' },           // 第二个敌人
                    { x: 1200, y: 492, type: 'goomba' },          // 星星后敌人
                    { x: 1350, y: 492, type: 'goomba' },          // 无敌区敌人
                    { x: 1500, y: 492, type: 'goomba' },          // 综合区敌人1
                    { x: 1650, y: 492, type: 'goomba' },          // 综合区敌人2
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
            'L2': {
                platforms: [
                    { x: 0, y: 520, width: 2000, height: 120, type: 'ground' },
                    { x: 150, y: 440, width: 96, height: 32, type: 'brick', hasItem: true, item: 'mushroom' },
                    { x: 350, y: 400, width: 96, height: 32, type: 'brick', hasItem: true, item: 'coin' },
                    { x: 550, y: 360, width: 96, height: 32, type: 'brick', hasItem: true, item: 'star' },
                    { x: 750, y: 420, width: 64, height: 32, type: 'brick' },
                ],
                enemies: [
                    { x: 250, y: 492, type: 'goomba' },
                    { x: 450, y: 492, type: 'goomba' },
                    { x: 650, y: 492, type: 'goomba' },
                    { x: 800, y: 492, type: 'koopa' },
                ],
                items: [],
                hasBoss: true,
                triggerPoints: [
                    { x: 100, type: 'word', wordIndex: 0 },
                    { x: 280, type: 'word', wordIndex: 1 },
                    { x: 480, type: 'word', wordIndex: 2 },
                    { x: 680, type: 'word', wordIndex: 3 },
                ]
            }
        };

        const match = levelId.match(/L(\d+)/);
        const levelNum = match ? parseInt(match[1]) : 1;

        if (configs[levelId]) {
            return configs[levelId];
        }

        return {
            platforms: [
                { x: 0, y: 520, width: 960, height: 120, type: 'ground' },
            ],
            enemies: [],
            items: [],
            hasBoss: levelNum > 1,
            triggerPoints: []
        };
    }

    buildLevel(config) {
        config.platforms.forEach(p => {
            if (p.type === 'brick') {
                this.platforms.push(new Brick(p.x, p.y, p.hasItem, p.item));
            } else {
                this.platforms.push(new Platform(p.x, p.y, p.width, p.height, p.type));
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
