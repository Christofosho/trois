import random
import string
from trois.deck import Deck


class Room():
    def __init__(self, handler):
        self.room_id = ''.join(
            random.choices(string.ascii_letters+string.digits, k=8)
        )
        self.players = {}
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
