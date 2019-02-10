import React from 'react';
import ReactDOM from 'react-dom';

let user_id = -1;

(() => {
    const socket = new WebSocket('ws://' + document.domain + ':5000/ws');

    // Open
    socket.addEventListener('open', (event) => {
        const data = {
            type: "register"
        };
        socket.send(JSON.stringify(data));
    });

    // Message
    socket.addEventListener('message', (event) => {
        const data = JSON.parse(event.data);
        if (data.type == "register") {
            // Prior to joining a room, the user
            // is given an id for updates.
            user_id = data.user_id;
            console.log("User ID:", user_id);
        }
        // TODO: join_room
        if (data.type == "join_room") {

        }
        // TODO: start_game
        if (data.type == "start_game") {
            
        }
        // TODO: send_action
        if (data.type == "send_action") {
            
        }
        // TODO: end_game
        if (data.type == "end_game") {
            
        }
        // TODO: leave_game
        if (data.type == "leave_game") {
            
        }
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

    /*
    socket.on('connect', () => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            socket.emit('authentication', JSON.stringify({
              'username': document.getElementById('username').value
            }));
      });
    });
    */

    class Card extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                button: props.buttonName
            }
        }

        render() {
            return (
                <div class="card">
                    <span>{this.state.button}</span>
                </div>
            );
        }
    }

    function Cards(props) {
        return (
            <div id="cards">
                <div class="row justify">
                    <Card buttonName={'Q'} />
                    <Card buttonName={'W'} />
                    <Card buttonName={'E'} />
                    <Card buttonName={'R'} />
                </div>
                <div class="row justify">
                    <Card buttonName={'A'} />
                    <Card buttonName={'S'} />
                    <Card buttonName={'D'} />
                    <Card buttonName={'F'} />
                </div>
                <div class="row justify">
                    <Card buttonName={'Z'} />
                    <Card buttonName={'X'} />
                    <Card buttonName={'C'} />
                    <Card buttonName={'V'} />
                </div>
            </div>
        );
    }

    class Players extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                active: {}
            };
        }

        render() {
            let players = [];
            for (const k in this.state.active) {
                if (this.state.active.hasOwnProperty(k)) {
                    players.push(<Player
                        playerName={this.state.active[k].playerName}
                        playerScore={this.state.active[k].playerScore}
                    />);
                }
            }
            return (
                <aside id="players">
                    {players}
                </aside>
            );
        }
    }

    function Room(props) {
        return (
            <div id="room">
                <Cards />
                <Players />
            </div>
        );
    }

    class Lobby extends React.Component {
        constructor (props) {
            super(props);
        }

        sendNewGame() {
            const data = {
                type: 'new_game',
                user_id: user_id,

            }
            console.log("Sending data:", data);
            socket.send(data);
        };

        render() {
            return (
                <div id="lobby" class="column">
                    <div>
                        <p>Start a new game:</p>
                        <button id="new" onClick={this.sendNewGame}>New</button>
                    </div>
                    <hr/>
                    <div>
                        <label for="join">Join a game:</label>
                        <input id="join" type="textbox" placeholder="Room ID"></input>
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
                mode: 0
            };
        }

        render() {
            let mode = <Lobby />;
            if (this.state.mode == 1) {
                mode = <Room />;
            }
            return (
                <div id="game" class="justify">
                    {mode}
                </div>
            );
        }
    }

    ReactDOM.render(
        <Game />,
        document.querySelector('main')
    );
})();