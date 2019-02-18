import React from 'react';

export default class Player extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const is_owner = this.props.isOwner ? "player-name bold" : "player-name";
        return (
            <div className="player row">
                <div className={is_owner}>
                    {this.props.playerName}
                </div>
                <div className="player-score">
                    {this.props.playerScore}
                </div>
            </div>
        );
    }
}
