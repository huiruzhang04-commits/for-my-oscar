/**
 * SoundManager - Web Audio API 音效系统
 * 使用程序化生成音效，无需外部音频文件
 */
class SoundManager {
    constructor() {
        this.audioContext = null;
        this.masterGain = null;
        this.enabled = true;
        this.initialized = false;
    }

    /**
     * 初始化音频上下文（需要用户交互后才能调用）
     */
    init() {
        if (this.initialized) return;
        
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.masterGain = this.audioContext.createGain();
            this.masterGain.gain.value = 0.3;
            this.masterGain.connect(this.audioContext.destination);
            this.initialized = true;
            console.log('✅ SoundManager initialized');
        } catch (e) {
            console.warn('❌ Web Audio API not supported:', e);
            this.enabled = false;
        }
    }

    /**
     * 播放跳跃音效
     */
    playJump() {
        if (!this.enabled || !this.initialized) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        oscillator.type = 'square';
        oscillator.frequency.setValueAtTime(300, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(600, this.audioContext.currentTime + 0.1);
        
        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.15);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.15);
    }

    /**
     * 播放金币收集音效
     */
    playCoin() {
        if (!this.enabled || !this.initialized) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        oscillator.type = 'square';
        oscillator.frequency.setValueAtTime(988, this.audioContext.currentTime);
        oscillator.frequency.setValueAtTime(1319, this.audioContext.currentTime + 0.05);
        
        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.3);
    }

    /**
     * 播放蘑菇/道具获得音效
     */
    playPowerUp() {
        if (!this.enabled || !this.initialized) return;
        
        const notes = [523, 659, 784, 1047];
        let time = this.audioContext.currentTime;
        
        notes.forEach((freq, index) => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.masterGain);
            
            oscillator.type = 'square';
            oscillator.frequency.value = freq;
            
            gainNode.gain.setValueAtTime(0, time + index * 0.1);
            gainNode.gain.linearRampToValueAtTime(0.2, time + index * 0.1 + 0.05);
            gainNode.gain.exponentialRampToValueAtTime(0.01, time + index * 0.1 + 0.2);
            
            oscillator.start(time + index * 0.1);
            oscillator.stop(time + index * 0.1 + 0.2);
        });
    }

    /**
     * 播放星星无敌音效
     */
    playStar() {
        if (!this.enabled || !this.initialized) return;
        
        const notes = [784, 988, 1175, 1568];
        let time = this.audioContext.currentTime;
        
        notes.forEach((freq, index) => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.masterGain);
            
            oscillator.type = 'sine';
            oscillator.frequency.value = freq;
            
            gainNode.gain.setValueAtTime(0, time + index * 0.08);
            gainNode.gain.linearRampToValueAtTime(0.2, time + index * 0.08 + 0.04);
            gainNode.gain.exponentialRampToValueAtTime(0.01, time + index * 0.08 + 0.15);
            
            oscillator.start(time + index * 0.08);
            oscillator.stop(time + index * 0.08 + 0.15);
        });
    }

    /**
     * 播放答题正确音效
     */
    playCorrect() {
        if (!this.enabled || !this.initialized) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(523, this.audioContext.currentTime);
        oscillator.frequency.setValueAtTime(659, this.audioContext.currentTime + 0.1);
        oscillator.frequency.setValueAtTime(784, this.audioContext.currentTime + 0.2);
        
        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.4);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.4);
    }

    /**
     * 播放答题错误音效
     */
    playWrong() {
        if (!this.enabled || !this.initialized) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        oscillator.type = 'sawtooth';
        oscillator.frequency.setValueAtTime(200, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(100, this.audioContext.currentTime + 0.3);
        
        gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.3);
    }

    /**
     * 播放踩敌人音效
     */
    playStomp() {
        if (!this.enabled || !this.initialized) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        oscillator.type = 'triangle';
        oscillator.frequency.setValueAtTime(400, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(100, this.audioContext.currentTime + 0.15);
        
        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.15);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.15);
    }

    /**
     * 播放死亡音效
     */
    playDeath() {
        if (!this.enabled || !this.initialized) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        oscillator.type = 'square';
        oscillator.frequency.setValueAtTime(600, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(100, this.audioContext.currentTime + 0.8);
        
        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.8);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.8);
    }

    /**
     * 播放Boss战背景音乐（简单循环）
     */
    playBossMusic() {
        if (!this.enabled || !this.initialized) return;
        
        // 停止当前BGM
        this.stopBossMusic();
        
        // 创建简单的Boss战BGM
        this.bossMusicOscillators = [];
        const baseTime = this.audioContext.currentTime;
        
        // 低音部分
        const bassOsc = this.audioContext.createOscillator();
        const bassGain = this.audioContext.createGain();
        
        bassOsc.connect(bassGain);
        bassGain.connect(this.masterGain);
        
        bassOsc.type = 'sawtooth';
        bassOsc.frequency.value = 110;
        bassGain.gain.value = 0.1;
        
        bassOsc.start(baseTime);
        this.bossMusicOscillators.push(bassOsc);
        
        // 旋律部分
        const melodyOsc = this.audioContext.createOscillator();
        const melodyGain = this.audioContext.createGain();
        
        melodyOsc.connect(melodyGain);
        melodyGain.connect(this.masterGain);
        
        melodyOsc.type = 'square';
        melodyOsc.frequency.value = 220;
        melodyGain.gain.value = 0.08;
        
        melodyOsc.start(baseTime);
        this.bossMusicOscillators.push(melodyOsc);
    }

    /**
     * 停止Boss战BGM
     */
    stopBossMusic() {
        if (this.bossMusicOscillators) {
            this.bossMusicOscillators.forEach(osc => {
                try {
                    osc.stop();
                } catch (e) {
                    // 忽略已经停止的振荡器
                }
            });
            this.bossMusicOscillators = [];
        }
    }

    /**
     * 播放通关音效
     */
    playLevelComplete() {
        if (!this.enabled || !this.initialized) return;
        
        const notes = [523, 659, 784, 1047, 784, 1047];
        let time = this.audioContext.currentTime;
        
        notes.forEach((freq, index) => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.masterGain);
            
            oscillator.type = 'sine';
            oscillator.frequency.value = freq;
            
            const startTime = time + index * 0.15;
            gainNode.gain.setValueAtTime(0, startTime);
            gainNode.gain.linearRampToValueAtTime(0.25, startTime + 0.05);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.3);
            
            oscillator.start(startTime);
            oscillator.stop(startTime + 0.3);
        });
    }

    /**
     * 播放Game Over音效
     */
    playGameOver() {
        if (!this.enabled || !this.initialized) return;
        
        const notes = [494, 440, 370, 330];
        let time = this.audioContext.currentTime;
        
        notes.forEach((freq, index) => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.masterGain);
            
            oscillator.type = 'triangle';
            oscillator.frequency.value = freq;
            
            const startTime = time + index * 0.3;
            gainNode.gain.setValueAtTime(0.25, startTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.4);
            
            oscillator.start(startTime);
            oscillator.stop(startTime + 0.4);
        });
    }

    /**
     * 切换音效开关
     */
    toggle() {
        this.enabled = !this.enabled;
        if (!this.enabled) {
            this.stopBossMusic();
        }
        return this.enabled;
    }

    /**
     * 设置主音量
     * @param {number} volume - 0到1之间
     */
    setVolume(volume) {
        if (this.masterGain) {
            this.masterGain.gain.value = Math.max(0, Math.min(1, volume));
        }
    }
}

// 导出全局实例
window.soundManager = new SoundManager();
