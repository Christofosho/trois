import React from 'react';

import Card from './card';

export default class History extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
          <div className="history">
            <h3 className="history-title">Match History</h3>
            { this.props.lastMatch.length
              ? <div className="row justify">
                  <Card cardData={this.props.lastMatch[0]} />
                  <Card cardData={this.props.lastMatch[1]} />
                  <Card cardData={this.props.lastMatch[2]} />
                </div>
              : null
            }
          </div>
        );
    }
}