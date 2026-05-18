class Goomba {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 28;
        this.height = 28;
        this.vx = -1;
        this.vy = 0;
        this.active = true;
        this.dead = false;
        this.deadTimer = 0;
        this.direction = -1;
        this.onGround = true;
    }

    update() {
        if (this.dead) {
            this.deadTimer++;
            if (this.deadTimer > 30) {
                this.active = false;
            }
            return;
        }

        this.x += this.vx;

        Physics.applyGravity(this);
        Physics.updatePosition(this);

        if (this.vy > 0) {
            this.onGround = true;
        }
    }

    stomp() {
        this.dead = true;
        this.vy = -5;
    }

    reverse() {
        this.vx *= -1;
        this.direction *= -1;
    }

    getBounds() {
        return {
            x: this.x,
            y: this.y,
            width: this.width,
            height: this.height
        };
    }
}

class Koopa {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 28;
        this.height = 36;
        this.vx = -1;
        this.vy = 0;
        this.active = true;
        this.dead = false;
        this.deadTimer = 0;
        this.isShell = false;
        this.shellMoving = false;
        this.direction = -1;
    }

    update() {
        if (this.dead) {
            this.deadTimer++;
            if (this.deadTimer > 30) {
                this.active = false;
            }
            return;
        }

        if (!this.isShell || this.shellMoving) {
            this.x += this.vx;
        }

        Physics.applyGravity(this);
        Physics.updatePosition(this);
    }

    stomp() {
        if (!this.isShell) {
            this.isShell = true;
            this.height = 20;
            this.vx = 0;
            this.deadTimer = 0;
        } else if (!this.shellMoving) {
            this.shellMoving = true;
            this.vx = 8;
        }
    }

    reverse() {
        if (!this.isShell) {
            this.vx *= -1;
            this.direction *= -1;
        }
    }

    getBounds() {
        return {
            x: this.x,
            y: this.y,
            width: this.width,
            height: this.height
        };
    }
}
