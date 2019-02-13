import React from 'react';

import {socket} from '../index';

export default class Controls extends React.Component {
    constructor (props) {
        super(props);

        this.leaveRoom = this.leaveRoom.bind(this);
        this.startRoom = this.startRoom.bind(this);
        this.noMatches = this.noMatches.bind(this);
        this.endRoom = this.endRoom.bind(this);
    }

    leaveRoom(event) {
        socket.send(JSON.stringify({
            message_type: "leave_room",
            user_id: this.props.userId,
            room_id: this.props.roomId
        }));
    }

    startRoom(event) {
        socket.send(JSON.stringify({
            message_type: "start_room",
            user_id: this.props.userId,
            room_id: this.props.roomId
        }))
    }

    noMatches(event) {
        socket.send(JSON.stringify({
            message_type: "no_matches",
            user_id: this.props.userId,
            room_id: this.props.roomId
        }));
    }

    endRoom(event) {
        socket.send(JSON.stringify({
            message_type: "end_room",
            user_id: this.props.userId,
            room_id: this.props.roomId
        }))
    }

    render() {
        return (
            <div className="controls row">
                <button className="leave-room" onClick={this.leaveRoom}>
                    Leave Room
                </button>
                {this.props.mode === 1 ?
                    <button className="start-room" onClick={this.startRoom}>
                        Start Room
                    </button>
                :
                <React.Fragment>
                    <button className="no-matches" onClick={this.noMatches}>
                        No Matches
                    </button>
                    <button className="end-room" onClick={this.endRoom}>
                        End Room
                    </button>
                </React.Fragment>
                }
            </div>
        );
    }
}
