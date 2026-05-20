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
            // ===== SMM2 SMW 精灵 (从 Mario Maker 2 编辑器图标提取) =====
            // 马里奥 - 小尺寸 (51x64)
            { name: 'mario_small_idle',   src: spritePath + 'mario_small_idle.png',   frames: 1, frameWidth: 51, frameHeight: 64 },
            { name: 'mario_small_walk',   src: spritePath + 'mario_small_walk.png',   frames: 3, frameWidth: 51, frameHeight: 64 },
            { name: 'mario_small_jump',   src: spritePath + 'mario_small_jump.png',   frames: 1, frameWidth: 51, frameHeight: 64 },
            { name: 'mario_small_dead',   src: spritePath + 'mario_small_dead.png',   frames: 1, frameWidth: 51, frameHeight: 64 },
            // 马里奥 - 大尺寸 (64x80)
            { name: 'mario_big_idle',     src: spritePath + 'mario_big_idle.png',     frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'mario_big_walk',     src: spritePath + 'mario_big_walk.png',     frames: 3, frameWidth: 64, frameHeight: 80 },
            { name: 'mario_big_jump',     src: spritePath + 'mario_big_jump.png',     frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'mario_fire_idle',    src: spritePath + 'mario_fire_idle.png',    frames: 1, frameWidth: 64, frameHeight: 80 },
            // 兼容旧名称
            { name: 'mario_small_star',   src: spritePath + 'mario_small_jump.png',   frames: 1, frameWidth: 51, frameHeight: 64 },
            { name: 'mario_big_star',     src: spritePath + 'mario_big_jump.png',     frames: 1, frameWidth: 64, frameHeight: 80 },

            // ===== 敌人精灵 =====
            { name: 'goomba_walk',        src: spritePath + 'goomba.png',             frames: 2, frameWidth: 51, frameHeight: 64 },
            { name: 'goomba_flying',      src: spritePath + 'goomba_flying.png',      frames: 1, frameWidth: 51, frameHeight: 64 },
            { name: 'goomba_stomp',       src: spritePath + 'goomba.png',             frames: 1, frameWidth: 51, frameHeight: 32 },
            { name: 'koopa_green',        src: spritePath + 'koopa_green.png',        frames: 2, frameWidth: 51, frameHeight: 64 },
            { name: 'koopa_red',          src: spritePath + 'koopa_red.png',          frames: 2, frameWidth: 51, frameHeight: 64 },
            { name: 'piranha_green',      src: spritePath + 'piranha_green.png',      frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'piranha_red',        src: spritePath + 'piranha_red.png',        frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'buzzy_beetle',       src: spritePath + 'buzzy_beetle.png',       frames: 1, frameWidth: 64, frameHeight: 80 },
            // 兼容旧名称
            { name: 'koopa_walk',         src: spritePath + 'koopa_green.png',        frames: 2, frameWidth: 51, frameHeight: 64 },
            { name: 'koopa_shell',        src: spritePath + 'koopa_green.png',        frames: 1, frameWidth: 51, frameHeight: 64 },

            // ===== Boss =====
            { name: 'bowser_idle',        src: spritePath + 'koopa_red.png',          frames: 1, frameWidth: 80, frameHeight: 80 },
            { name: 'bowser_hurt',        src: spritePath + 'koopa_red.png',          frames: 1, frameWidth: 80, frameHeight: 80 },

            // ===== 物品精灵 =====
            { name: 'coin',               src: spritePath + 'coin.png',               frames: 4, frameWidth: 51, frameHeight: 64 },
            { name: 'question_block',     src: spritePath + 'question_block.png',     frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'brick',              src: spritePath + 'brick.png',              frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'ground',             src: spritePath + 'ground.png',             frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'block_empty',        src: spritePath + 'block_empty.png',        frames: 1, frameWidth: 64, frameHeight: 80 },
            // 兼容旧名称
            { name: 'mushroom',           src: spritePath + 'brick.png',              frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'star',               src: spritePath + 'coin.png',               frames: 1, frameWidth: 51, frameHeight: 64 },
            { name: 'block_question',     src: spritePath + 'question_block.png',     frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'block_brick',        src: spritePath + 'brick.png',              frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'ground_top',         src: spritePath + 'ground.png',             frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'ground_fill',        src: spritePath + 'ground.png',             frames: 1, frameWidth: 64, frameHeight: 80 },

            // ===== 管道 (SMM2) =====
            { name: 'pipe_top',           src: spritePath + 'pipe_green_top.png',     frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'pipe_body',          src: spritePath + 'pipe_green_body.png',    frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'pipe_green_piranha', src: spritePath + 'pipe_green_piranha.png', frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'pipe_yellow',        src: spritePath + 'pipe_yellow.png',        frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'pipe_red',           src: spritePath + 'pipe_red.png',           frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'pipe_blue',          src: spritePath + 'pipe_blue.png',          frames: 1, frameWidth: 64, frameHeight: 80 },

            // ===== 场景元素 (保留旧文件) =====
            { name: 'cloud',              src: spritePath + 'cloud.png',              frames: 1, frameWidth: 128, frameHeight: 64 },
            { name: 'hill',               src: spritePath + 'hill.png',               frames: 1, frameWidth: 128, frameHeight: 128 },
            { name: 'word_block',         src: spritePath + 'word_block.png',         frames: 1, frameWidth: 96, frameHeight: 80 },

            // ===== SMW 背景素材 (保留) =====
            { name: 'smw_background',     src: spritePath + 'smw/smw_background_clean.png', frames: 1, frameWidth: 5120, frameHeight: 432 },
            { name: 'smw_pipe',           src: spritePath + 'pipe_green_top.png',     frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'smw_question_block', src: spritePath + 'question_block.png',     frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'smw_brick',          src: spritePath + 'brick.png',              frames: 1, frameWidth: 64, frameHeight: 80 },
            { name: 'smw_ground_tile',    src: spritePath + 'ground.png',             frames: 1, frameWidth: 400, frameHeight: 34 },
            { name: 'smw_coin',           src: spritePath + 'coin.png',               frames: 1, frameWidth: 51, frameHeight: 64 },
            // SMW 地面瓦片
            { name: 'smw_ground_top',     src: spritePath + 'smw/smw_ground_top_tile.png', frames: 1, frameWidth: 32, frameHeight: 7 },
            { name: 'smw_ground_fill',    src: spritePath + 'smw/smw_ground_fill_tile.png', frames: 1, frameWidth: 32, frameHeight: 33 },
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
