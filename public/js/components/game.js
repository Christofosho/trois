import React from 'react';

import Lobby from './lobby';
import Message from './message';
import Room from './room';

import {socket} from '../index';

export default class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user_id: -1,
            mode: 0,
            message: [
                "Welcome to Trois",
                "The game of shapes and matching three!"
            ],
            room: {}
        };

        this.socketMessageHandler = this.socketMessageHandler.bind(this);
    }

    socketMessageHandler(event) {
        /* Handles responses from the server.
            Names of response types correlate to original
            request sent to the server.
        */
        const data = JSON.parse(event.data);

        if (data.message) {
            this.setState({
                message: data.message
            });
        }

        if (data.response_type == "register") {
            // Prior to joining a room, the user
            // is given an id for updates.
            this.setState({
                user_id: data.user_id
            });
        }

        else if (data.response_type == "join_room") {
            this.setState({
                mode: 1,
                room: data.room
            });
        }

        else if (data.response_type == "start_room") {
            this.setState({
                mode: 2,
                room: data.room
            });
        }

        else if (data.response_type == "send_action") {
            if (data.success) {
                this.setState({
                    room: data.room
                });
            }
        }

        else if (data.response_type == "no_matches") {
            if (data.success) {
                this.setState((state) => ({
                    room: Object.assign(state.room, {
                        'active_cards': data.active_cards
                    })
                }));
            }

            if (data.message) {

            }
        }
        // TODO: end_room
        else if (data.response_type == "end_room") {
            if (data.success) {
                this.setState({
                    mode: 1,
                    room: data.room
                })
            }
        }

        else if (data.response_type == "leave_room") {
            this.setState({
                mode: 0,
                room: {}
            });
        }
    }

    componentDidMount() {
        // Message
        socket.addEventListener('message', this.socketMessageHandler);
    }

    componentWillUnmount() {
        socket.removeEventListener('message', this.socketMessageHandler);
    }

    render() {
        return (
            <div className="game column">
                <Message messages={this.state.message} />
                {this.state.mode >= 1 ?
                    <Room mode={this.state.mode}
                        userId={this.state.user_id}
                        roomId={this.state.room.room_id}
                        players={this.state.room.players}
                        activeCards={this.state.room.active_cards}
                    />
                    : <Lobby userId={this.state.user_id} />}
            </div>
        );
    }
}
