import React from 'react';

export default class Card extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let val = this.props.cardData > -1 ? this.props.cardData : -1;
        let bg = ((this.props.cardData > -1) ? { 
            background: `url(../img/shapes.png) no-repeat -${
                (this.props.cardData % 9) * 56}px -${
                Math.floor(this.props.cardData / 9) * 89}px`
        } : {});
        return (
            <div className="card">
                <div style={bg} className={this.props.selected ? "active-card" : ""}
                    onClick={this.props.onClick}>
                </div>
            </div>
        );
    }
}
