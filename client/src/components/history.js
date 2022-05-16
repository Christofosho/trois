import React from 'react';

import Card from './card';

export default props => (
    <div className="history">
        <h3 className="history-title">Match History</h3>
        { props.lastMatch.length
            ? <div className="row justify">
                    <Card cardData={props.lastMatch[0]} />
                    <Card cardData={props.lastMatch[1]} />
                    <Card cardData={props.lastMatch[2]} />
                </div>
          : null
        }
    </div>
);