import React from 'react';

import Card from './card';

import {socket} from '../index';

export default class Cards extends React.Component {
    constructor (props) {
        super(props);
        this.state = {
            selected_cards: []
        }
        // this.addSelectedCard = this.addSelectedCard.bind(this);
    }

    addSelectedCard(event, cardValue) {
        event.preventDefault();
        if (this.state.selected_cards.length == 3) {
            return;
        }
        else {
            if (!this.state.selected_cards.includes(cardValue)) {
                this.setState((state) => ({
                    selected_cards: state.selected_cards
                        .concat([cardValue])
                }));
            }
            else {
                this.setState((state) => ({
                    selected_cards:
                        state.selected_cards.filter(x => x !== cardValue)
                }));
            }
        }
    }

    componentDidUpdate(pProps, pState) {
        for (const i in this.state.selected_cards) {
            const card = this.state.selected_cards[i];
            if (!this.props.activeCards.includes(card)) {
                this.setState((state) => ({
                    selected_cards: state.selected_cards.filter(c => c != card)
                }));
            }
        }
        if (pState.selected_cards.length !== this.state.selected_cards.length
            && this.state.selected_cards.length == 3) {
            socket.send(JSON.stringify({
                message_type: "send_action",
                user_id: this.props.userId,
                room_id: this.props.roomId,
                cards: this.state.selected_cards
            }));
            this.setState({
                selected_cards: []
            })
        }
    }

    render() {
        let active = Object.entries(this.props.activeCards).map((val, i) => {
            if (val[1] === null) return;
            return <Card key={i}
                cardData={val[1]}
                onClick={(e) => this.addSelectedCard(e, val[1])}
                selected={this.state.selected_cards
                    .includes(val[1])
                }
            />;
        });

        return (
            <section className="cards row">
                {active}
            </section>
        );
    }
}
