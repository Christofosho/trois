import React from 'react';

import {socket} from '../index';

export default class Lobby extends React.Component {
    constructor (props) {
        super(props);
        this.sendNewRoom = this.sendNewRoom.bind(this);
    }

    sendNewRoom(e) {
        const data = {
            message_type: 'new_room',
            user_id: this.props.userId,
        }
        socket.send(JSON.stringify(data));
    };

    render() {
        return (
            <div className="lobby column">
                <div className="center">
                    <button className="new-room" onClick={this.sendNewRoom}>
                        New Room
                    </button>
                </div>
                <hr/>
                <div className="column">
                    <input id="join" className="join-room-input"
                        type="textbox" placeholder="Room ID"></input>
                    <button className="join-room-button">Join Room</button>
                </div>
            </div>
        );
    }
}
