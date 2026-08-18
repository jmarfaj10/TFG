const djangoSocket = new WebSocket(window.WS_ROUTE);
const opcImage = document.getElementById('image-selector');
const robotImage = document.getElementById('cam-robot-display');
const robotChatForm = document.getElementById('chat-form');
const robotChatContent = document.getElementById('chat-content');
const robotChatTextField = document.getElementById('chat-field');
const robotChatButton = document.getElementById("chat-button");
const info_position_x = document.getElementById('info-position-x');
const info_position_y = document.getElementById('info-position-y');
const info_position_z = document.getElementById('info-position-z');
const info_orientation_qx = document.getElementById('info-orientation-qx');
const info_orientation_qy = document.getElementById('info-orientation-qy');
const info_orientation_qz = document.getElementById('info-orientation-qz');
const info_goal_x = document.getElementById('info-goal-x');
const info_goal_y = document.getElementById('info-goal-y');
const info_goal_z = document.getElementById('info-goal-z');
const info_goal_tarjet = document.getElementById('info-goal-tarjet');
const info_mission_distance = document.getElementById('info-mission-distance');
const info_mission_x = document.getElementById('info-mission-x');
const info_mission_y = document.getElementById('info-mission-y');
const info_mission_z = document.getElementById('info-mission-z');
const info_mission_time = document.getElementById('info-mission-time');

let canType = true
let pendingAIMessage = null

function createMessage(text, className){
    const div = document.createElement('div');
    div.className = className;
    div.textContent = text;
    robotChatContent.append(div);
    robotChatContent.scrollTop = robotChatContent.scrollHeight;
    return div;
}

const createUserMessage = (text) => createMessage(text, 'rounded bg-primary px-2 py-0.5 w-3/4 self-end');
const createAIMessage = (text) => createMessage(text, 'rounded bg-secondary px-2 py-0.5 w-3/4 self-start');

function setNumber(el, value, decimals = 2){
    if(!el) return;
    const n = Number(value);
    if(value === null || value === undefined || Number.isNaN(n)) return;
    el.textContent = n.toFixed(decimals);
}

function toXYZ(pose){
    if(!pose) return {};
    if(Array.isArray(pose)) return {x: pose[0], y: pose[1], z: pose[2]};
    return pose;
}

djangoSocket.onopen = function(e){
    console.log("Conectado exitosamente al control panel de Django");
}

djangoSocket.onmessage = function(e){
    const parsedData = JSON.parse(e.data);
    const data = parsedData.data;

    if(data.status !== "SUCCESS"){
        console.error("Estado no es SUCCESS", data);
        return;
    }

    if(!data.data) return;

    const type = data.data.type;
    const payload = data.data.data;

    const typeParts = type.split("_");

    if (typeParts[0] === "camera"){
        const img_type = opcImage.checked ? "depth" : "rgb";
        if (typeParts[1] === img_type && payload) {
            robotImage.src = "data:image/jpeg;base64," + payload;
        }
        return;
    }

    switch(type){
        case "position":
            if(payload) updatePosition(payload);
            break;
        case "goal":
            if(payload) updateGoal(payload);
            break;
        case "final":
            if(payload) updateMission(payload);
            break;
        case "vlm_request":
            if(payload) updateChatVLMResponse(payload);
            break;
        default:
            break;
    }
}

djangoSocket.onclose = function(e){
    console.log("Desconectado de Django");
}

djangoSocket.onerror = function(e){
    console.error("Error en Django WebSocket", e);
}

robotChatForm.addEventListener('submit', function(event){
    event.preventDefault();

    if (!canType) return;

    const msg = robotChatTextField.value.trim();
    if (!msg) return;

    const mapa = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
        '/': '&#x2F;'
    };

    const escapeHTML = (str) => str.replace(/[&<>"'/]/g, (char) => mapa[char]);

    const sanitizeMsg = escapeHTML(
        msg
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
    );

    djangoSocket.send(JSON.stringify({action: "vlm_request", params: {prompt: sanitizeMsg}}));

    createUserMessage(msg);
    pendingAIMessage = createAIMessage("...");

    canType = false
    robotChatButton.disabled = true
    robotChatTextField.disabled = true
    robotChatTextField.value = ""
    robotChatTextField.placeholder = "Esperando respuesta del robot..."
})

function unlockChat(){
    canType = true
    robotChatButton.disabled = false
    robotChatTextField.disabled = false
    robotChatTextField.placeholder = ""
}

function updateChatVLMResponse(payload){
    if(pendingAIMessage){
        pendingAIMessage.textContent = payload;
        pendingAIMessage = null;
    } else {
        createAIMessage(payload);
    }
    robotChatContent.scrollTop = robotChatContent.scrollHeight;

    unlockChat();
}

function updatePosition(payload){
    setNumber(info_position_x, payload.x);
    setNumber(info_position_y, payload.y);
    setNumber(info_position_z, payload.z);

    setNumber(info_orientation_qx, payload.qx);
    setNumber(info_orientation_qy, payload.qy);
    setNumber(info_orientation_qz, payload.qz);
}

function updateGoal(payload){
    const pose = toXYZ(payload.goal_pose);

    setNumber(info_goal_x, pose.x);
    setNumber(info_goal_y, pose.y);
    setNumber(info_goal_z, pose.z);

    if(info_goal_tarjet && payload.tarjet) info_goal_tarjet.textContent = payload.tarjet;
}

function updateMission(payload){
    unlockChat();

    const pose = toXYZ(payload.final_pose);

    setNumber(info_mission_distance, payload.distance);
    setNumber(info_mission_x, pose.x);
    setNumber(info_mission_y, pose.y);
    setNumber(info_mission_z, pose.z);

    if(info_mission_time && payload.time !== undefined && payload.time !== null){
        const total = Math.floor(Number(payload.time) / 1000);
        const horas = Math.floor(total / 3600);
        const minutos = Math.floor((total % 3600) / 60);
        const segundos = total % 60;

        const h = horas.toString().padStart(2, '0');
        const m = minutos.toString().padStart(2, '0');
        const s = segundos.toString().padStart(2, '0');

        info_mission_time.textContent = `${h} h ${m} m ${s} s`;
    }
}
