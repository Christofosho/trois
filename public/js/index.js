import React from 'react';
import ReactDOM from 'react-dom';

import Game from './components/game';
const socket = new WebSocket(
    process.env.REACT_APP_SSL_ENABLED == "1"
        ? `wss://${document.domain}/ws`
        : `ws://${document.domain}:8080/ws`
);

let heartbeat = () => {
    if (!socket) return;
    if (socket.readyState !== 1) return;
    socket.send(JSON.stringify({message_type: "heartbeat"}));
    setTimeout(heartbeat, 10000);
};

// Open
socket.addEventListener('open', (event) => {
    ReactDOM.render(
        <Game />,
        document.querySelector('main')
    );
    const data = {
        message_type: "register"
    };
    socket.send(JSON.stringify(data));
    heartbeat();
});

// Error
socket.addEventListener('error', (data) => {
    console.error(data);
});

// Close
socket.addEventListener('close', (data) => {
    console.log(data);
});


let overlay = document.querySelector('.overlay');
let close = document.querySelector('.close');
let instructions_toggle = document.querySelector('.instructions-toggle');
let overlay_toggle = (e) => {
    e.preventDefault();
    overlay.classList.toggle('hide');
};
overlay.addEventListener('click', overlay_toggle);
close.addEventListener('click', overlay_toggle);
instructions_toggle.addEventListener('click', overlay_toggle);

let instructions = document.querySelector('.instructions');
let overlay_ignore = (e) => {
    e.stopPropagation();
};
instructions.addEventListener('click', overlay_ignore);


export {socket};
