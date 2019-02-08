class KeyController {
    constructor(up, down, left, right, turnLeft, turnRight, shoot) {
        this.keys = {};
        this.keys[up || 'w'] = 'up';
        this.keys[down || 's'] = 'down';
        this.keys[left || 'a'] = 'left';
        this.keys[right || 'd'] = 'right';
        this.keys[turnLeft || 'ArrowLeft'] = 'turnLeft';
        this.keys[turnRight || 'ArrowRight'] = 'turnRight';
        this.keys[shoot || ' '] = 'shoot';

        this.inputs = {
            up: false,
            down: false,
            left: false,
            right: false,
            turnLeft: false,
            turnRight: false,
            shoot: false
        };

        document.addEventListener('keydown', this.handleKeys.bind(this));
        document.addEventListener('keyup', this.handleKeys.bind(this));
    }

    handleKeys(event) {
        if (!this.keys.hasOwnProperty(event.key)) {
            return;
        }
        this.inputs[this.keys[event.key]] = event.type == 'keydown';
    }

    iterate() {
	return clientControl;
        //return this.inputs;
    }
}
