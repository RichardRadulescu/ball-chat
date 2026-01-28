const { Bodies, Composite } = Matter;

let walls = {};

export function updateWalls(engine, container, wallThickness = 60) {
    const width = container.clientWidth;
    const height = container.clientHeight;

    const wallData = {
        ground:  { x: width / 2, y: height + wallThickness / 2, w: width, h: wallThickness },
        ceiling: { x: width / 2, y: -wallThickness / 2, w: width, h: wallThickness },
        left:    { x: -wallThickness / 2, y: height / 2, w: wallThickness, h: height },
        right:   { x: width + wallThickness / 2, y: height / 2, w: wallThickness, h: height }
    };

    if (!walls.ground) {
        // First time setup: Create the bodies
        walls.ground = Bodies.rectangle(wallData.ground.x, wallData.ground.y, wallData.ground.w, wallData.ground.h, { isStatic: true, render: { fillStyle: 'gray' } });
        walls.ceiling = Bodies.rectangle(wallData.ceiling.x, wallData.ceiling.y, wallData.ceiling.w, wallData.ceiling.h, { isStatic: true, render: { fillStyle: 'gray' } });
        walls.left = Bodies.rectangle(wallData.left.x, wallData.left.y, wallData.left.w, wallData.left.h, { isStatic: true, render: { fillStyle: 'gray' } });
        walls.right = Bodies.rectangle(wallData.right.x, wallData.right.y, wallData.right.w, wallData.right.h, { isStatic: true, render: { fillStyle: 'gray' } });
        
        Composite.add(engine.world, [walls.ground, walls.ceiling, walls.left, walls.right]);
    } else {
        const currentGroundWidth = walls.ground.bounds.max.x - walls.ground.bounds.min.x;
        const currentLeftHeight = walls.left.bounds.max.y - walls.left.bounds.min.y;

        const scaleX = width / currentGroundWidth;
        const scaleY = height / currentLeftHeight;

        // 2. Scale the walls to match the new container size
        // Ground/Ceiling scale horizontally
        Matter.Body.scale(walls.ground, scaleX, 1);
        Matter.Body.scale(walls.ceiling, scaleX, 1);
        
        // Left/Right scale vertically
        Matter.Body.scale(walls.left, 1, scaleY);
        Matter.Body.scale(walls.right, 1, scaleY);

        // 3. NOW reposition them to the new centers
        Matter.Body.setPosition(walls.ground, { x: width / 2, y: height + wallThickness / 2 });
        Matter.Body.setPosition(walls.ceiling, { x: width / 2, y: -wallThickness / 2 });
        Matter.Body.setPosition(walls.left, { x: -wallThickness / 2, y: height / 2 });
        Matter.Body.setPosition(walls.right, { x: width + wallThickness / 2, y: height / 2 });
    }
}
