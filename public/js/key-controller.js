class KeyController {
    constructor(up, down, left, right) {
        this.keys = {};
        this.keys[up || 'w'] = 'up';
        this.keys[down || 's'] = 'down';
        this.keys[left || 'a'] = 'left';
        this.keys[right || 'd'] = 'right';

        this.inputs = {
            up: false,
            down: false,
            left: false,
            right: false,
            mouseX: 0,
            mouseY: 0,
            click: false
        };

        document.addEventListener('keydown', this.handleKeys.bind(this));
        document.addEventListener('keyup', this.handleKeys.bind(this));

        document.addEventListener('mousedown', this.handleMouse.bind(this));
        document.addEventListener('mouseup', this.handleMouse.bind(this));

        this.mouse = Matter.Mouse.create(document.body);
    }

    handleKeys(event) {
        if (!this.keys.hasOwnProperty(event.key)) {
            return;
        }
        this.inputs[this.keys[event.key]] = event.type == 'keydown';
    }

    handleMouse(event) {
        this.inputs.click = event.type == 'mousedown';
    }

    iterate() {
        this.inputs.mouseX = this.mouse.position.x;
        this.inputs.mouseY = this.mouse.position.y;
        return this.inputs;
    }
}
