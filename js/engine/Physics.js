class Physics {
    static GRAVITY = 0.6;
    static MAX_FALL_SPEED = 15;
    static FRICTION = 0.85;

    static applyGravity(entity) {
        if (entity.onGround) return;
        entity.vy += this.GRAVITY;
        if (entity.vy > this.MAX_FALL_SPEED) {
            entity.vy = this.MAX_FALL_SPEED;
        }
    }

    static applyFriction(entity) {
        if (entity.onGround) {
            entity.vx *= this.FRICTION;
        }
    }

    static updatePosition(entity) {
        entity.x += entity.vx;
        entity.y += entity.vy;
    }

    static checkCollision(a, b) {
        return a.x < b.x + b.width &&
               a.x + a.width > b.x &&
               a.y < b.y + b.height &&
               a.y + a.height >= b.y;
    }

    static checkPlatformCollision(player, platforms) {
        player.onGround = false;
        
        for (const platform of platforms) {
            if (!this.checkCollision(player, platform)) continue;

            const playerBottom = player.y + player.height;
            const playerTop = player.y;
            const playerLeft = player.x;
            const playerRight = player.x + player.width;

            const platTop = platform.y;
            const platBottom = platform.y + platform.height;
            const platLeft = platform.x;
            const platRight = platform.x + platform.width;

            const overlapBottom = playerBottom - platTop;
            const overlapTop = platBottom - playerTop;
            const overlapLeft = playerRight - platLeft;
            const overlapRight = platRight - playerLeft;

            const minOverlap = Math.min(overlapBottom, overlapTop, overlapLeft, overlapRight);

            if (minOverlap === overlapBottom && player.vy >= 0) {
                player.y = platTop - player.height;
                player.vy = 0;
                player.onGround = true;
                // 移动平台：玩家跟着平台水平移动
                if (platform.moving && platform.moveAxis === 'x') {
                    player.x += platform.vx;
                }
                if (platform.type === 'brick' && platform.hasItem) {
                    return { type: 'brick_hit', platform };
                }
            } else if (minOverlap === overlapTop && player.vy < 0) {
                player.y = platBottom;
                player.vy = 0;
            } else if (minOverlap === overlapLeft && platform.type !== 'ground') {
                player.x = platLeft - player.width;
                player.vx = 0;
            } else if (minOverlap === overlapRight && platform.type !== 'ground') {
                player.x = platRight;
                player.vx = 0;
            }
        }

        return null;
    }

    static checkItemCollision(player, items) {
        const collected = [];
        
        for (let i = items.length - 1; i >= 0; i--) {
            const item = items[i];
            if (!item.active) continue;
            
            if (this.checkCollision(player, item)) {
                collected.push(item);
                item.active = false;
            }
        }
        
        return collected;
    }

    static checkEnemyCollision(player, enemies) {
        for (const enemy of enemies) {
            if (!enemy.active || enemy.dead) continue;
            
            if (this.checkCollision(player, enemy)) {
                const playerBottom = player.y + player.height;
                const enemyTop = enemy.y;
                const playerCenterX = player.x + player.width / 2;
                const enemyCenterX = enemy.x + enemy.width / 2;
                
                if (player.vy > 0 && playerBottom < enemyTop + enemy.height / 2) {
                    return { type: 'stomp', enemy };
                } else if (player.isStar) {
                    return { type: 'star_kill', enemy };
                } else if (!player.invincible) {
                    return { type: 'hurt', enemy };
                }
            }
        }
        return null;
    }

    static checkBoundary(entity, worldWidth, worldHeight) {
        if (entity.x < 0) {
            entity.x = 0;
            entity.vx = 0;
        }
        if (entity.x + entity.width > worldWidth) {
            entity.x = worldWidth - entity.width;
            entity.vx = 0;
        }
        if (entity.y > worldHeight) {
            entity.y = worldHeight - entity.height;
            entity.vy = 0;
            entity.onGround = true;
        }
    }
}
