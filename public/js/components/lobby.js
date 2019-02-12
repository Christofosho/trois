import React from 'react';

import {socket} from '../index';

export default class Lobby extends React.Component {
    constructor (props) {
        super(props);
        this.sendNewRoom = this.sendNewRoom.bind(this);
    }

    sendNewRoom(e) {
        const data = {
            type: 'new_room',
            user_id: this.props.userId,
        }
        socket.send(JSON.stringify(data));
    };

    render() {
        return (
            <div id="lobby" className="column">
                <div className="row">
                    <p>Start a new room:</p>
                    <button className="new-room" onClick={this.sendNewRoom}>
                        New
                    </button>
                </div>
                <hr/>
                <div>
                    <label htmlFor="join">Join a room:</label>
                    <input id="join" className="join-room-input"
                        type="textbox" placeholder="Room ID"></input>
                    <button className="join-room-button">Join</button>
                </div>
            </div>
        );
    }
}
