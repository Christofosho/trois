import React from 'react';

export default props => {
    const newRoom = e => {
        props.socket.send(JSON.stringify({
            message_type: 'new_room',
            user_id: props.userId,
        }));
    };

    const joinRoom = e => {
        const val = document.querySelector('.join-room-input').value;
        if (val.length == 8) {
            props.socket.send(JSON.stringify({
                message_type: 'join_room',
                user_id: props.userId,
                room_id: val
            }));
        }
    };

    return (
        <div className="lobby row flex-center justify">
            <div className="column">
                <input id="join" className="join-room-input"
                    type="textbox" placeholder="Room ID"></input>
                <button className="join-room-button" onClick={joinRoom}>Join Room</button>
            </div>
            <div>OR</div>
            <div>
                <button className="new-room" onClick={newRoom}>
                    New Room
                </button>
            </div>
        </div>
    );
}
