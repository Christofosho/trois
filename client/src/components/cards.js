import React, { useEffect, useState } from 'react';

import Card from './card';

export default props => {

    const [selectedCards, setSelectedCards] = useState([]);

    const addSelectedCard = (e, cardValue) => {
        e.preventDefault();
        if (selectedCards.length == 3) {
            return;
        }
        else {
            if (!selectedCards.includes(cardValue)) {
                setSelectedCards(selectedCards.concat([cardValue]));
            }
            else {
                setSelectedCards(selectedCards.filter(x => x !== cardValue));
            }
        }
    };

    // Check props against state each update
    useEffect(() => {
        for (const card of selectedCards) {
            if (!props.activeCards.includes(card)) {
                setSelectedCards(selectedCards.filter(c => c != card));
            }
        }
    });

    // Only check state against itself if it has changed.
    useEffect(() => {
        if (selectedCards.length == 3) {
            props.socket.send(JSON.stringify({
                message_type: "send_action",
                user_id: props.userId,
                room_id: props.roomId,
                cards: selectedCards
            }));
            setSelectedCards([]);
        }
    }, [selectedCards]);

    return (
        <section className="cards row">
            {Object.entries(props.activeCards).map((val, i) => {
                if (val[1] === null) return;
                return <Card key={i}
                    cardData={val[1]}
                    onClick={(e) => addSelectedCard(e, val[1])}
                    selected={selectedCards.includes(val[1])}
                />;
            })}
        </section>
    );
}
