class Coin {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 24;
        this.height = 24;
        this.active = true;
        this.collected = false;
        this.bounceY = y;
        this.bounceDir = -1;
        this.collectAnim = 0;
    }

    update() {
        if (this.collected) {
            this.collectAnim++;
            this.y -= 3;
            if (this.collectAnim > 20) {
                this.active = false;
            }
            return;
        }

        if (this.bounceDir === -1) {
            this.bounceY -= 0.5;
            if (this.bounceY < this.y - 8) {
                this.bounceDir = 1;
            }
        } else {
            this.bounceY += 0.5;
            if (this.bounceY > this.y) {
                this.bounceY = this.y;
                this.bounceDir = -1;
            }
        }
    }

    collect() {
        this.collected = true;
        this.bounceY = this.y;
    }

    getBounds() {
        return {
            x: this.x,
            y: this.bounceY,
            width: this.width,
            height: this.height
        };
    }
}

class Mushroom {
    constructor(x, y, type = 'power') {
        this.x = x;
        this.y = y;
        this.width = 28;
        this.height = 28;
        this.vx = 0.3;  // 很慢，方便小朋友捡
        this.startX = x;  // 限制移动范围
        this.moveRange = 80;  // 只能前后移动约80px
        this.vy = 0;
        this.active = true;
        this.collected = false;
        this.emerging = true;
        this.emergeY = y + 32;
        this.targetY = y;
        this.type = type;
    }

    update() {
        if (this.collected) {
            this.active = false;
            return;
        }

        if (this.emerging) {
            this.y -= 1;
            if (this.y <= this.targetY) {
                this.y = this.targetY;
                this.emerging = false;
            }
            return;
        }

        this.x += this.vx;
        // 限制移动范围，超出后反向
        if (this.x < this.startX - this.moveRange || this.x > this.startX + this.moveRange) {
            this.vx *= -1;
        }
        Physics.applyGravity(this);
        Physics.updatePosition(this);
    }

    collect() {
        this.collected = true;
    }

    reverse() {
        this.vx *= -1;
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

class Star {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 24;
        this.height = 24;
        this.vx = 0.5;  // 慢速，不要飞走
        this.startX = x;  // 限制移动范围
        this.moveRange = 150;
        this.vy = 0;
        this.active = true;
        this.collected = false;
        this.bounceY = y;
        this.bounceTimer = 0;
    }

    update() {
        if (this.collected) {
            this.active = false;
            return;
        }

        this.bounceTimer++;
        this.bounceY = this.y + Math.sin(this.bounceTimer * 0.2) * 5;

        this.x += this.vx;
        // 限制移动范围，超出后反向
        if (this.x < this.startX - this.moveRange || this.x > this.startX + this.moveRange) {
            this.vx *= -1;
        }
        Physics.applyGravity(this);
        Physics.updatePosition(this);
    }

    collect() {
        this.collected = true;
    }

    reverse() {
        this.vx *= -1;
    }

    getBounds() {
        return {
            x: this.x,
            y: this.bounceY,
            width: this.width,
            height: this.height
        };
    }
}

class Brick {
    constructor(x, y, hasItem = false, item = null) {
        this.x = x;
        this.y = y;
        this.width = 32;
        this.height = 32;
        this.hasItem = hasItem;
        this.item = item;
        this.itemGiven = false;
        this.hitAnim = 10;
        this.type = 'brick';
    }

    hit() {
        if (this.hasItem && !this.itemGiven) {
            this.itemGiven = true;
            this.hitAnim = 10;
            return this.item;
        }
        return false;
    }

    update() {
        if (this.hitAnim > 0) {
            this.hitAnim--;
        }
    }

    getBounds() {
        return {
            x: this.x,
            y: this.y + (this.hitAnim > 0 ? -4 : 0),
            width: this.width,
            height: this.height
        };
    }
}

class Platform {
    constructor(x, y, width, height, type = 'ground') {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.type = type;
        // 移动平台属性
        this.moving = false;
        this.moveAxis = 'x';
        this.moveSpeed = 0;
        this.moveRange = 0;
        this.moveOriginX = x;
        this.moveOriginY = y;
        this.moveDir = 1;
        this.vx = 0;
        this.vy = 0;
    }

    getBounds() {
        return this;
    }

    update() {
        if (!this.moving) return;
        const prevX = this.x;
        const prevY = this.y;
        if (this.moveAxis === 'x') {
            this.x += this.moveSpeed * this.moveDir;
            if (Math.abs(this.x - this.moveOriginX) >= this.moveRange) {
                this.moveDir *= -1;
            }
        } else {
            this.y += this.moveSpeed * this.moveDir;
            if (Math.abs(this.y - this.moveOriginY) >= this.moveRange) {
                this.moveDir *= -1;
            }
        }
        this.vx = this.x - prevX;
        this.vy = this.y - prevY;
    }
}
