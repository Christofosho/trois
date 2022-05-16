import React from 'react';

export default props => (
    <div className="card">
        <div
            style={(props.cardData > -1) ? { 
                background: `url(../img/shapes.webp) no-repeat -${
                    (props.cardData % 9) * 56}px -${
                    Math.floor(props.cardData / 9) * 89}px`
                } : {}
            }
            className={props.selected ? "active-card" : ""}
            onClick={props.onClick}
            title={props.cardData > -1 ? props.cardData : -1}>
        </div>
    </div>
);