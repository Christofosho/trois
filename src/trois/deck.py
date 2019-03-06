import random


class Deck():
    size = 81
    cards = [
        {
            'shape': shape,
            'count': count,
            'colour': colour,
            'fill': fill
        }
        for fill in range(3)
        for count in range(3)
        for colour in range(3)
        for shape in range(3)
    ]

    def __init__(self):
        self.current = list(zip(
            list(range(len(self.cards))),
            list(self.cards)
        ))
        random.shuffle(self.current)

    def __len__(self):
        return len(self.current)

    def draw(self):
        """ Return a card from the current deck. """
        return self.current.pop() if len(self.current) > 0 else None

    def check_cards(self, cards):
        """ Compare the cards passed in to
            determine whether they meet the
            matching criteria.
        """
        if len(cards) != 3:
            return False

        match = 0
        card1 = cards[0][1]
        card2 = cards[1][1]
        card3 = cards[2][1]

        match += self.compare_element(card1, card2, card3, 'shape')
        match += self.compare_element(card1, card2, card3, 'colour')
        match += self.compare_element(card1, card2, card3, 'count')
        match += self.compare_element(card1, card2, card3, 'fill')

        return match == 4

    def compare_element(self, card1, card2, card3, element):
        """ Compare one element of three cards to determine
            if they are all the same, or all different.
        """
        e1 = card1[element]
        e2 = card2[element]
        e3 = card3[element]
        if (e1 == e2 and e2 == e3) or (e1 != e2 and e1 != e3 and e2 != e3):
            # All the same or all different.
            return 1
        return 0
