class XP {
    constructor(x, y, engine) {
        this.engine = engine;
        this.size = 5;
        this.body = Matter.Bodies.circle(x, y, this.size, {
            isSensor: true,
            render: {
                strokeStyle: '#2222ff',
                fillStyle: '#2222ff',
                lineWidth: 1
            }
        });

        Matter.Events.on(this.engine, 'collisionStart', this.collide.bind(this));

        Matter.World.add(engine.world, [this.body]);
    }

    collide(e) {
        for (var i = 0; i < e.pairs.length; i++) {
            var pair = e.pairs[i];
            if (pair.bodyA === this.body) {
                Matter.Events.trigger(this.engine, 'xp:' + pair.bodyB.id, this);
            } else if (pair.bodyB === this.body) {
                Matter.Events.trigger(this.engine, 'xp:' + pair.bodyA.id, this);
            }
        }
    }
}
