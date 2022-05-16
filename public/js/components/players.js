import React from 'react';

import Player from './player';

export default props => (
    <section className="players">
        <h3 className="players-title">Players</h3>
        {Object.entries(props.players).map((val, i) => {
            return <Player key={i}
                playerName={val[1]['name']}
                playerScore={val[1]['score']}
                isOwner={val[0] === props.userId}
            />;
        })}
    </section>
);
