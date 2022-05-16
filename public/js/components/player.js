import React from 'react';

export default props => (
    <div className="player row">
        <div className={props.isOwner ? "player-name bold" : "player-name"}>
            {props.playerName}
        </div>
        <div className="player-score">
            {props.playerScore}
        </div>
    </div>
);