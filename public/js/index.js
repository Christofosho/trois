import React from 'react';
import ReactDOM from 'react-dom';

import Game from './components/game';
const socket = new WebSocket(
    (process.env.SSL_ENABLED === "1" ? 'wss://' : 'ws://')
    + document.domain + '/ws'
);

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
});

// Error
socket.addEventListener('error', (event) => {

});

// Close
socket.addEventListener('close', (event) => {

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
