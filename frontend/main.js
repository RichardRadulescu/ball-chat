import { updateWalls } from "./wall.js";

// Matter.js Setup
const { Engine, Render, Runner, Bodies, Composite } = Matter;

const container = document.getElementById('physics-container');
const engine = Engine.create();
const render = Render.create({
    element: container,
    engine: engine,
    options: {
        width: container.offsetWidth,
        height: container.offsetHeight,
        wireframes: false,
        background: 'transparent'
    }
});

updateWalls(engine, container);
Render.run(render);
const runner = Runner.create();
Runner.run(runner, engine);

// Logic to add a "User" ball
let userCount = 0;
export function addUser() {
    userCount++;
    document.getElementById('user-count').innerText = userCount;

    const x = Math.random() * (container.clientWidth - 50) + 25;
    const ball = Bodies.circle(x, 50, 20, {
        restitution: 0.8, // Bounciness
        friction: 0.05,
        render: {
            fillStyle: ['#e94560', '#00d2ff', '#9d50bb', '#6e48aa'][Math.floor(Math.random() * 4)]
        }
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


window.addUser = addUser;
window.shuffleUsers = shuffleUsers;