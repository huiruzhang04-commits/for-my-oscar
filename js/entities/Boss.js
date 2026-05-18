class Boss {
    constructor() {
        this.x = 700;
        this.y = 320;
        this.width = 120;
        this.height = 160;
        this.hp = 3;
        this.maxHp = 3;
        this.active = false;
        this.defeated = false;
        this.hurtTimer = 0;
        this.moveTimer = 0;
        this.currentX = 700;
        this.startX = 700;
    }

    activate() {
        this.active = true;
        this.hp = this.maxHp;
        this.defeated = false;
        this.currentX = this.startX;
    }

    update() {
        if (!this.active) return;

        if (this.hurtTimer > 0) {
            this.hurtTimer--;
        }

        this.moveTimer++;
        if (this.moveTimer > 60) {
            this.currentX += (Math.random() - 0.5) * 10;
            this.currentX = Math.max(500, Math.min(800, this.currentX));
            this.moveTimer = 0;
        }
    }

    hit() {
        this.hp--;
        this.hurtTimer = 20;
        
        this.currentX += 30;
        
        if (this.hp <= 0) {
            this.defeated = true;
            this.active = false;
            return true;
        }
        return false;
    }

    miss() {
        this.currentX -= 30;
        this.currentX = Math.max(400, this.currentX);
    }

    reset() {
        this.active = false;
        this.defeated = false;
        this.hp = this.maxHp;
        this.currentX = this.startX;
        this.hurtTimer = 0;
    }

    getPosition() {
        return {
            x: this.currentX,
            y: this.y
        };
    }

    getHpPercent() {
        return (this.hp / this.maxHp) * 100;
    }
}
