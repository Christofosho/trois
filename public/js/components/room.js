import React from 'react';

import Cards from './cards';
import Controls from './controls';
import History from './history';
import Options from './options';
import Players from './players';

import {modes} from './constants';

export default class Room extends React.Component {
    constructor (props) {
        super(props);
    }

    render() {
        return (
            <div className="room column">
                <div className="scene justify">
                    { this.props.mode >= modes.PLAYING ?
                    <Cards userId={this.props.userId}
                        roomId={this.props.roomId}
                        activeCards={this.props.activeCards} />
                    : <Options/> }
                    <aside className="row">
                        <Players
                            players={this.props.players}
                            userId={this.props.userId} />
                        { this.props.mode >= modes.PLAYING ?
                        <History lastMatch={this.props.lastMatch} />
                        : null
                        }
                    </aside>
                </div>
                <Controls mode={this.props.mode}
                    userId={this.props.userId}
                    roomId={this.props.roomId} />
            </div>
        );
    }
}
