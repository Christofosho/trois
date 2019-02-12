import React from 'react';
import ReactDOM from 'react-dom';

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

class Card extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let val = this.props.cardData > -1 ? this.props.cardData : -1;
        let bg = ((this.props.cardData > -1) ? { 
            background: 'url(shapes.png) no-repeat -'
                + ((this.props.cardData % 9) * 56)
                + 'px -'
                + (Math.floor(this.props.cardData / 9) * 89)
                + 'px'
        } : {});
        return (
            <div className="card">
                <div style={bg} className={this.props.selected ? "active-card" : ""}
                    onClick={this.props.onClick}>
                </div>
            </div>
        );
    }
}

class Cards extends React.Component {
    constructor (props) {
        super(props);
        this.state = {
            selected_cards: []
        }
        // this.addSelectedCard = this.addSelectedCard.bind(this);
    }

    addSelectedCard(event, cardValue) {
        event.preventDefault();
        if (this.state.selected_cards.length == 3) {
            return;
        }
        else {
            this.setState((state) => ({
                selected_cards: state.selected_cards
                    .concat([cardValue])
            }));
        }
    }

    componentDidUpdate(pProps, pState) {
        if (pState.selected_cards.length !== this.state.selected_cards.length
            && this.state.selected_cards.length == 3) {
            socket.send(JSON.stringify({
                type: "send_action",
                user_id: this.props.userId,
                room_id: this.props.roomId,
                cards: this.state.selected_cards
            }));
            this.setState({
                selected_cards: []
            })
        }
    }

    render() {
        let active = Object.entries(this.props.activeCards).map((val, i) => {
            if (val[1] === null) return;
            return <Card key={i}
                cardData={val[1]}
                onClick={(e) => this.addSelectedCard(e, val[1])}
                selected={this.state.selected_cards
                    .includes(val[1])
                }
            />;
        });

        return (
            <div className="cards row">
                {active}
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
            <div className="player row">
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
        let activePlayers = Object.entries(this.state.active).map((val, i) => {
            return <Player key={i}
                playerName={val[1]['name']}
                playerScore={val[1]['score']} />;
        });
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
        this.noMatches = this.noMatches.bind(this);
    }

    leaveRoom(event) {
        socket.send(JSON.stringify({
            type: "leave_room",
            user_id: this.props.userId,
            room_id: this.props.roomId
        }));
    }

    startRoom(event) {
        socket.send(JSON.stringify({
            type: "start_room",
            user_id: this.props.userId,
            room_id: this.props.roomId
        }))
    }

    noMatches(event) {
        socket.send(JSON.stringify({
            type: "no_matches",
            user_id: this.props.userId,
            room_id: this.props.roomId
        }));
    }

    render() {
        return (
            <div className="controls row">
                <button className="leave-room" onClick={this.leaveRoom}>
                    Leave Room
                </button>
                {this.props.mode === 1 ?
                    <button className="start-room" onClick={this.startRoom}>
                        Start Game
                    </button>
                    : <button className="no-matches" onClick={this.noMatches}>
                        No Matches
                    </button>
                }
            </div>
        );
    }
}

class Room extends React.Component {
    constructor (props) {
        super(props);
    }

    render() {
        return (
            <div className="room column">
                <div className="row justify">
                    <Cards userId={this.props.userId}
                        roomId={this.props.roomId}
                        activeCards={this.props.activeCards} />
                    <Players players={this.props.players} />
                </div>
                <Controls mode={this.props.mode}
                    userId={this.props.userId}
                    roomId={this.props.roomId} />
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
        /* Handles responses from the server.
            Names of response types correlate to original
            request sent to the server.
        */
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

        else if (data.type == "start_room") {
            this.setState({
                mode: 2,
                room: data.room
            });
        }

        else if (data.type == "send_action") {
            if (data.success) {
                this.setState({
                    room: data.room
                });
            }
        }
        // TODO: end_room
        else if (data.type == "end_room") {
            
        }

        else if (data.type == "leave_room") {
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
            <div className="game row justify">
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
