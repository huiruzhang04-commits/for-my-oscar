class InputManager {
    constructor() {
        this.keys = {};
        this.justPressed = {};
        this.justReleased = {};
        this.setupListeners();
    }

    setupListeners() {
        window.addEventListener('keydown', (e) => {
            if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Space', 'KeyA', 'KeyD', 'KeyW'].includes(e.code) || e.code === 'Space') {
                e.preventDefault();
            }
            if (!this.keys[e.code]) {
                this.justPressed[e.code] = true;
            }
            this.keys[e.code] = true;
        });

        window.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
            this.justReleased[e.code] = true;
        });
    }

    isPressed(code) {
        return this.keys[code] === true;
    }

    isJustPressed(code) {
        if (this.justPressed[code]) {
            this.justPressed[code] = false;
            return true;
        }
        return false;
    }

    isJustReleased(code) {
        if (this.justReleased[code]) {
            this.justReleased[code] = false;
            return true;
        }
        return false;
    }

    getLeft() {
        return this.isPressed('ArrowLeft') || this.isPressed('KeyA');
    }

    getRight() {
        return this.isPressed('ArrowRight') || this.isPressed('KeyD');
    }

    getJump() {
        return this.isJustPressed('Space') || this.isJustPressed('ArrowUp') || this.isJustPressed('KeyW');
    }

    getJumpHeld() {
        return this.isPressed('Space') || this.isPressed('ArrowUp') || this.isPressed('KeyW');
    }

    clear() {
        this.justPressed = {};
        this.justReleased = {};
    }
}

const input = new InputManager();
