class GameWorld {

    constructor(width, height, element) {
        var Engine = Matter.Engine,
            Render = Matter.Render,
            World = Matter.World,
            Events = Matter.Events,
            Bodies = Matter.Bodies;
        
        // create an engine
        this.engine = Engine.create();
        
        // create a renderer
        this.render = Render.create({
            element: element,
            engine: this.engine,
            options: {
                width: width,
                height: height,
                hasBounds: true,
                wireframes: false,
                showAngleIndicator: true
            }
        });

        this.engine.world.gravity.y = 0;

        World.add(this.engine.world, [
            Bodies.rectangle(width/2, 0, width, 50, { isStatic: true }),
            Bodies.rectangle(width/2, height, width, 50, { isStatic: true }),
            Bodies.rectangle(width, height/2, 50, height, { isStatic: true }),
            Bodies.rectangle(0, height/2, 50, height, { isStatic: true })
        ]);

        this.xp = [];
        this.width = width;
        this.height = height;
    }

    run() {
        var Engine = Matter.Engine,
            Render = Matter.Render;

        // run the engine
        Engine.run(this.engine);
        
        // run the renderer
        Render.run(this.render);
    }

    spawnXp(num) {
        for (let i = 0; i < num; i++) {
            this.xp.push(new XP(Math.floor(Math.random() * this.width), Math.floor(Math.random() * this.height), this.engine));
        }
    }
}
