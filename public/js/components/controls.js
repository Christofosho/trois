import React from 'react';

import {socket} from '../index';

import {modes} from './constants';

export default class Controls extends React.Component {
    constructor (props) {
        super(props);

        this.leaveRoom = this.leaveRoom.bind(this);
        this.startRoom = this.startRoom.bind(this);
        this.drawCards = this.drawCards.bind(this);
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

    drawCards(event) {
        socket.send(JSON.stringify({
            message_type: "draw_cards",
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
            <section className="controls row">
                <button className="leave-room" onClick={this.leaveRoom}>
                    Leave
                </button>
                {this.props.mode === modes.LOBBY ?
                    <button className="start-room" onClick={this.startRoom}>
                        Start
                    </button>
                :
                <React.Fragment>
                    <button className="draw-cards" onClick={this.drawCards}>
                        Draw 3
                    </button>
                    <button className="end-room" onClick={this.endRoom}>
                        End
                    </button>
                </React.Fragment>
                }
            </section>
        );
    }
}
