/**
 * Renderer - 精灵图渲染器
 * 所有绘制方法优先使用 SpriteLoader 加载的精灵图，
 * 若精灵未加载则自动使用色块 fallback。
 */

class Renderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;
        this.cameraX = 0;
        this.cameraY = 0;
    }

    setCamera(x, y) {
        this.cameraX = x;
        this.cameraY = y;
    }

    applyCamera() {
        this.ctx.save();
        this.ctx.translate(-this.cameraX, -this.cameraY);
    }

    removeCamera() {
        this.ctx.restore();
    }

    clear(color = '#5c94fc') {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(0, 0, this.width, this.height);
    }

    // ==================== 背景 ====================

    drawBackground(colors) {
        // 优先使用 SMW 背景图（山丘+灌木丛远景层）
        if (window.spriteLoader && window.spriteLoader.has('smw_background')) {
            const bgImg = window.spriteLoader.images.get('smw_background');
            if (bgImg) {
                // SMW背景图 5120x432，远宽于画布(960)
                // 高度缩放到250px（约占画布46%），宽度随之按比例
                const targetH = 250;
                const scale = targetH / bgImg.height;  // = 250/432 ≈ 0.579
                const drawW = bgImg.width * scale;   // ≈ 2967
                const drawH = bgImg.height * scale; // = 250
                
                // 底部对齐地面 y=420
                const offsetY = 420 - drawH;
                
                // 视差滚动：背景移动速度是前景的30%
                // 背景宽度>画布，需要偏移使居中
                const parallax = this.cameraX * 0.3;
                const offsetX = -parallax;
                
                // 裁剪超出画布的部分
                const srcX = Math.max(0, Math.floor(-offsetX / scale));
                const srcW = Math.min(bgImg.width - srcX, Math.ceil((this.width - offsetX) / scale));
                const destX = Math.max(0, Math.floor(offsetX));
                const destW = Math.min(srcW * scale, this.width - destX);
                
                if (destW > 0) {
                    this.ctx.drawImage(bgImg,
                        srcX, 0, srcW, bgImg.height,
                        destX, offsetY, destW, drawH
                    );
                }
                
                // 天空填充上方空白
                this.ctx.fillStyle = '#5c94fc';
                this.ctx.fillRect(0, 0, this.width, offsetY);
                return;
            }
        }
        
        // Fallback: 原来的渐变天空
        const gradient = this.ctx.createLinearGradient(0, 0, 0, this.height * 0.8);
        gradient.addColorStop(0, colors.skyGradient[0]);
        gradient.addColorStop(1, colors.skyGradient[1]);
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.width, this.height);
    }

    drawGround(colors, groundY, width = 2000) {
        // 优先使用 SMW 地面精灵
        const useSMWGround = window.spriteLoader && 
            window.spriteLoader.has('smw_ground_top') && 
            window.spriteLoader.has('smw_ground_fill');
        
        const groundHeight = this.height - groundY;
        
        if (useSMWGround) {
            // SMW 地面：草顶7px + 土主体（剩余高度）
            const tileW = 32;
            const grassH = 7;
            const dirtH = groundHeight - grassH;
            
            // 草顶平铺
            for (let gx = 0; gx < width; gx += tileW) {
                window.spriteLoader.draw('smw_ground_top', gx, groundY, this.ctx, 
                    { width: tileW, height: grassH });
            }
            // 土主体平铺（从草顶下方开始）
            if (dirtH > 0) {
                for (let gx = 0; gx < width; gx += tileW) {
                    window.spriteLoader.draw('smw_ground_fill', gx, groundY + grassH, this.ctx,
                        { width: tileW, height: dirtH });
                }
            }
        } else {
            // Fallback: 原来的 PIL 生成地面
            window.spriteLoader.draw('ground_top', 0, groundY, this.ctx, { width: width, height: 32 });
            for (let gx = 0; gx < width; gx += 32) {
                window.spriteLoader.draw('ground_fill', gx, groundY + 32, this.ctx, 
                    { width: 32, height: groundHeight - 32 });
            }
        }
    }

    drawCloud(x, y, size = 1) {
        const w = Math.round(64 * size);
        const h = Math.round(32 * size);
        window.spriteLoader.draw('cloud', x, y - h / 2, this.ctx, { width: w, height: h });
    }

    drawHill(x, groundY, size = 1) {
        const w = Math.round(120 * size);
        const h = Math.round(60 * size);
        window.spriteLoader.draw('hill', x - w / 2, groundY - h, this.ctx, { width: w, height: h });
    }

    // ==================== 平台 / 砖块 ====================

    drawPlatform(platform) {
        const { x, y, width, height, type } = platform;

        if (type === 'brick') {
            // 支持多块平铺
            for (let bx = 0; bx < width; bx += 32) {
                const bw = Math.min(32, width - bx);
                window.spriteLoader.draw('block_brick', x + bx, y, this.ctx, { width: bw, height: height });
            }
            if (platform.hasItem && !platform.itemGiven) {
                this.ctx.fillStyle = '#fff';
                this.ctx.font = 'bold 20px Arial';
                this.ctx.textAlign = 'center';
                this.ctx.fillText('?', x + width / 2 - 5, y + height / 2 + 7);
            }
        } else if (type === 'question') {
            for (let bx = 0; bx < width; bx += 32) {
                const bw = Math.min(32, width - bx);
                window.spriteLoader.draw('block_question', x + bx, y, this.ctx, { width: bw, height: height });
            }
        } else if (type === 'ground') {
            this.drawGround({ grasse: '#4CAF50' }, y, width);
        } else if (type === 'pipe') {
            this.drawPipe(x, y, width, height);
        }
    }

    drawPipe(x, y, width, height) {
        // 管道顶部（宽于主体）
        const topH = 32;
        window.spriteLoader.draw('pipe_top', x - 8, y, this.ctx, { width: width + 16, height: topH });
        // 管道主体（平铺）
        for (let py = y + topH; py < y + height; py += 32) {
            const remain = y + height - py;
            const bh = Math.min(32, remain);
            window.spriteLoader.draw('pipe_body', x, py, this.ctx, { width: width, height: bh });
        }
    }

    // ==================== 玩家（马里奥）====================

    /**
     * 根据玩家状态选择精灵并绘制
     * @param {Object} player - Player 实例
     * @param {number} [animFrame] - 动画帧（0/1/2 循环）
     */
    drawPlayer(player, animFrame = 0) {
        const { x, y, width, height, direction, isBig, isStar, vy } = player;

        // 判断动作状态
        const isJumping = vy !== 0;
        const size = isBig ? 'big' : 'small';
        const star = isStar ? '_star' : '';
        let spriteName;

        if (isJumping) {
            spriteName = `mario_${size}_jump${star}`;
        } else {
            // 行走动画用 walk 帧，站立用 idle
            const walkFrames = window.spriteLoader.getConfig(`mario_${size}_walk`);
            if (walkFrames && walkFrames.frames > 1) {
                spriteName = `mario_${size}_walk`;
            } else {
                spriteName = `mario_${size}_idle${star}`;
            }
        }

        const flipX = direction === -1;
        // SMM2 精灵尺寸: small=51x64, big=64x80
        const sw = isBig ? 40 : 32;   // 游戏内绘制宽度
        const sh = isBig ? 56 : 44;   // 游戏内绘制高度

        // 星星状态加闪光滤镜
        if (isStar) {
            this.ctx.save();
            const hue = (Date.now() / 30) % 360;
            this.ctx.filter = `hue-rotate(${hue}deg) brightness(1.3)`;
        }

        window.spriteLoader.draw(spriteName, x, y, this.ctx, {
            frame: animFrame,
            width: sw,
            height: sh,
            flipX: flipX,
        });

        if (isStar) this.ctx.restore();
    }

    // ==================== 敌人 ====================

    drawGoomba(enemy) {
        const { x, y, width, height, dead, deadTimer } = enemy;

        if (dead) {
            this.ctx.globalAlpha = Math.max(0, 1 - deadTimer / 30);
            window.spriteLoader.draw('goomba_stomp', x, y + height - 16, this.ctx, { width: 28, height: 16 });
            this.ctx.globalAlpha = 1;
            return;
        }

        const walkFrame = Math.floor(Date.now() / 200) % 2; // 2 帧行走动画
        window.spriteLoader.draw('goomba_walk', x, y, this.ctx, {
            frame: walkFrame,
            width: 28,
            height: 32,
        });
    }

    drawKoopa(enemy) {
        const { x, y, width, height, dead, deadTimer, isShell, shellMoving, direction } = enemy;

        if (dead) {
            this.ctx.globalAlpha = Math.max(0, 1 - deadTimer / 30);
            window.spriteLoader.draw('koopa_shell', x, y + height - 24, this.ctx, { width: 32, height: 24 });
            this.ctx.globalAlpha = 1;
            return;
        }

        if (isShell) {
            // 龟壳形态
            window.spriteLoader.draw('koopa_shell', x, y + height - 24, this.ctx, { width: 32, height: 24 });
        } else {
            // 行走形态
            const walkFrame = Math.floor(Date.now() / 200) % 2;
            window.spriteLoader.draw('koopa_walk', x, y, this.ctx, {
                frame: walkFrame,
                width: 32,
                height: 44,
                flipX: direction === -1,
            });
        }
    }

    // ==================== Boss（库巴）====================

    drawBoss(boss) {
        const { x, y, hurtTimer, defeated } = boss;
        if (defeated) return;

        const spriteName = hurtTimer > 0 ? 'bowser_hurt' : 'bowser_idle';
        window.spriteLoader.draw(spriteName, x, y, this.ctx, { width: 80, height: 80 });

        // 眼睛（叠加在精灵上面，若精灵本身已含眼睛可删除此段）
        if (hurtTimer <= 0) {
            this.ctx.fillStyle = '#fff';
            this.ctx.beginPath();
            this.ctx.arc(x + 30, y + 30, 10, 0, Math.PI * 2);
            this.ctx.arc(x + 50, y + 30, 10, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.fillStyle = '#d32f2f';
            this.ctx.beginPath();
            this.ctx.arc(x + 32, y + 32, 5, 0, Math.PI * 2);
            this.ctx.arc(x + 52, y + 32, 5, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }

    // ==================== 物品 ====================

    drawCoin(item) {
        const { x, y, collected } = item;
        if (collected) return;
        const frame = Math.floor(Date.now() / 150) % 4; // 金币旋转 4 帧
        window.spriteLoader.draw('coin', x, y, this.ctx, { frame, width: 16, height: 16 });
    }

    drawMushroom(item) {
        const { x, y, collected } = item;
        if (collected) return;
        window.spriteLoader.draw('mushroom', x, y, this.ctx, { width: 16, height: 16 });
    }

    drawStar(item) {
        const { x, y, collected } = item;
        if (collected) return;
        // 星星也可以用精灵，若未加载则用程序化绘制作为 fallback
        if (window.spriteLoader.has('star')) {
            window.spriteLoader.draw('star', x, y, this.ctx, { width: 16, height: 16 });
        } else {
            this.drawStarFallback(x, y);
        }
    }

    /** 星星程序化 fallback（保持原有的闪光效果）*/
    drawStarFallback(x, y) {
        const centerX = x + 8;
        const centerY = y + 8;
        const hue = (Date.now() / 5) % 360;

        this.ctx.fillStyle = `hsla(${hue}, 100%, 70%, 0.3)`;
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, 12, 0, Math.PI * 2);
        this.ctx.fill();

        this.ctx.fillStyle = `hsl(${hue}, 100%, 60%)`;
        this.ctx.shadowColor = `hsl(${hue}, 100%, 60%)`;
        this.ctx.shadowBlur = 10;
        this.ctx.beginPath();
        for (let i = 0; i < 5; i++) {
            const angle = (i * 4 * Math.PI) / 5 - Math.PI / 2;
            const px = centerX + Math.cos(angle) * 8;
            const py = centerY + Math.sin(angle) * 8;
            if (i === 0) this.ctx.moveTo(px, py);
            else this.ctx.lineTo(px, py);
        }
        this.ctx.closePath();
        this.ctx.fill();
        this.ctx.shadowBlur = 0;
    }

    // ==================== 单词路障（书本）====================

    drawWordTrigger(x) {
        // y 固定（地面上方）
        const y = 388; // 地面顶部420 - 单词块高度32 - 微调间距 = 站在地面上
        window.spriteLoader.draw('word_block', x, y, this.ctx, { width: 48, height: 40 });
    }

    // ==================== UI 辅助 ====================

    setFont(size, weight = 'bold') {
        this.ctx.font = `${weight} ${size}px Arial`;
    }

    drawText(text, x, y, color = '#fff', align = 'left') {
        this.ctx.fillStyle = color;
        this.ctx.textAlign = align;
        this.ctx.fillText(text, x, y);
    }

    drawScore(coins, x = 20, y = 30) {
        this.ctx.fillStyle = '#FFD700';
        this.ctx.font = 'bold 20px Arial';
        this.ctx.fillText(`🪙 ${coins}`, x, y);
    }
}

// 确保全局可用
window.Renderer = Renderer;
