class ProgressManager {
    constructor() {
        this.STORAGE_KEY = 'mario_word_game_progress';
        this.load();
    }

    load() {
        const saved = localStorage.getItem(this.STORAGE_KEY);
        if (saved) {
            this.data = JSON.parse(saved);
        } else {
            this.data = {
                currentWorld: 1,
                currentLevel: 1,
                unlockedWorlds: [1],
                completedLevels: [],
                totalCoins: 0,
                learnedWords: [],
                learnedLetters: [],
                settings: {
                    sound: true,
                    music: true,
                    difficulty: "normal"
                }
            };
        }
    }

    save() {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.data));
    }

    getCurrentWorld() {
        return this.data.currentWorld;
    }

    getCurrentLevel() {
        return this.data.currentLevel;
    }

    setCurrentLevel(world, level) {
        this.data.currentWorld = world;
        this.data.currentLevel = level;
        this.save();
    }

    isWorldUnlocked(world) {
        return this.data.unlockedWorlds.includes(world);
    }

    unlockWorld(world) {
        if (!this.data.unlockedWorlds.includes(world)) {
            this.data.unlockedWorlds.push(world);
            this.save();
        }
    }

    isLevelCompleted(levelId) {
        return this.data.completedLevels.includes(levelId);
    }

    completeLevel(levelId, coinsEarned, wordsLearned) {
        if (!this.data.completedLevels.includes(levelId)) {
            this.data.completedLevels.push(levelId);
        }
        this.data.totalCoins += coinsEarned;
        
        wordsLearned.forEach(word => {
            if (!this.data.learnedWords.includes(word)) {
                this.data.learnedWords.push(word);
            }
        });

        const levelData = this.getLevelData(levelId);
        if (levelData) {
            const letter = levelData.letter;
            if (!this.data.learnedLetters.includes(letter)) {
                this.data.learnedLetters.push(letter);
            }
        }

        this.save();
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

    getTotalCoins() {
        return this.data.totalCoins;
    }

    addCoins(amount) {
        this.data.totalCoins += amount;
        this.save();
    }

    getLearnedWords() {
        return this.data.learnedWords;
    }

    getLearnedLetters() {
        return this.data.learnedLetters;
    }

    getSettings() {
        return this.data.settings;
    }

    updateSettings(settings) {
        this.data.settings = { ...this.data.settings, ...settings };
        this.save();
    }

    getWorldProgress(world) {
        const levelData = this.getWorldLevelData(world);
        const completed = levelData.filter(l => this.isLevelCompleted(l)).length;
        return {
            completed,
            total: levelData.length
        };
    }

    getWorldLevelData(world) {
        const worlds = ['world1', 'world2', 'world3', 'world4', 'world5'];
        const worldKey = worlds[world - 1];
        if (WORDS_DATA[worldKey]) {
            return Object.keys(WORDS_DATA[worldKey].levels);
        }
        return [];
    }

    getNextLevel(currentLevelId) {
        const match = currentLevelId.match(/L(\d+)/);
        if (!match) return null;
        const currentNum = parseInt(match[1]);
        const nextNum = currentNum + 1;
        
        if (nextNum > 26) return null;
        
        return `L${nextNum}`;
    }

    reset() {
        this.data = {
            currentWorld: 1,
            currentLevel: 1,
            unlockedWorlds: [1],
            completedLevels: [],
            totalCoins: 0,
            learnedWords: [],
            learnedLetters: [],
            settings: {
                sound: true,
                music: true,
                difficulty: "normal"
            }
        };
        this.save();
    }
}

const progressManager = new ProgressManager();
