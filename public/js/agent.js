class Agent {
    defaults() {
        this.size = 20;
        this.maxSpeed = 0.8;
        this.dV = 0.01;
        this.aV = ((10 / 360) * 2 * Math.PI);
        this.friction = 0.1;
        this.lastShot = 0;
        this.shotCd = 1000;
        this.shotSpeed = 2;
        this.shotRange = 300;
        this.xp = 0;
        this.hp = 100;
        this.sensors = [
            {angle: -50},
            {angle: -45},
            {angle: -40},
            {angle: -35},
            {angle: -30},
            {angle: -25},
            {angle: -20},
            {angle: -15},
            {angle: -10},
            {angle: -5},
            {angle: 0},
            {angle: 5},
            {angle: 10},
            {angle: 15},
            {angle: 20},
            {angle: 25},
            {angle: 30},
            {angle: 35},
            {angle: 40},
            {angle: 45},
            {angle: 50},
        ];
        this.sensorDist = 100;
	this.roleMap = {
	  agent: 1,
          xp: 2,
          wall: 3
	};
    }

    constructor(x, y, controller, engine) {
        this.defaults();

        this.controller = controller;
        this.engine = engine;

        this.body = Matter.Bodies.circle(x, y, this.size);
        this.body.frictionAir = this.friction;
        this.body.role = 'agent';
        Matter.World.add(this.engine.world, [this.body]);

        Matter.Events.on(this.engine, 'beforeUpdate', this.iterate.bind(this));
        Matter.Events.on(this.engine, 'shot:' + this.body.id, this.damaged.bind(this));
        Matter.Events.on(this.engine, 'xp:' + this.body.id, this.pickupXP.bind(this));
    }

    iterate(e) {
	connection.send({
		agentId: 1,
		messageType: 'frame',
                sensors: this.sensors,
		x: this.body.position.x,
		y: this.body.position.y,
		dX: this.body.velocity.x,
		dY: this.body.velocity.y,
		canShoot: this.canShoot(e.timestamp),
		xp: this.xp,
	});
	clientState = {
		agentId: 1,
		messageType: 'frame',
                sensors: this.sensors,
		x: this.body.position.x,
		y: this.body.position.y,
		dX: this.body.velocity.x,
		dY: this.body.velocity.y,
		canShoot: this.canShoot(e.timestamp),
		xp: this.xp,
	};
        var inputs = this.controller.iterate();

        this.look(inputs);

        Matter.Body.applyForce(
            this.body,
            this.body.position,
            this.move(
                inputs.up,
                inputs.down,
                inputs.left,
                inputs.right
            )
        );

        this.clampVel();

        if (inputs.shoot && this.canShoot(e.timestamp)) {
            this.shoot(e.timestamp);
        }
    }

    damaged(shot) {
        console.log("Ouch");
    }

    pickupXP(xp) {
        Matter.World.remove(this.engine.world, xp.body);
        this.xp += 1;
    }

    move(up, down, left, right) {
        var dir = Matter.Vector.create();
        if (up && this.body.velocity.y > -this.maxSpeed) {
            dir = Matter.Vector.add(dir, {x:0, y: -this.dV});
        }
        if (down && this.body.velocity.y < this.maxSpeed) {
            dir = Matter.Vector.add(dir, {x:0, y: this.dV});
        }
        if (left && this.body.velocity.x > -this.maxSpeed) {
            dir = Matter.Vector.add(dir, {x: -this.dV, y: 0});
        }
        if (right && this.body.velocity.x < this.maxSpeed) {
            dir = Matter.Vector.add(dir, {x: this.dV, y: 0});
        }
        return dir;
    }

    look(input) {
        let dA = 0;
        dA += input.turnRight ? this.aV : 0;
        dA -= input.turnLeft ? this.aV : 0;

        for (var i = 0; i < this.sensors.length; i++) {
            this.updateSensor(this.body.angle + dA, this.sensors[i]);
        }

        Matter.Body.rotate(this.body, dA);
    }

    updateSensor(look, sensor) {
        var end = Matter.Vector.create(1);
        end = Matter.Vector.rotate(end, look + ((sensor.angle / 360) * 2 * Math.PI));
        end = Matter.Vector.mult(end, this.sensorDist);
        end = Matter.Vector.add(this.body.position, end);

        var collisions = raycast(_.without(this.engine.world.bodies, this.body), this.body.position, end);

        if (collisions.length > 0) {
            sensor.length = Matter.Vector.magnitude(Matter.Vector.sub(collisions[0].point, this.body.position));
            sensor.hitting = this.roleMap[collisions[0].body.role || 'wall'];
        } else {
            sensor.length = this.sensorDist;
            sensor.hitting = 0;
        }
    }

    clampVel() {
        Matter.Body.setVelocity(
            this.body,
            {
                x: Matter.Common.clamp(this.body.velocity.x, -this.maxSpeed, this.maxSpeed),
                y: Matter.Common.clamp(this.body.velocity.y, -this.maxSpeed, this.maxSpeed)
            }
        );
    }

    shoot(timestamp) {
        this.lastShot = timestamp;
        var shot = new Shot(
            this.body,
            this.body.angle,
            this.shotSpeed,
            this.shotRange,
            this.engine
        );
    }

    canShoot(timestamp) {
        return (timestamp - this.lastShot) > this.shotCd;
    }
}
