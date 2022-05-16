import React from 'react';
import { createRoot } from 'react-dom/client';

export default Base => {
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

    // Error
    socket.addEventListener('error', (data) => {
        console.error(data);
    });

    // Close
    socket.addEventListener('close', (data) => {
        console.log(data);
    });

    // Open
    socket.addEventListener('open', () => {
        createRoot(
            document.querySelector('main')
        ).render(
            <Base socket={socket} />
        );
        const data = {
            message_type: "register"
        };
        socket.send(JSON.stringify(data));
        heartbeat();
    });

  return socket;
}