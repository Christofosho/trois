import React from 'react';

export default class Message extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let messages = Object.entries(this.props.messages).map((val, i) => {
            if (i === 0) {
                return <h2 className="message">{val[1]}</h2>
            }
            return <div className="message">
                {val[1]}
            </div>
        });
        return (
            <div className="messages centered">
                {messages}
            </div>
        );
    }
}