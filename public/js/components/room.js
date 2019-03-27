import React from 'react';

import Cards from './cards';
import Controls from './controls';
import Options from './options';
import Players from './players';

export default class Room extends React.Component {
    constructor (props) {
        super(props);
    }

    render() {
        return (
            <div className="room column">
                <div className="scene justify">
                    { this.props.mode >= 2 ?
                    <Cards userId={this.props.userId}
                        roomId={this.props.roomId}
                        activeCards={this.props.activeCards} />
                    : <Options/> }
                    <Players players={this.props.players}
                        userId={this.props.userId} />
                </div>
                <Controls mode={this.props.mode}
                    userId={this.props.userId}
                    roomId={this.props.roomId} />
            </div>
        );
    }
}
