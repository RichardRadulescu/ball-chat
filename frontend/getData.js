// getData.js
import { spawnUserBall } from "./physics.js";

let currentUser = null;
const socket = new WebSocket("ws://0.0.0.0:8000/ws");

// Handle Incoming Messages
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Received from Server:", data);

    // If the server sends a "UserJoined" broadcast
    if (data.type=== "success" && data.event=== "JoinRoom") {
        // 1. Add the ball to the physics world
        spawnUserBall();
       
    }
};

export const loadRooms = async (userData) => {
    currentUser = userData; // Store the user passed from main.js
    const roomTemplateBase = await getTemplate('./templates/room.html');
    const resp = await fetch("http://localhost:8000/rooms");
    const rooms = await resp.json();
    
    const aside = document.querySelector("aside");
    aside.innerHTML = "";

    Object.values(rooms).forEach(room => {
        const roomElement = roomTemplateBase.cloneNode(true);
        roomElement.querySelector(".room-info").innerText = `${room.name}`;
        
        roomElement.querySelector(".join-btn").addEventListener("click", () => {
            const payload = {
                "event_type": "JoinRoom",
                "user_id": currentUser.user_id,
                "room_id": room.room_id,
                "datetime": new Date().toISOString()
            };
            socket.send(JSON.stringify(payload));
        });
        aside.appendChild(roomElement);
    });
};

async function getTemplate(url) {
    const resp = await fetch(url);
    const html = await resp.text();
    return new DOMParser().parseFromString(html, 'text/html').querySelector('.room-item');
}