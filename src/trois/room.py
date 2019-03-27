import random
import string
from trois.deck import Deck


class Room():
    def __init__(self, handler):
        self.room_id = ''.join(
            random.choices(string.ascii_letters+string.digits, k=8)
        )
        self.players = {}
        self.options = {
            "GAME_MODE": 0
        }
        self.reset()

        handler.rooms[self.room_id] = self

    def reset(self):
        """ Reset the values in the room. """
        self.deck = Deck()
        self.game_stage = 0
        self.active_cards = []
        self.started = False
        self.start_room = set()
        self.draw_cards = set()
        self.end_room = set()

    def options(self, op):
        pass

    def start(self):
        self.game_stage = 1
        self.active_cards = [
            self.deck.draw()
            for _ in range(12)
        ]
        self.start_room.clear()
        self.draw_cards.clear()
        self.end_room.clear()
        self.started = True
        for user in self.players.values():
            user.score = 0

    def add_user(self, user):
        """ Add a user to the room. """
        self.players[user.user_id] = user

    def get_users(self):
        """ Return the current users active in the room. """
        return {
            user.user_id: {
                'name': user.name,
                'score': user.score
            }
            for user in self.players.values()
        }

    def add_cards(self, amount=3):
        if (len(self.deck) > 0):
            self.active_cards.extend(
                [self.deck.draw() for _ in range(amount)]
            )
            return True
        return False

    def remove_cards(self, cards=None):
        if cards is None:
            cards = []
        self.active_cards = [
            card for card in self.active_cards
            if card[0] not in cards
        ]

    def room_complete(self):
        if (len(self.active_cards) == 0
                and len(self.deck) == 0):
            # Game complete.
            return True
        return False

    def get_public_information(self):
        """ Return a subset of the data in the room
            object to send to the client.
        """
        return {
            'room_id': self.room_id,
            'started': self.started,
            'players': self.get_users(),
            'draw_cards': list(self.draw_cards),
            'end_room': list(self.end_room),
            'active_cards': [
                c[0] for c in self.active_cards
            ]
        }
