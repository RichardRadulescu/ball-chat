import { initPhysics } from "./physics.js";
import { loadRooms } from "./getData.js";
import { updateWalls } from "./wall.js";

const engine = initPhysics();
const container = document.getElementById('physics-container');
updateWalls(engine, container);

async function initApp() {
    try {
        // 1. Create User
        const userResp = await fetch("http://localhost:8000/users/create");
        const userData = await userResp.json();

        // 2. Load Rooms and pass the user data
        await loadRooms(userData);
    } catch (err) {
        console.error("Initialization failed", err);
    }
}

initApp();