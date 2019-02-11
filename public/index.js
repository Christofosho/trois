import React from 'react';
import ReactDOM from 'react-dom';

(() => {
    const socket = new WebSocket('ws://' + document.domain + ':5000/ws');

    // Open
    socket.addEventListener('open', (event) => {
        ReactDOM.render(
            <Game />,
            document.querySelector('main')
        );
        const data = {
            type: "register"
        };
        socket.send(JSON.stringify(data));
    });

    // Error
    socket.addEventListener('error', (event) => {

    });

    // Close
    socket.addEventListener('close', (event) => {

    });

    const main = (ts) => {
        requestAnimationFrame(main);
    };

    class Card extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                cardData: props.cardData
            }
        }

        render() {
            return (
                <div className="card">
                    <span>
                        {this.state.cardData ? this.state.cardData[0]
                            : -1}
                    </span>
                </div>
            );
        }
    }

    class Cards extends React.Component {
        constructor (props) {
            super(props);
            this.state = {
                active_cards: this.props.activeCards
            };
        }

        render() {
            return (
                <div id="cards">
                    <div className="row justify">
                        <Card buttonName={'Q'}
                            cardData={this.state.active_cards[0]} />
                        <Card buttonName={'W'}
                            cardData={this.state.active_cards[1]} />
                        <Card buttonName={'E'}
                            cardData={this.state.active_cards[2]} />
                        <Card buttonName={'R'}
                            cardData={this.state.active_cards[3]} />
                    </div>
                    <div className="row justify">
                        <Card buttonName={'A'}
                            cardData={this.state.active_cards[4]} />
                        <Card buttonName={'S'}
                            cardData={this.state.active_cards[5]} />
                        <Card buttonName={'D'}
                            cardData={this.state.active_cards[6]} />
                        <Card buttonName={'F'}
                            cardData={this.state.active_cards[7]} />
                    </div>
                    <div className="row justify">
                        <Card buttonName={'Z'}
                            cardData={this.state.active_cards[8]} />
                        <Card buttonName={'X'}
                            cardData={this.state.active_cards[9]} />
                        <Card buttonName={'C'}
                            cardData={this.state.active_cards[10]} />
                        <Card buttonName={'V'}
                            cardData={this.state.active_cards[11]} />
                    </div>
                </div>
            );
        }
    }

    class Player extends React.Component {
        constructor(props) {
            super(props);
        }

        render() {
            return (
                <div className="player">
                    <div className="player-name">
                        {this.props.playerName}
                    </div>
                    <div className="player-score">
                        {this.props.playerScore}
                    </div>
                </div>
            );
        }
    }

    class Players extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                active: props.players
            };
        }

        render() {
            let activePlayers = [];
            for (const k in this.state.active) {
                if (this.state.active.hasOwnProperty(k)) {
                    activePlayers.push(<Player key={k}
                        playerName={this.state.active[k]['name']}
                        playerScore={this.state.active[k]['score']} />);
                }
            }
            return (
                <aside className="players">
                    {activePlayers}
                </aside>
            );
        }
    }

    class Controls extends React.Component {
        constructor (props) {
            super(props);

            this.leaveRoom = this.leaveRoom.bind(this);
            this.startRoom = this.startRoom.bind(this);
        }

        leaveRoom(event) {
            socket.send(JSON.stringify({
                type: "leave_room",
                user_id: this.props.userId
            }));
        }

        startRoom(event) {
            socket.send(JSON.stringify({
                type: "start_room",
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
                    <button className="start-room" onClick={this.startRoom}>
                        Start Game
                    </button>
                </div>
            );
        }
    }

    class Room extends React.Component {
        constructor (props) {
            super(props);
            this.state = {
                players: this.props.players,
                active_cards: this.props.activeCards
            }
        }

        render() {
            return (
                <div className="room column">
                    <div className="row">
                        <Cards activeCards={this.state.active_cards} />
                        <Players players={this.state.players} />
                    </div>
                    <div className="row">
                        <Controls userId={this.props.userId}
                                  roomId={this.props.roomId} />
                    </div>
                </div>
            );
        }
    }

    class Lobby extends React.Component {
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
                    <div>
                        <p>Start a new game:</p>
                        <button id="new" onClick={this.sendNewRoom}>
                            New
                        </button>
                    </div>
                    <hr/>
                    <div>
                        <label htmlFor="join">Join a game:</label>
                        <input id="join" type="textbox"
                            placeholder="Room ID"></input>
                        <button id="join">Join</button>
                    </div>
                </div>
            );
        }
    }

    class Game extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                user_id: -1,
                mode: 0,
                room: {}
            };

            this.socketMessageHandler = this.socketMessageHandler.bind(this);
        }

        socketMessageHandler(event) {
            const data = JSON.parse(event.data);
            if (data.type == "register") {
                // Prior to joining a room, the user
                // is given an id for updates.
                this.setState({
                    user_id: data.user_id
                });
            }

            else if (data.type == "join_room") {
                this.setState({
                    mode: 1,
                    room: data.room
                });
            }
            // TODO: start_game
            else if (data.type == "start_room") {
                this.setState({
                    mode: 2,
                    room: data.room
                });
            }
            // TODO: send_action
            else if (data.type == "send_action") {
                
            }
            // TODO: end_game
            else if (data.type == "end_room") {
                
            }
            // TODO: leave_game
            else if (data.type == "leave_room") {
                
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
                <div id="game" className="row justify">
                    {this.state.mode >= 1 ?
                        <Room userId={this.state.user_id}
                              roomId={this.state.room.room_id}
                              players={this.state.room.players}
                              activeCards={this.state.room.active_cards}
                        />
                        : <Lobby userId={this.state.user_id} />}
                </div>
            );
        }
    }
})();