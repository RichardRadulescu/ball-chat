import { updateWalls } from "./wall.js";

// physics.js
const { Engine, Render, Runner, Bodies, Composite } = Matter;
const container = document.getElementById('physics-container');
const engine = Engine.create();

export let render= null

export function initPhysics() {
    render = Render.create({
        element: container,
        engine: engine,
        options: {
            width: container.offsetWidth,
            height: container.offsetHeight,
            wireframes: false,
            background: 'transparent'
        }
    });

    Render.run(render);
    Runner.run(Runner.create(), engine);
    return engine;
}

export function spawnUserBall() {
    const x = Math.random() * (container.clientWidth - 50) + 25;
    const ball = Bodies.circle(x, 50, 20, {
        restitution: 0.8,
        render: { fillStyle: '#e94560' }
    });
    Composite.add(engine.world, ball);
}


export function shuffleUsers() {
     const allBodies = Composite.allBodies(engine.world);
     allBodies.forEach(body => {
        if (!body.isStatic) {
            const forceMagnitude = 50; 
            const velocityX = (Math.random() - 0.5) * forceMagnitude;
            const velocityY = (Math.random() - 0.5) * forceMagnitude;
            Matter.Body.setVelocity(body, { x: velocityX, y: velocityY });
        }
    });
}


window.addEventListener('resize', () => {
    if (!render || !engine) return;

    const container = document.getElementById('physics-container');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    render.canvas.width = width;
    render.canvas.height = height;

    render.options.width = width;
    render.options.height = height;
    
    render.bounds.max.x = width;
    render.bounds.max.y = height;

    updateWalls(engine, container);
});

window.shuffleUsers=shuffleUsers
window.spawnUserBall= spawnUserBall