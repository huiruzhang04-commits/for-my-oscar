class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 32;
        this.height = 32;
        this.vx = 0;
        this.vy = 0;
        this.speed = 4;
        this.jumpPower = -14;
        this.direction = 1;
        this.onGround = false;
        this.isBig = false;
        this.isStar = false;
        this.starTimer = 0;
        this.invincible = false;
        this.invincibleTimer = 0;
        this.frame = 0;
        this.frameTimer = 0;
        this.state = 'idle';
    }

    update() {
        if (input.getLeft()) {
            this.vx = -this.speed;
            this.direction = -1;
            this.state = 'running';
        } else if (input.getRight()) {
            this.vx = this.speed;
            this.direction = 1;
            this.state = 'running';
        } else {
            this.state = 'idle';
        }

        if (input.getJump() && this.onGround) {
            this.vy = this.jumpPower;
            this.onGround = false;
            // 播放跳跃音效
            if (window.soundManager) window.soundManager.playJump();
        }

        if (input.getJumpHeld() && this.vy < 0) {
        } else if (!input.getJumpHeld() && this.vy < -5) {
            this.vy = -5;
        }

        Physics.applyGravity(this);
        Physics.updatePosition(this);
        Physics.applyFriction(this);

        if (this.isStar) {
            this.starTimer--;
            if (this.starTimer <= 0) {
                this.isStar = false;
                this.starTimer = 0;
            }
        }

        if (this.invincible) {
            this.invincibleTimer--;
            if (this.invincibleTimer <= 0) {
                this.invincible = false;
                this.invincibleTimer = 0;
            }
        }

        this.frameTimer++;
        if (this.frameTimer > 8) {
            this.frame = (this.frame + 1) % 4;
            this.frameTimer = 0;
        }
    }

    grow() {
        if (!this.isBig) {
            this.isBig = true;
            this.height = 48;
            this.y -= 16;
        }
    }

    shrink() {
        if (this.isBig) {
            this.isBig = false;
            this.height = 32;
            this.y += 16;
            this.invincible = true;
            this.invincibleTimer = 60;
        } else {
            this.die();
        }
    }

    activateStar() {
        this.isStar = true;
        this.starTimer = 300;
    }

    die() {
        this.vy = -10;
        this.invincible = true;
    }

    getSize() {
        return {
            width: this.width,
            height: this.height
        };
    }

    reset(x, y) {
        this.x = x;
        this.y = y;
        this.vx = 0;
        this.vy = 0;
        this.isBig = false;
        this.isStar = false;
        this.invincible = false;
        this.height = 32;
        this.onGround = false;
    }
}
