import React from 'react';

export default class Player extends React.Component {
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
