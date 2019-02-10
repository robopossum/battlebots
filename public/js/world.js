var Matter = require( "../../node_modules/matter-js");
var XP = require("./xp.js");
global.window = {};
class GameWorld {

    constructor(width, height, element) {
        var Engine = Matter.Engine,
            Render = Matter.Render,
            World = Matter.World,
            Events = Matter.Events,
            Bodies = Matter.Bodies;
        
        // create an engine
        this.engine = Engine.create();
        
        this.renderToBrowser = element
        // create a renderer
        // here we need to disable this
        if (element != false) {
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

        }else{
            this.renderToBrowser = element;
        }
        
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

    // dont think this method is necessary for what we are doing
    run() {
        var Engine = Matter.Engine;
            
        // might be worth while add ing all render functions to a seperate flag on the creattion of the world
        if (this.renderToBrowser != false) {
        var Render = Matter.Render;
        Render.run(this.render);
    };
        // run the engine
        Engine.run(this.engine);
        
        // run the renderer
        // need to 
        
        //me and tom
        this.engine.timing.timeScale = 100;

    }


    iterate() {
        var Engine = Matter.Engine;
        Engine.update(this.engine, [delta=50], [correction=1]);
        // we really need to have it return the state of the agent here as that would save effort later
    }


    spawnXp(num) {
        for (let i = 0; i < num; i++) {
            this.xp.push(new XP.XP(Math.floor(Math.random() * this.width), Math.floor(Math.random() * this.height), this.engine));
        }
    }
}


module.exports =  GameWorld;
