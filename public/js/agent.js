class Agent {
    constructor(x, y, world) {
        this.size = 20;
        this.maxSpeed = 0.8;
        this.body = Matter.Bodies.circle(x, y, this.size);
        this.body.frictionAir = 0.1;

        Matter.World.add(world, [this.body]);
    }

    iterate(inputs) {
        var lookAngle = Matter.Vector.angle(
            this.body.position,
            Matter.Vector.create(inputs.mouseX, inputs.mouseY)
        );
        Matter.Body.rotate(this.body, lookAngle - this.body.angle);

        if (inputs.up && this.body.velocity.y > -this.maxSpeed) {
            Matter.Body.applyForce(this.body, this.body.position, {x:0, y: -0.01});
        }
        if (inputs.down && this.body.velocity.y < this.maxSpeed) {
            Matter.Body.applyForce(this.body, this.body.position, {x:0, y: 0.01});
        }
        if (inputs.left && this.body.velocity.x > -this.maxSpeed) {
            Matter.Body.applyForce(this.body, this.body.position, {x:-0.01, y: 0});
        }
        if (inputs.right && this.body.velocity.x < this.maxSpeed) {
            Matter.Body.applyForce(this.body, this.body.position, {x:0.01, y: 0});
        }

        Matter.Body.setVelocity(
            this.body,
            {
                x: Matter.Common.clamp(this.body.velocity.x, -this.maxSpeed, this.maxSpeed),
                y: Matter.Common.clamp(this.body.velocity.y, -this.maxSpeed, this.maxSpeed)
            }
        );
    }
}
