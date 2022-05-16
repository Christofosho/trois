import React from 'react';

import Cards from './cards';
import Controls from './controls';
import History from './history';
import Options from './options';
import Players from './players';

import {modes} from './constants';

export default props => (
    <div className="room column">
        <div className="scene justify">
            { props.mode >= modes.PLAYING ?
            <Cards
                socket={props.socket}
                userId={props.userId}
                roomId={props.roomId}
                activeCards={props.activeCards} />
            : <Options/> }
            <aside className="row">
                <Players
                    players={props.players}
                    userId={props.userId} />
                { props.mode >= modes.PLAYING ?
                <History lastMatch={props.lastMatch} />
                : null
                }
            </aside>
        </div>
        <Controls
            socket={props.socket}
            mode={props.mode}
            userId={props.userId}
            roomId={props.roomId} />
    </div>
);
