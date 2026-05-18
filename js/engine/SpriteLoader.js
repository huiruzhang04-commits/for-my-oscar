/**
 * SpriteLoader - 精灵图资源加载器
 * 统一加载所有游戏精灵图，提供按名称获取精灵的能力
 * 
 * 使用方法：
 * 1. 将精灵图放入 assets/sprites/ 目录
 * 2. 在 SPRITE_CONFIG 中配置精灵的裁剪参数
 * 3. 调用 SpriteLoader.loadAll() 加载所有精灵
 * 4. 在 Renderer 中用 SpriteLoader.draw('mario_small_idle', x, y, ctx) 绘制
 */

class SpriteLoader {
    constructor() {
        /** @type {Map<string, HTMLImageElement>} */
        this.images = new Map();
        /** @type {Map<string, Object>} */
        this.configs = new Map();
        this.loaded = false;
    }

    /**
     * 加载单张图片
     * @param {string} name - 精灵名称（用于后续引用）
     * @param {string} src - 图片路径
     * @returns {Promise<void>}
     */
    loadImage(name, src) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                this.images.set(name, img);
                console.log(`✅ Sprite loaded: ${name} (${img.width}x${img.height})`);
                resolve();
            };
            img.onerror = () => {
                console.warn(`❌ Failed to load sprite: ${name} (${src})`);
                reject(new Error(`Failed to load: ${src}`));
            };
            img.src = src;
        });
    }

    /**
     * 加载所有配置的精灵图
     * @returns {Promise<void>}
     */
    async loadAll() {
        const spritePath = 'assets/sprites/';
        
        // 每张精灵图的配置：
        // name: 引用名称
        // src: 文件路径
        // frames: 帧数（用于动画）
        // frameWidth/frameHeight: 每帧尺寸（精灵图是横向排列的帧时）
        const spriteList = [
            // ===== 马里奥精灵 =====
            // 小马里奥 - 行走动画帧（建议 2-3 帧横向排列）
            { name: 'mario_small_walk',   src: spritePath + 'mario_small_walk.png',   frames: 3, frameWidth: 16, frameHeight: 16 },
            // 小马里奥 - 站立
            { name: 'mario_small_idle',   src: spritePath + 'mario_small_idle.png',   frames: 1, frameWidth: 16, frameHeight: 16 },
            // 小马里奥 - 跳跃
            { name: 'mario_small_jump',   src: spritePath + 'mario_small_jump.png',   frames: 1, frameWidth: 16, frameHeight: 16 },
            // 大马里奥 - 行走
            { name: 'mario_big_walk',     src: spritePath + 'mario_big_walk.png',     frames: 3, frameWidth: 16, frameHeight: 32 },
            // 大马里奥 - 站立
            { name: 'mario_big_idle',     src: spritePath + 'mario_big_idle.png',     frames: 1, frameWidth: 16, frameHeight: 32 },
            // 大马里奥 - 跳跃
            { name: 'mario_big_jump',     src: spritePath + 'mario_big_jump.png',     frames: 1, frameWidth: 16, frameHeight: 32 },
            // 星星马里奥（小）
            { name: 'mario_small_star',   src: spritePath + 'mario_small_star.png',   frames: 1, frameWidth: 16, frameHeight: 16 },
            // 星星马里奥（大）
            { name: 'mario_big_star',     src: spritePath + 'mario_big_star.png',     frames: 1, frameWidth: 16, frameHeight: 32 },

            // ===== 敌人精灵 =====
            // 栗子（Goomba）- 行走
            { name: 'goomba_walk',        src: spritePath + 'goomba_walk.png',        frames: 2, frameWidth: 16, frameHeight: 16 },
            // 栗子 - 被踩扁
            { name: 'goomba_stomp',       src: spritePath + 'goomba_stomp.png',       frames: 1, frameWidth: 16, frameHeight: 8  },

            // ===== 库巴（Boss）=====
            { name: 'bowser_idle',         src: spritePath + 'bowser_idle.png',         frames: 1, frameWidth: 40, frameHeight: 40 },
            { name: 'bowser_hurt',        src: spritePath + 'bowser_hurt.png',        frames: 1, frameWidth: 40, frameHeight: 40 },

            // ===== 物品精灵 =====
            // 金币
            { name: 'coin',               src: spritePath + 'coin.png',               frames: 4, frameWidth: 16, frameHeight: 16 },
            // 蘑菇
            { name: 'mushroom',           src: spritePath + 'mushroom.png',           frames: 1, frameWidth: 16, frameHeight: 16 },
            // 星星
            { name: 'star',               src: spritePath + 'star.png',               frames: 1, frameWidth: 16, frameHeight: 16 },

            // ===== 场景元素 =====
            // 砖块（问号块）
            { name: 'block_question',     src: spritePath + 'block_question.png',     frames: 1, frameWidth: 32, frameHeight: 32 },
            // 普通砖块
            { name: 'block_brick',        src: spritePath + 'block_brick.png',        frames: 1, frameWidth: 32, frameHeight: 32 },
            // 地面块
            { name: 'ground_top',         src: spritePath + 'ground_top.png',         frames: 1, frameWidth: 32, frameHeight: 32 },
            { name: 'ground_fill',        src: spritePath + 'ground_fill.png',        frames: 1, frameWidth: 32, frameHeight: 32 },
            // 管道
            { name: 'pipe_top',           src: spritePath + 'pipe_top.png',           frames: 1, frameWidth: 64, frameHeight: 32 },
            { name: 'pipe_body',          src: spritePath + 'pipe_body.png',          frames: 1, frameWidth: 64, frameHeight: 32 },
            // 云
            { name: 'cloud',              src: spritePath + 'cloud.png',              frames: 1, frameWidth: 64, frameHeight: 32 },
            // 山丘
            { name: 'hill',               src: spritePath + 'hill.png',               frames: 1, frameWidth: 64, frameHeight: 64 },
            // 单词路障（书本）
            { name: 'word_block',         src: spritePath + 'word_block.png',         frames: 1, frameWidth: 48, frameHeight: 40 },
        ];

        const promises = spriteList.map(sprite => {
            this.configs.set(sprite.name, sprite);
            return this.loadImage(sprite.name, sprite.src);
        });

        try {
            await Promise.all(promises);
            this.loaded = true;
            console.log(`✅ All sprites loaded! Total: ${this.images.size}`);
        } catch (e) {
            console.warn('⚠️ Some sprites failed to load, using fallbacks', e);
            this.loaded = true; // 仍然标记为已加载，未加载的会用色块代替
        }
    }

    /**
     * 绘制精灵（支持动画帧）
     * @param {string} name - 精灵名称
     * @param {number} x - 画布 X 坐标
     * @param {number} y - 画布 Y 坐标
     * @param {CanvasRenderingContext2D} ctx - 画布上下文
     * @param {Object} [options] - 可选参数
     * @param {number} [options.frame] - 动画帧索引（默认 0）
     * @param {number} [options.width] - 绘制宽度（默认 frameWidth）
     * @param {number} [options.height] - 绘制高度（默认 frameHeight）
     * @param {number} [options.flipX] - 是否水平翻转（默认 false）
     */
    draw(name, x, y, ctx, options = {}) {
        const config = this.configs.get(name);
        const img = this.images.get(name);

        if (!img || !config) {
            // 精灵未加载，用色块代替
            this.drawFallback(name, x, y, ctx, options);
            return;
        }

        const {
            frame = 0,
            width = config.frameWidth,
            height = config.frameHeight,
            flipX = false,
        } = options;

        const sx = frame * config.frameWidth;
        const sy = 0;

        ctx.save();
        if (flipX) {
            ctx.translate(x + width, y);
            ctx.scale(-1, 1);
            ctx.translate(-x, -y);
        }

        ctx.drawImage(
            img,
            sx, sy, config.frameWidth, config.frameHeight,  // 源图裁剪
            x, y, width, height                           // 画布绘制位置/大小
        );
        ctx.restore();
    }

    /**
     * 未加载到精灵时，用色块代替（保证游戏不崩溃）
     */
    drawFallback(name, x, y, ctx, options = {}) {
        const { width = 32, height = 32 } = options;
        
        const fallbackColors = {
            mario_small:     '#E53935',
            mario_big:       '#E53935',
            goomba:          '#8D6E63',
            coin:            '#FFD700',
            mushroom:        '#E53935',
            star:            '#FFD700',
            block_question:  '#FFA000',
            block_brick:     '#FFA000',
            pipe:            '#4CAF50',
            cloud:           '#FFFFFF',
            hill:            '#6ab04c',
            word_block:      '#8B4513',
            bowser:          '#4CAF50',
        };

        let color = '#CCC';
        for (const [key, val] of Object.entries(fallbackColors)) {
            if (name.includes(key)) {
                color = val;
                break;
            }
        }

        ctx.fillStyle = color;
        ctx.fillRect(x, y, width, height);
        
        // 显示名称（调试用）
        ctx.fillStyle = '#000';
        ctx.font = '8px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(name.split('_')[0], x + width / 2, y + height / 2 + 3);
    }

    /**
     * 获取精灵配置
     */
    getConfig(name) {
        return this.configs.get(name);
    }

    /**
     * 检查精灵是否已加载
     */
    has(name) {
        return this.images.has(name);
    }
}

// 导出全局实例
window.spriteLoader = new SpriteLoader();
