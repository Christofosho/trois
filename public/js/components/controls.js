import React from 'react';

import {modes} from './constants';

export default props => {
    const leaveRoom = e => {
        props.socket.send(JSON.stringify({
            message_type: "leave_room",
            user_id: props.userId,
            room_id: props.roomId
        }));
    }

    const startRoom = e => {
        props.socket.send(JSON.stringify({
            message_type: "start_room",
            user_id: props.userId,
            room_id: props.roomId
        }))
    }

    const drawCards = e => {
        props.socket.send(JSON.stringify({
            message_type: "draw_cards",
            user_id: props.userId,
            room_id: props.roomId
        }));
    }

    const endRoom = e => {
        props.socket.send(JSON.stringify({
            message_type: "end_room",
            user_id: props.userId,
            room_id: props.roomId
        }))
    }

    return (
        <section className="controls row">
            <button className="leave-room" onClick={leaveRoom}>
                Leave
            </button>
            {props.mode === modes.LOBBY ?
                <button className="start-room" onClick={startRoom}>
                    Start
                </button>
            :
            <React.Fragment>
                <button className="draw-cards" onClick={drawCards}>
                    Draw 3
                </button>
                <button className="end-room" onClick={endRoom}>
                    End
                </button>
            </React.Fragment>
            }
        </section>
    );
}
