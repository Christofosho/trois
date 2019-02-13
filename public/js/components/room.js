import React from 'react';

import Cards from './cards';
import Controls from './controls';
import Players from './players';

export default class Room extends React.Component {
    constructor (props) {
        super(props);
    }

    render() {
        return (
            <div className="room column">
                <div className="row justify">
                    { this.props.mode >= 2 ?
                    <Cards userId={this.props.userId}
                        roomId={this.props.roomId}
                        activeCards={this.props.activeCards} />
                    : null }
                    <Players players={this.props.players} />
                </div>
                <Controls mode={this.props.mode}
                    userId={this.props.userId}
                    roomId={this.props.roomId} />
            </div>
        );
    }
}
