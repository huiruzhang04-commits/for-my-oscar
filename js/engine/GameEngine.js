const WORLD_COLORS = {
    world1: {
        sky: '#5c94fc',
        skyGradient: ['#87CEEB', '#E0F6FF'],
        grass: '#4CAF50',
        ground: '#8B4513',
        groundLight: '#A0522D'
    }
};

class GameEngine {
    constructor(canvas) {
        this.canvas = canvas;
        this.renderer = new Renderer(canvas);
        this.width = canvas.width;
        this.height = canvas.height;
        
        this.player = null;
        this.platforms = [];
        this.enemies = [];
        this.items = [];
        this.boss = null;
        
        this.gameState = 'menu';
        this.currentLevel = null;
        this.levelData = null;
        this.world = 1;
        this.levelWidth = 2800;  // 默认L1宽度，会在startLevel中动态设置
        this.clouds = [];     // 缓存云朵位置（每关生成一次，不每帧随机）
        this.hills = [];      // 缓存山丘位置（每关生成一次，不每帧随机）
        this.isDying = false; // 防止一帧内多次触发死亡
        
        this.coins = 0;
        this.wordsAnswered = 0;
        this.wordsCorrect = 0;
        this.currentWordIndex = 0;
        this.triggeredPoints = [];
        this.lives = 5;  // 初始5条命（测试模式）
        
        this.levelManager = new LevelManager();
        this.wordCardUI = new WordCardUI();
        this.bossCardUI = new BossCardUI();
        this.levelCompleteUI = new LevelCompleteUI();
        this.gameUI = new GameUI();
        this.menuUI = new MenuUI();

        this.lastTime = 0;
        this.running = false;
        this.animFrame = 0;
        this.animTimer = 0;

        this.setupUIHandlers();
        this.menuUI.onLevelSelect = (levelId) => this.startLevel(levelId);
    }

    setupUIHandlers() {
        // 初始化音效系统（需要用户交互）
        document.getElementById('start-btn').addEventListener('click', () => {
            if (window.soundManager && !window.soundManager.initialized) {
                window.soundManager.init();
            }
        });
        
        const startBtn = document.getElementById('start-btn');
        console.log('Start button:', startBtn);
        startBtn.addEventListener('click', () => {
            console.log('Start button clicked!');
            // 强制从L1开始（清除之前的进度）
            localStorage.removeItem('mario_word_game_progress');
            progressManager.load();
            const currentLevelId = 'L1';
            console.log('Starting level:', currentLevelId);
            this.startLevel(currentLevelId);
        });

        document.getElementById('world-select-btn').addEventListener('click', () => {
            this.menuUI.showWorldSelect();
        });

        document.getElementById('close-world-btn').addEventListener('click', () => {
            this.menuUI.hideWorldSelect();
        });

        document.getElementById('close-level-btn').addEventListener('click', () => {
            this.menuUI.hideLevelSelect();
        });

        document.getElementById('pause-btn').addEventListener('click', () => {
            if (this.gameState === 'playing') {
                this.pause();
            }
        });

        document.getElementById('resume-btn').addEventListener('click', () => {
            this.resume();
        });

        document.getElementById('restart-btn').addEventListener('click', () => {
            this.menuUI.hidePause();
            this.startLevel(this.currentLevel);
        });

        document.getElementById('quit-btn').addEventListener('click', () => {
            this.menuUI.hidePause();
            this.showMenu();
        });

        document.getElementById('settings-btn').addEventListener('click', () => {
            alert('设置功能开发中...');
        });

        document.getElementById('word-library-btn').addEventListener('click', () => {
            alert('单词库功能开发中...');
        });
    }

    startLevel(levelId) {
        this.currentLevel = levelId;
        this.gameState = 'loading';
        
        // 重置镜头，防止从其他关卡切换时镜头位置错误
        this.renderer.setCamera(0, 0);
        
        // 重置生命值为5
        this.lives = 5;  // 测试模式5条命
        this.updateLivesDisplay();
        
        const levelInfo = this.levelManager.loadLevel(levelId);
        const config = this.levelManager.getLevelConfig(levelId);
        
        this.player = new Player(levelInfo.playerStart.x, levelInfo.playerStart.y);
        this.player.onGround = true;
        this.platforms = levelInfo.platforms;
        this.enemies = levelInfo.enemies;
        this.items = levelInfo.items;
        this.boss = levelInfo.boss;
        
        // 动态设置 Boss 位置到 boss trigger 附近
        if (this.boss && config.triggerPoints) {
            const bossTrigger = config.triggerPoints.find(t => t.type === 'boss');
            if (bossTrigger) {
                this.boss.startX = bossTrigger.x - 100;
                this.boss.currentX = this.boss.startX;
                this.boss.x = this.boss.startX;
            }
        }
        this.levelData = levelInfo.levelData;
        this.world = levelInfo.world;

        this.coins = 0;
        this.wordsAnswered = 0;
        this.wordsCorrect = 0;
        this.currentWordIndex = 0;
        this.triggeredPoints = [];
        this.scrollDelay = 180;

        // 动态设置关卡宽度（取地面platform的width）
        const groundPlatform = config.platforms.find(p => p.type === 'ground');
        this.levelWidth = groundPlatform ? groundPlatform.width : 2800;

        // 缓存云朵和山丘位置（只在进入关卡时生成一次，不每帧随机）
        this.clouds = [];
        for (let cx = 100; cx < this.levelWidth; cx += 300 + Math.random() * 100) {
            this.clouds.push({
                x: cx,
                y: 60 + Math.random() * 60,
                scale: 0.7 + Math.random() * 0.6
            });
        }
        this.hills = [];
        for (let hx = 150; hx < this.levelWidth; hx += 200 + Math.random() * 100) {
            this.hills.push({
                x: hx,
                scale: 0.8 + Math.random() * 1.4
            });
        }
        this.isDying = false;
        if (config.triggerPoints) {
            config.triggerPoints.forEach(tp => {
                this.triggeredPoints.push({ ...tp, triggered: false });
            });
        }

        this.gameUI.updateLevel(levelId, this.levelData?.letter || '?');
        this.gameUI.updateWordProgress(0, this.levelData?.words?.length || 0);
        this.gameUI.updateProgress(0);
        this.gameUI.updateCoins(0);
        this.gameUI.resetTimer();

        this.menuUI.hideMainMenu();
        this.menuUI.hideWorldSelect();
        this.menuUI.hideLevelSelect();

        this.gameState = 'playing';
        this.gameUI.startTimer();
        this.running = true;
        this.lastTime = performance.now();
        this.gameLoop();
    }

    gameLoop(currentTime = 0) {
        if (!this.running) return;

        const deltaTime = currentTime - this.lastTime;
        this.lastTime = currentTime;

        if (this.gameState === 'playing') {
            this.update();
            this.render();
        }

        requestAnimationFrame((time) => this.gameLoop(time));
    }

    update() {
        if (this.gameState !== 'playing') return;

        // 更新移动平台
        this.platforms.forEach(p => {
            if (p.moving) p.update();
        });

        this.player.update();

        // 更新玩家行走动画帧
        if (this.player.onGround && Math.abs(this.player.vx) > 0) {
            this.animTimer++;
            const size = this.player.isBig ? 'big' : 'small';
            const walkSprite = `mario_${size}_walk`;
            const config = window.spriteLoader.getConfig(walkSprite);
            const maxFrames = config ? config.frames : 1;
            if (maxFrames > 1 && this.animTimer % 10 === 0) {
                this.animFrame = (this.animFrame + 1) % maxFrames;
            }
        } else {
            this.animFrame = 0;
        }

        // 检测玩家是否掉出屏幕底部
        if (this.player.y > this.height + 100) {
            this.playerDeath();
            return;
        }

        // 如果正在死亡动画/复活过程中，跳过后续逻辑
        if (this.isDying) return;

        const playerBounds = {
            x: this.player.x,
            y: this.player.y,
            width: this.player.width,
            height: this.player.height,
            vy: this.player.vy,
            onGround: this.player.onGround
        };

        const brickHit = Physics.checkPlatformCollision(playerBounds, this.platforms);
        if (brickHit && brickHit.type === 'brick_hit') {
            const brick = brickHit.platform;
            if (brick.hit() && brick.itemGiven) {
                if (brick.hasItem) {
                    this.levelManager.spawnItem('mushroom', brick.x, brick.y);
                }
            }
        }

        Physics.checkBoundary(playerBounds, this.levelWidth, this.height);  // 使用动态关卡宽度
        this.player.x = playerBounds.x;
        this.player.y = playerBounds.y;
        if (playerBounds.onGround) {
            this.player.onGround = true;
        }

        for (let i = this.items.length - 1; i >= 0; i--) {
            const item = this.items[i];
            item.update();

            if (!item.active) {
                this.items.splice(i, 1);
                continue;
            }

            const itemBounds = item.getBounds();
            if (Physics.checkCollision(playerBounds, itemBounds)) {
                if (item instanceof Coin) {
                    item.collect();
                    this.coins += 10;
                    this.gameUI.updateCoins(this.coins);
                    if (window.soundManager) window.soundManager.playCoin();
                } else if (item instanceof Mushroom) {
                    item.collect();
                    this.player.grow();
                    this.coins += 100;
                    this.gameUI.updateCoins(this.coins);
                    if (window.soundManager) window.soundManager.playPowerUp();
                } else if (item instanceof Star) {
                    item.collect();
                    this.player.activateStar();
                    this.coins += 50;
                    this.gameUI.updateCoins(this.coins);
                    if (window.soundManager) window.soundManager.playStar();
                }
            }
        }

        for (let i = this.enemies.length - 1; i >= 0; i--) {
            const enemy = this.enemies[i];
            enemy.update();

            if (!enemy.active) {
                this.enemies.splice(i, 1);
                continue;
            }

            const enemyBounds = enemy.getBounds();
            if (Physics.checkCollision(playerBounds, enemyBounds)) {
                const playerBottom = this.player.y + this.player.height;
                const enemyTop = enemy.y;
                
                if (this.player.vy > 0 && playerBottom < enemyTop + enemy.height / 2) {
                    enemy.stomp();
                    this.player.vy = -10;
                    this.coins += 100;
                    this.gameUI.updateCoins(this.coins);
                    if (window.soundManager) window.soundManager.playStomp();
                } else if (this.player.isStar) {
                    enemy.stomp();
                    this.coins += 200;
                    this.gameUI.updateCoins(this.coins);
                    if (window.soundManager) window.soundManager.playStomp();
                } else if (!this.player.invincible) {
                    // 玩家受伤或死亡
                    if (this.player.isBig) {
                        // 如果是大马里奥，变小
                        this.player.shrink();
                        if (window.soundManager) window.soundManager.playWrong();
                    } else {
                        // 如果是小马里奥，减少生命值
                        if (window.soundManager) window.soundManager.playDeath();
                        this.playerDeath();
                    }
                }
            }

            for (const platform of this.platforms) {
                const platBounds = platform.getBounds();
                if (platBounds.type === 'brick') continue;
                
                if (Physics.checkCollision(enemyBounds, platBounds)) {
                    if (enemy instanceof Goomba) {
                        enemy.reverse();
                    } else if (enemy instanceof Koopa && !enemy.isShell) {
                        enemy.reverse();
                    }
                }
            }
        }

        this.checkTriggers();

        if (this.boss) this.boss.update();
    }

    checkTriggers() {
        for (const trigger of this.triggeredPoints) {
            if (trigger.triggered) continue;

            if (this.player.x >= trigger.x) {
                trigger.triggered = true;

                if (trigger.type === 'word') {
                    this.showWordCard(trigger.wordIndex);
                } else if (trigger.type === 'boss') {
                    this.startBossFight();
                } else if (trigger.type === 'end') {
                    this.completeLevel();
                }
            }
        }
    }

    showWordCard(wordIndex) {
        if (!this.levelData || !this.levelData.words) return;
        if (wordIndex >= this.levelData.words.length) return;

        this.gameState = 'wordcard';
        this.gameUI.stopTimer();

        const word = this.levelData.words[wordIndex];
        this.currentWordIndex = wordIndex;

        this.wordCardUI.show(word, (correct) => {
            this.wordsAnswered++;
            if (correct) {
                this.wordsCorrect++;
                this.coins += 50;
                this.gameUI.updateCoins(this.coins);
                this.spawnCoinRain(this.player.x, this.player.y);
                if (this.gameUI.floatingText) {
                    this.gameUI.floatingText("答对了！+50金币", this.player.x, this.player.y - 40);
                }
                if (window.soundManager) window.soundManager.playCorrect();
            } else {
                if (window.soundManager) window.soundManager.playWrong();
            }

            this.gameUI.updateWordProgress(this.wordsAnswered, this.levelData.words.length);
            const progress = (this.wordsAnswered / this.levelData.words.length) * 100;
            this.gameUI.updateProgress(progress);

            this.gameState = 'playing';
            this.gameUI.startTimer();
        });
    }

    startBossFight() {
        this.gameState = 'boss';
        this.gameUI.stopTimer();

        const questions = this.levelManager.getBossQuestions(this.currentLevel);
        if (questions.length === 0) {
            this.completeLevel();
            return;
        }

        this.boss.activate();
        this.bossCorrectCount = 0; // 记录答对几题

        this.bossCardUI.show(questions, (correct) => {
            if (correct) {
                this.wordsCorrect++;
                this.coins += 100;
                this.gameUI.updateCoins(this.coins);
                this.bossCorrectCount++;
                
                // Boss 后退 + 金币雨
                this.boss.hit();
                this.spawnCoinRain(this.boss.currentX, this.boss.y);
                if (this.gameUI.floatingText) {
                    this.gameUI.floatingText(`答对！+100金币 (${this.bossCorrectCount}/3)`, this.boss.currentX, this.boss.y - 40);
                }
                
                if (window.soundManager) window.soundManager.playCorrect();
                
                // 更新 Boss HP 条
                this.bossCardUI.updateHp(this.boss.hp);
            } else {
                // Boss 前进（不惩罚）
                this.boss.miss();
                if (window.soundManager) window.soundManager.playWrong();
            }
        }, (defeated) => {
            if (defeated) {
                this.coins += 500;
                this.gameUI.updateCoins(this.coins);
                
                // Boss 飞走动画 + 大金币雨
                this.spawnCoinRain(this.boss.currentX, this.boss.y, 30);
                
                if (window.soundManager) window.soundManager.playLevelComplete();
                
                // 延迟显示通关界面
                setTimeout(() => {
                    this.completeLevel();
                }, 1500);
            }
        });
    }

    completeLevel() {
        // 播放通关音效
        if (window.soundManager) window.soundManager.playLevelComplete();
        
        this.gameState = 'complete';
        this.running = false;
        this.gameUI.stopTimer();

        const world = this.levelManager.getWorldForLevel(this.currentLevel);
        const levelData = this.levelManager.getLevelData(this.currentLevel);

        progressManager.completeLevel(
            this.currentLevel,
            this.coins,
            levelData?.words?.map(w => w.word) || []
        );

        if (this.levelManager.getNextLevel(this.currentLevel)) {
            const nextWorld = this.levelManager.getWorldForLevel(
                this.levelManager.getNextLevel(this.currentLevel)
            );
            if (nextWorld > world) {
                progressManager.unlockWorld(nextWorld);
            }
            progressManager.setCurrentLevel(
                nextWorld,
                parseInt(this.currentLevel.match(/L(\d+)/)[1]) + 1
            );
        }

        // 根据是否有 Boss 决定通关消息
        const config = this.levelManager.getLevelConfig(this.currentLevel);
        let levelName;
        if (config.hasBoss) {
            levelName = `库巴被打败了！${this.currentLevel.replace('L', '第')}关通过`;
        } else {
            levelName = `${this.currentLevel.replace('L', '第')}关通过`;
        }

        this.levelCompleteUI.show({
            levelId: this.currentLevel,
            levelName,
            letter: levelData?.letter || '?',
            correct: this.wordsCorrect,
            total: this.wordsAnswered || levelData?.words?.length || 0,
            coins: this.coins
        }, () => {
            const nextLevel = this.levelManager.getNextLevel(this.currentLevel);
            if (nextLevel) {
                this.startLevel(nextLevel);
            } else {
                this.showMenu();
            }
        });
    }

    spawnCoinRain(x, y, count = 5) {
        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                this.items.push(new Coin(x + (Math.random() - 0.5) * 100, y - Math.random() * 80));
            }, i * 80);
        }
    }

    pause() {
        this.gameState = 'paused';
        this.menuUI.showPause();
    }

    resume() {
        this.menuUI.hidePause();
        this.gameState = 'playing';
    }

    showMenu() {
        this.gameState = 'menu';
        this.running = false;
        this.gameUI.stopTimer();
        this.menuUI.showMainMenu();
        this.renderMenuBackground();
    }

    updateLivesDisplay() {
        // 更新数字显示
        const livesCount = document.getElementById('lives-count');
        if (livesCount) {
            livesCount.textContent = this.lives;
        }
        
        // 更新爱心显示
        const livesHearts = document.getElementById('lives-hearts');
        if (livesHearts) {
            const hearts = livesHearts.querySelectorAll('.heart');
            hearts.forEach((heart, index) => {
                if (index < this.lives) {
                    heart.classList.remove('lost');
                } else {
                    heart.classList.add('lost');
                }
            });
        }
    }

    playerDeath() {
        if (this.isDying) return;
        this.isDying = true;

        this.lives--;
        console.log('[DEATH] lives now:', this.lives);
        this.updateLivesDisplay();
        
        if (this.lives <= 0) {
            this.gameOver();
            this.isDying = false;
        } else {
            // 0.5秒后原地复活（小马里奥死亡：直接消失后立即复活）
            setTimeout(() => {
                this.respawnPlayer();
                this.isDying = false;
            }, 500);
        }
    }

    respawnPlayer() {
        // 原地复活：回到死亡位置附近，不回起点
        this.player.x = Math.max(50, this.player.x - 50);  // 向左50px，但不小于50
        
        // 如果玩家掉出屏幕，拉回屏幕内安全高度
        const safeY = this.height - 100;
        if (this.player.y > safeY) {
            this.player.y = safeY;
        }
        
        this.player.vx = 0;
        this.player.vy = 0;
        this.player.isBig = false;
        this.player.invincible = true;
        this.player.isStar = false;
        this.player.width = 32;
        this.player.height = 32;
        this.player.onGround = true;
        
        this.scrollDelay = 180;
        
        // 2秒无敌时间
        setTimeout(() => {
            if (this.player) this.player.invincible = false;
        }, 2000);
    }

    gameOver() {
        this.gameState = 'gameOver';
        this.running = false;
        this.gameUI.stopTimer();
        
        // 显示游戏结束画面
        setTimeout(() => {
            alert('游戏结束！生命值耗尽！');
            this.showMenu();
        }, 500);
    }

    render() {
        const colors = WORLD_COLORS[`world${this.world}`] || WORLD_COLORS.world1;

        this.renderer.clear(colors.sky);
        this.renderer.drawBackground(colors);

        if (this.player) {
            const autoScrollSpeed = 1.5;  // 加快自动滚动，让玩家更快到达后半段
            const targetX = this.player.x - this.renderer.width / 3;
            const levelMaxX = Math.max(0, this.levelWidth - this.renderer.width);  // 动态计算
            
            const currentCamera = this.renderer.cameraX;
            let autoScrollX = currentCamera;
            
            if (this.scrollDelay > 0) {
                this.scrollDelay--;
            } else {
                autoScrollX = currentCamera + autoScrollSpeed;
            }
            
            const playerBasedX = Math.max(0, Math.min(targetX, levelMaxX));
            
            const newCameraX = Math.max(autoScrollX, playerBasedX);
            this.renderer.setCamera(Math.min(newCameraX, levelMaxX), 0);
        }

        this.renderer.applyCamera();
        
        // 使用缓存的云朵位置（不每帧随机）
        for (const cloud of this.clouds) {
            this.renderer.drawCloud(cloud.x, cloud.y, cloud.scale);
        }

        // 先画地面，再画山丘（山丘在地面后面）
        for (const platform of this.platforms) {
            if (platform.type === 'ground') {
                this.renderer.drawGround(colors, platform.y, platform.width);
            }
        }

        // 使用缓存的山丘位置（不每帧随机）
        for (const hill of this.hills) {
            this.renderer.drawHill(hill.x, 520, hill.scale);
        }

        for (const platform of this.platforms) {
            if (platform.type === 'brick') {
                const { x, y, width, height, hasItem, itemGiven } = platform;
                this.renderer.ctx.fillStyle = '#FFA000';
                this.renderer.ctx.fillRect(x, y, width, height);
                this.renderer.ctx.strokeStyle = '#BF360C';
                this.renderer.ctx.lineWidth = 2;
                this.renderer.ctx.strokeRect(x, y, width, height);
                
                if (hasItem && !itemGiven) {
                    this.renderer.ctx.fillStyle = '#fff';
                    this.renderer.ctx.font = 'bold 20px Arial';
                    this.renderer.ctx.fillText('?', x + width/2 - 5, y + height/2 + 7);
                }
            } else if (platform.type === 'pipe') {
                this.renderer.ctx.fillStyle = '#4CAF50';
                this.renderer.ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
            } else if (platform.type === 'platform') {
                // 移动/静止平台
                const { x, y, width, height, moving } = platform;
                this.renderer.ctx.fillStyle = moving ? '#5DADE2' : '#8B4513';
                this.renderer.ctx.fillRect(x, y, width, height);
                this.renderer.ctx.strokeStyle = moving ? '#2E86C1' : '#A0522D';
                this.renderer.ctx.lineWidth = 2;
                this.renderer.ctx.strokeRect(x, y, width, height);
                if (moving) {
                    // 移动平台标记：两侧画箭头
                    this.renderer.ctx.fillStyle = '#fff';
                    this.renderer.ctx.font = 'bold 14px Arial';
                    this.renderer.ctx.fillText('↔', x + 4, y + height - 4);
                    this.renderer.ctx.fillText('↔', x + width - 20, y + height - 4);
                }
            }
        }

        for (const item of this.items) {
            if (item instanceof Coin) {
                this.renderer.drawCoin(item);
            } else if (item instanceof Mushroom) {
                this.renderer.drawMushroom(item);
            } else if (item instanceof Star) {
                this.renderer.drawStar(item);
            }
        }

        for (const trigger of this.triggeredPoints) {
            if (!trigger.triggered && trigger.type === 'word') {
                this.renderer.drawWordTrigger(trigger.x);
            }
        }

        for (const enemy of this.enemies) {
            if (enemy instanceof Goomba) {
                this.renderer.drawGoomba(enemy);
            } else if (enemy instanceof Koopa) {
                this.renderer.drawKoopa(enemy);
            }
        }

        if (this.player) {
            this.renderer.drawPlayer(this.player, this.animFrame);
        }

        this.renderer.removeCamera();

        if (this.boss) {
            const pos = this.boss.getPosition();
            this.boss.x = pos.x;
            this.boss.y = pos.y;
            this.renderer.drawBoss(this.boss);
        }
    }

    renderMenuBackground() {
        const colors = WORLD_COLORS.world1;
        this.renderer.clear(colors.sky);
        this.renderer.drawBackground(colors);
        this.renderer.drawGround(colors, 520);
        this.renderer.drawCloud(100, 80, 1);
        this.renderer.drawCloud(300, 120, 0.8);
        this.renderer.drawCloud(600, 60, 1.2);
        this.renderer.drawCloud(850, 100, 0.9);
        this.renderer.drawHill(150, 520, 1.5);
        this.renderer.drawHill(400, 520, 1);
        this.renderer.drawHill(700, 520, 2);
    }
}
