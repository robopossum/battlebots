class DummyController {
    constructor() {
        this.inputs = {
            up: false,
            down: false,
            left: false,
            right: false,
            mouseX: 0,
            mouseY: 0,
            click: false
        };
    }

    iterate() {
        return this.inputs;
    }

}
