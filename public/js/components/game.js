import React, { useEffect, useState } from 'react';

import Lobby from './lobby';
import Message from './message';
import Room from './room';
import {modes} from './constants';

const INIT_MESSAGE = [
    "Welcome to Trois",
    "The game of shapes and matching three!"
];

export default props => {
    const [userId, setUserId] = useState(-1);
    const [mode, setMode] = useState(modes.HOME);
    const [message, setMessage] = useState(INIT_MESSAGE);
    const [room, setRoom] = useState(null);

    const socketMessageHandler = e => {
        /* Handles responses from the server.
            Names of response types correlate to original
            request sent to the server.
        */
        const data = JSON.parse(e.data);
        if (data.message) {
            setMessage(data.message);
        }
    
        if (data.message_type == "register") {
            // Prior to joining a room, the user
            // is given an id for updates.
            setUserId(data.user_id);
        }
    
        else if (data.message_type == "init_room") {
            if (!data.room.started) {
                setMode(modes.LOBBY);
                setRoom(data.room);
            }
        }
    
        else if (data.message_type == "start_room") {
            if (data.room.started) {
                setMode(modes.PLAYING);
                setRoom(data.room);
            }
        }
    
        else if (data.message_type == "update_room") {
            setRoom(data.room);
        }
    
        else if (data.message_type == "leave_room") {
            setMode(modes.HOME);
            setMessage(INIT_MESSAGE);
            setRoom(null);
        }
    };

    useEffect(() => {
        props.socket.addEventListener('message', socketMessageHandler);
        return () => {
            props.socket.removeEventListener('message', socketMessageHandler);
        };
    });

    return (
        <div className="game">
            <div className="game-top">
                <Message messages={message} />
            </div>
            <div className="game-bottom">
                {mode >= modes.LOBBY ?
                    <Room
                        socket={props.socket}
                        mode={mode}
                        userId={userId}
                        roomId={room.room_id}
                        players={room.players}
                        activeCards={room.active_cards}
                        lastMatch={room.last_match}
                        /* drawCards={draw_cards}
                         endGame={end_game} */
                    />
                    : <Lobby userId={userId} socket={props.socket} />}
            </div>
        </div>
    );
}
