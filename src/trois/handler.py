import random
import string
import uuid
from trois.deck import Deck
from trois.validator import Validator


class Handler():
    def __init__(self):
        """ Create two dicts:

            self.rooms: Contains a reference to each active room.
            self.users: Contains a reference to each active user.
        """
        self.rooms = {}
        self.users = {}

        self.validator = Validator(self)

    def distribute(self, client, payload):
        """ Distribute the payload to the correct handler function
            by determining the type of action the payload is requesting.

            client: socket object
            payload: dict of information including a type
        """
        message_type = payload.get("type", None)
        user_id = payload.get("user_id", None)
        valid_message = self.validator.validate_message_type(message_type)
        if not valid_message:
            # TODO: Handle error.
            print("Invalid message: {}".format(message_type))
            return

        if message_type == "register":
            # Register a user in the system.
            return self.register_user(client)

        # All other routes assume the user is authenticated.
        valid_user = self.validator.validate_user_id(user_id)
        if not valid_user:
            # TODO: Handle error.
            print("Invalid user: {}".format(user_id))
            return

        if message_type == "unregister":
            # Remove a user from the handler.
            self.remove_user(user_id)
            # TODO: Update all.
            return

        elif message_type == "new_room":
            # Create a new room and add the user to it.
            print("Creating a new room with user: {}".format(user_id))
            return {
                "type": "join_room",
                "room": self.add_room(user_id)
            }

        # All other routes assume the room exists.
        room_id = payload.get("room_id", None)
        valid_room = self.validator.validate_room_id(room_id)
        if not valid_room:
            # TODO: Handle error.
            print("Invalid room_id for user: {}".format(user_id))
            return

        # TODO: join_room
        if message_type == "join_room":
            pass

        elif message_type == "start_room":
            return self.start_room(user_id, room_id)

        # TODO: send_action
        elif message_type == "send_action":
            cards = payload.get("cards", None)
            valid_cards = self.validator.validate_cards(room_id, cards)
            if valid_cards:
                return self.handle_action(user_id, room_id, cards)

        elif message_type == "no_matches":
            pass

        # TODO: end_room
        elif message_type == "end_room":
            return self.end_room(room_id)

        # TODO: leave_room
        elif message_type == "leave_room":
            return self.leave_room(user_id)

    def register_user(self, client):
        return {
            "type": "register",
            "user_id": self.add_user(client)
        }

    def add_user(self, client):
        """ Add a user to the user dict and return the id.

            client: socket object
        """
        user_id = str(uuid.uuid4())
        client.user_id = user_id

        print("Adding user: {}".format(user_id))

        # Set to None until a room is assigned.
        self.users[user_id] = {
            'room_id': None
        }
        return user_id

    def remove_user(self, user_id):
        """ Remove a user from the user dict.

            user_id: uuid
        """
        room_id = None
        if user_id in self.users:
            room_id = self.users[user_id]
            del self.users[user_id]

        if room_id and room_id in self.rooms:
            room = self.rooms[room_id]
            if user_id in room['players']:
                room['players'].pop(
                    room['players'].index(user_id)
                )

            if len(room['players']) < 1:
                self.remove_room(room_id)

    def add_room(self, owner_id):
        """ Add a new room to the self.rooms dict
            and generate a room_id for sharing.
            Return the room information generated.

            owner_id: uuid
        """
        if owner_id not in self.users:
            # TODO: Handle error.
            return

        room_id = str(uuid.uuid4())
        room = {
            'room_id': room_id,
            'players': {},
            'deck': Deck(),
            'game_stage': 0,  # 0: Not started, 1: Started
            'active_cards': [None]*12
        }
        self.rooms[room_id] = room

        if not self.add_user_to_room(owner_id, room_id):
            # TODO: Handle failure to add player.
            return

        return {
            'room_id': room['room_id'],
            'players': room['players'],
            'active_cards': room['active_cards']
        }

    def remove_room(self, room_id):
        """ Remove an empty room.

            room_id: string of random characters
        """
        if room_id in self.rooms:
            del self.rooms[room_id]

    def add_user_to_room(self, user_id, room_id):
        """ Add a user to a room, if they can join.

            user_id: uuid
            room_id: string of random characters
        """
        if not self.can_join_room(user_id, room_id):
            return False

        for room in self.rooms.values():
            if user_id in room['players']:
                self.remove_user_from_room(user_id, room_id)

        active_players = len(self.rooms[room_id]['players'])
        fake_name = "Player 1"
        if active_players == 1:
            fake_name = "Player 2"

        elif active_players == 2:
            fake_name = "Player 3"

        elif active_players == 3:
            fake_name = "Player 4"

        elif active_players > 3:
            return False

        self.rooms[room_id]['players'][user_id] = {
            'name': fake_name,
            'score': 0
        }
        self.users[user_id]['room_id'] = room_id

        return True

    def remove_user_from_room(self, user_id, room_id):
        """ Remove a user from a room.

            user_id: uuid
            room_id: string of random characters
        """
        del self.rooms[room_id]['players'][user_id]

    def can_join_room(self, user_id, room_id):
        """ Return a boolean after checking
            whether a user can join a room.

            user_id: uuid
            room_id: string of random characters
        """
        room = self.rooms[room_id]

        if room['game_stage'] != 0:
            # Game is started.
            return False

        if len(room['players']) >= 4:
            # Max players hit (4)
            return False

        return True

    def start_room(self, user_id, room_id):
        """ Initialize game parameters and draw
            the first set of active cards.

            user_id: uuid
            room_id: string of random characters
        """
        self.rooms[room_id]['game_stage'] = 1
        self.rooms[room_id]['active_cards'] = [
            self.rooms[room_id]['deck'].draw()
            for _ in range(12)
        ]

        return {
            "type": "start_room",
            "room": {
                'room_id': room_id,
                'players': self.rooms[room_id]['players'],
                'active_cards': [
                    c[0] for c in self.rooms[room_id]['active_cards']
                ]
            }
        }

    def leave_room(self, user_id):
        """ Remove user from room.

            user_id: uuid
        """
        room_id = self.users[user_id]['room_id']
        self.remove_user_from_room(user_id, room_id)
        # TODO: Update other users.
        return {
            "type": "leave_room"
        }

    def handle_action(self, user_id, room_id, cards):
        # Get card definitions
        card_defs = [
            card for card in self.rooms[room_id]['active_cards']
            if card[0] in cards
        ]
        success = self.check_cards(card_defs)
        if success:
            # Give the player a point
            self.rooms[room_id]['players'][user_id]['score'] += 1

            # Remove the three cards picked
            active_cards = [
                card for card in self.rooms[room_id]['active_cards']
                if card[0] not in cards
            ]

            # Draw three more cards
            active_cards.extend(
                [self.rooms[room_id]['deck'].draw() for _ in range(3)]
            )

        return {
            "type": "send_action",
            "success": success,
            "room": {
                'room_id': room_id,
                'players': self.rooms[room_id]['players'],
                'active_cards': [
                    c[0] for c in self.rooms[room_id]['active_cards']
                ]
            }
        }

    def check_cards(self, cards):
        # Match cards
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
        e1 = card1[element]
        e2 = card2[element]
        e3 = card3[element]
        if (e1 == e2 and e2 == e3) or (e1 != e2 and e1 != e3 and e2 != e3):
            # All the same or all different
            return 1
        return 0
