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
