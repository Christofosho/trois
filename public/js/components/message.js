import React from 'react';

export default props => (
    <div className="messages centered">
        {Object.entries(props.messages).map((val, i) => {
            if (i === 0) {
                return <h2 key={i} className="message">{val[1]}</h2>
            }
            return <div key={i} className="message">
                {val[1]}
            </div>
        })}
    </div>
);