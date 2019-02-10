var Matter = require( "../../node_modules/matter-js");
class Shot {
    constructor(emitter, angle, speed, range, engine) {
        this.engine = engine;
        this.emitter = emitter

        this.start = this.emitter.position;

        this.vel = Matter.Vector.create(1);
        this.vel = Matter.Vector.rotate(this.vel, angle);
        this.vel = Matter.Vector.mult(this.vel, speed);

        this.range = range;

        this.body = Matter.Bodies.polygon(this.start.x, this.start.y, 3, 3, {
            isSensor: true,
            render: {
                strokeStyle: '#ff2222',
                fillStyle: '#ff2222'
            }
        });

        this.body.frictionAir = 0;
        Matter.Body.rotate(this.body, angle + Math.PI);
        Matter.Body.setVelocity(this.body, this.vel);

        this.body.role = 'shot';

        Matter.Events.on(this.engine, 'collisionStart', this.collide.bind(this));
        Matter.Events.on(this.engine, 'beforeUpdate', this.checkRange.bind(this));

        Matter.World.add(this.engine.world, this.body);
    }

    collide(e) {
        for (var i = 0; i < e.pairs.length; i++) {
            var pair = e.pairs[i];
            if (pair.bodyA === this.body && pair.bodyB !== this.emitter) {
                Matter.Events.trigger(this.engine, 'shot:' + pair.bodyB.id, this);
                Matter.World.remove(this.engine.world, this.body);
                Matter.Events.off(this.engine, 'collisionStart', this.collide.bind(this));
            } else if (pair.bodyB === this.body && pair.bodyA !== this.emitter) {
                Matter.Events.trigger(this.engine, 'shot:' + pair.bodyA.id, this);
                Matter.World.remove(this.engine.world, this.body);
                Matter.Events.off(this.engine, 'collisionStart', this.collide.bind(this));
            }
        }
    }

    checkRange() {
        if (Matter.Vector.magnitude(Matter.Vector.sub(this.body.position, this.start)) > this.range) {
            Matter.World.remove(this.engine.world, this.body);
        }
    }
}

module.exports = Shot;