class GameUI {
    constructor() {
        this.coinCount = document.getElementById('coin-count');
        this.levelInfo = document.getElementById('level-info');
        this.wordProgress = document.getElementById('word-progress');
        this.gameTimer = document.getElementById('game-timer');
        this.progressFill = document.getElementById('progress-fill');
        this.timerValue = 0;
        this.timerInterval = null;
    }

    updateCoins(count) {
        this.coinCount.textContent = count;
    }

    updateLevel(levelId, letter) {
        this.levelInfo.textContent = `${levelId} ${letter}`;
    }

    updateWordProgress(current, total) {
        this.wordProgress.textContent = `${current}/${total}`;
    }

    updateProgress(percent) {
        this.progressFill.style.width = percent + '%';
    }

    startTimer() {
        this.stopTimer();  // 先清除旧 interval，防止叠加
        this.timerValue = 0;
        this.timerInterval = setInterval(() => {
            this.timerValue++;
            const minutes = Math.floor(this.timerValue / 60);
            const seconds = this.timerValue % 60;
            this.gameTimer.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }

    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    getTimerValue() {
        return this.timerValue;
    }

    resetTimer() {
        this.stopTimer();
        this.timerValue = 0;
        this.gameTimer.textContent = '0:00';
    }
}

class MenuUI {
    constructor() {
        this.mainMenu = document.getElementById('main-menu');
        this.worldSelectModal = document.getElementById('world-select-modal');
        this.levelSelectModal = document.getElementById('level-select-modal');
        this.pauseModal = document.getElementById('pause-modal');
        this.worldList = document.getElementById('world-list');
        this.levelList = document.getElementById('level-list');
        this.worldTitle = document.getElementById('world-title');
    }

    showMainMenu() {
        this.mainMenu.classList.remove('hidden');
    }

    hideMainMenu() {
        this.mainMenu.classList.add('hidden');
    }

    showWorldSelect() {
        this.renderWorldList();
        this.worldSelectModal.classList.remove('hidden');
    }

    hideWorldSelect() {
        this.worldSelectModal.classList.add('hidden');
    }

    renderWorldList() {
        this.worldList.innerHTML = '';
        
        const worlds = [
            { id: 1, name: '草地王国', icon: '🌿', letter: 'Aa~Ee', levels: 5 },
            { id: 2, name: '洞穴王国', icon: '🕳️', letter: 'Ff~Jj', levels: 5 },
            { id: 3, name: '海底王国', icon: '🐠', letter: 'Kk~Pp', levels: 6 },
            { id: 4, name: '天空之城', icon: '☁️', letter: 'Qq~Uu', levels: 5 },
            { id: 5, name: '库巴城堡', icon: '🏰', letter: 'Vv~Zz', levels: 5 }
        ];

        worlds.forEach(world => {
            const unlocked = progressManager.isWorldUnlocked(world.id);
            const progress = progressManager.getWorldProgress(world.id);

            const item = document.createElement('div');
            item.className = `world-item ${unlocked ? 'unlocked' : 'locked'}`;
            
            item.innerHTML = `
                <span class="world-icon">${world.icon}</span>
                <div class="world-info">
                    <div class="world-name">${world.name}</div>
                    <div class="world-progress">${world.letter} · ${world.levels}课</div>
                </div>
                <span class="world-status">${unlocked ? `${progress.completed}/${progress.total} ✓` : '🔒'}</span>
            `;

            if (unlocked) {
                item.addEventListener('click', () => {
                    this.showLevelSelect(world.id, world.name);
                });
            }

            this.worldList.appendChild(item);
        });
    }

    showLevelSelect(worldId, worldName) {
        this.worldTitle.textContent = `${worldId === 1 ? '🌿' : worldId === 2 ? '🕳️' : worldId === 3 ? '🐠' : worldId === 4 ? '☁️' : '🏰'} ${worldName}`;
        this.renderLevelList(worldId);
        this.levelSelectModal.classList.remove('hidden');
    }

    renderLevelList(worldId) {
        this.levelList.innerHTML = '';
        
        const levels = progressManager.getWorldLevelData(worldId);
        
        levels.forEach(levelId => {
            const completed = progressManager.isLevelCompleted(levelId);
            const unlocked = this.isLevelUnlocked(levelId, worldId);
            
            const match = levelId.match(/L(\d+)/);
            const levelNum = match ? parseInt(match[1]) : 1;
            const worldData = this.getWorldDataForLevel(levelNum);
            const letter = worldData ? worldData.letter : '?';

            const item = document.createElement('div');
            item.className = `level-item ${completed ? 'completed' : ''} ${!unlocked ? 'locked' : ''} ${!completed && unlocked ? 'current' : ''}`;
            
            item.innerHTML = `
                <div class="level-num">${levelId}</div>
                <div class="level-status">${completed ? '✓' : unlocked ? '▶' : '🔒'}</div>
            `;

            if (unlocked) {
                item.addEventListener('click', () => {
                    this.hideLevelSelect();
                    if (this.onLevelSelect) {
                        this.onLevelSelect(levelId);
                    }
                });
            }

            this.levelList.appendChild(item);
        });
    }

    isLevelUnlocked(levelId, worldId) {
        // 测试模式：所有关卡解锁
        console.log('[DEBUG] isLevelUnlocked called:', levelId, worldId, '-> returning true');
        return true;
    }

    getWorldDataForLevel(levelNum) {
        if (levelNum >= 1 && levelNum <= 5) {
            return WORDS_DATA.world1.levels[`L${levelNum}`];
        } else if (levelNum >= 6 && levelNum <= 10) {
            return WORDS_DATA.world2.levels[`L${levelNum}`];
        } else if (levelNum >= 11 && levelNum <= 16) {
            return WORDS_DATA.world3.levels[`L${levelNum}`];
        } else if (levelNum >= 17 && levelNum <= 21) {
            return WORDS_DATA.world4.levels[`L${levelNum}`];
        } else if (levelNum >= 22 && levelNum <= 26) {
            return WORDS_DATA.world5.levels[`L${levelNum}`];
        }
        return null;
    }

    hideLevelSelect() {
        this.levelSelectModal.classList.add('hidden');
    }

    showPause() {
        this.pauseModal.classList.remove('hidden');
    }

    hidePause() {
        this.pauseModal.classList.add('hidden');
    }

    onLevelSelect = null;
}
