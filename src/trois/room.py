import random
import string
from trois.deck import Deck


class Room():

    def __init__(self, handler):
        self.room_id = ''.join(
            random.choices(string.ascii_letters+string.digits, k=8)
        )
        self.players = {}
        self.deck = Deck()
        self.game_stage = 0  # 0: Not started, 1: Started
        self.active_cards = []
        self.no_matches = set()
        self.end_room = set()

        handler.rooms[self.room_id] = self

    def reset(self):
        self.deck = Deck()
        self.game_stage = 0
        self.active_cards = []
        self.no_matches.clear()
        self.end_room.clear()
        self.players = {
            u_id: {
                'name': val['name'],
                'score': 0
            } for u_id, val in self.players.items()
        }
