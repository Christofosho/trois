import React from 'react';

import Player from './player';

export default class Players extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let activePlayers = Object.entries(this.props.players).map((val, i) => {
            return <Player key={i}
                playerName={val[1]['name']}
                playerScore={val[1]['score']} />;
        });
        return (
            <aside className="players">
                <h3 className="players-title">Players</h3>
                {activePlayers}
            </aside>
        );
    }
}
