import React from 'react';
import ReactDOM from 'react-dom';

import Game from './components/game';

const socket = new WebSocket('ws://' + document.domain + ':5000/ws');

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

export {socket};
