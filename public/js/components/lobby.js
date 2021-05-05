import React from 'react';

import {socket} from '../index';

export default class Lobby extends React.Component {
    constructor (props) {
        super(props);
        this.newRoom = this.newRoom.bind(this);
        this.joinRoom = this.joinRoom.bind(this);
    }

    newRoom(e) {
        socket.send(JSON.stringify({
            message_type: 'new_room',
            user_id: this.props.userId,
        }));
    }

    joinRoom(e) {
        const val = document.querySelector('.join-room-input').value;
        if (val.length == 8) {
            socket.send(JSON.stringify({
                message_type: 'join_room',
                user_id: this.props.userId,
                room_id: val
            }));
        }
    }

    render() {
        return (
            <div className="lobby row flex-center justify">
                <div className="column">
                    <input id="join" className="join-room-input"
                        type="textbox" placeholder="Room ID"></input>
                    <button className="join-room-button" onClick={this.joinRoom}>Join Room</button>
                </div>
                <div>OR</div>
                <div>
                    <button className="new-room" onClick={this.newRoom}>
                        New Room
                    </button>
                </div>
            </div>
        );
    }
}
