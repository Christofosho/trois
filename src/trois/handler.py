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
        message_type = payload.get('message_type', None)
        user_id = payload.get('user_id', None)
        valid_message = self.validator.validate_message_type(message_type)
        if not valid_message:
            print("Invalid message: {}".format(message_type))
            return {
                'response_type': "error",
                'message': [
                    "Invalid Action",
                    "You have attempted to perform an invalid action.",
                    "Contact _ if you need assistance."
                ]
            }

        if message_type == "register":
            # Register a user in the system.
            return self.register_user(client)

        # All other routes assume the user is authenticated.
        valid_user = self.validator.validate_user_id(user_id)
        if not valid_user:
            print("Invalid user: {}".format(user_id))
            return {
                'response_type': "error",
                'message': [
                    "Invalid User ID",
                    "Oops! Looks like your User ID is not showing up in our system.",
                    "Reload the page to fix the problem."
                ]
            }

        if message_type == "unregister":
            # Remove a user from the handler.
            self.remove_user(user_id)
            # TODO: Update all.
            return

        elif message_type == "new_room":
            # Create a new room and add the user to it.
            print("Creating a new room with user: {}".format(user_id))
            return self.add_room(user_id)

        # All other routes assume the room exists.
        room_id = payload.get('room_id', None)
        valid_room = self.validator.validate_room_id(room_id)
        if not valid_room:
            print("Invalid room_id for user: {}".format(user_id))
            return {
                'response_type': "error",
                'message': [
                    "Invalid Room ID",
                    "Please verify the ID you have used and try again."
                ]
            }

        # TODO: join_room
        if message_type == "join_room":
            # Player joins room if game has not begun.
            pass

        elif message_type == "start_room":
            # Start the game.
            return self.start_room(user_id, room_id)

        elif message_type == "send_action":
            # Check the user submitted cards to see if
            # they are a match.
            cards = payload.get('cards', None)
            valid_cards = self.validator.validate_cards(room_id, cards)
            if valid_cards:
                return self.handle_action(user_id, room_id, cards)

        elif message_type == "no_matches":
            return self.add_no_matches(user_id, room_id)

        elif message_type == "end_room":
            return self.end_room(room_id, user_id=user_id)

        elif message_type == "leave_room":
            return self.leave_room(user_id)

    def register_user(self, client):
        return {
            'response_type': "register",
            'user_id': self.add_user(client)
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
        """ Remove a user from the user dict. """
        room_id = None
        if user_id in self.users:
            room_id = self.users[user_id]['room_id']
            del self.users[user_id]

        if room_id and room_id in self.rooms:
            room = self.rooms[room_id]
            if user_id in room['players']:
                del room['players'][user_id]

            if len(room['players']) < 1:
                self.remove_room(room_id)

    def add_room(self, owner_id):
        """ Add a new room to the self.rooms dict
            and generate a room_id for sharing.
            Return the room information generated.
        """
        room_id = ''.join(
            random.choices(string.ascii_letters+string.digits, k=8)
        )
        room = {
            'room_id': room_id,
            'players': {},
            'deck': Deck(),
            'game_stage': 0,  # 0: Not started, 1: Started
            'active_cards': [None]*12,
            'no_matches': set(),
            'end_room': set()
        }
        self.rooms[room_id] = room

        user_added = self.add_user_to_room(owner_id, room_id)
        if user_added['response_type'] != "success":
            return {
                'response_type': "error",
                'message': [
                    "Join Failed",
                    "Your attempt to join the room with ID {} has failed."
                    .format(room_id),
                    "Please check the ID and try again."
                ]
            }

        return {
            'response_type': "join_room",
            'room': {
                'room_id': room['room_id'],
                'players': room['players'],
                'active_cards': room['active_cards']
            },
            'message': [
                "New Room",
                "You have created a new room.",
                "Your Room ID is: {}".format(room['room_id'])
            ]
        }

    def remove_room(self, room_id):
        """ Remove an empty room. """
        if room_id in self.rooms:
            del self.rooms[room_id]

    def add_user_to_room(self, user_id, room_id):
        """ Add a user to a room, if they can join. """
        can_join = self.can_join_room(user_id, room_id)
        if not can_join['success']:
            return {
                'response_type': "error",
                'message': can_join['reason']
            }

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
            return {
                'response_type': "error",
                'message': [
                    "Room Full",
                    "There is a maximum of 4 players in a room.",
                    "Please wait for someone to leave, or try another room."
                ]
            }

        self.rooms[room_id]['players'][user_id] = {
            'name': fake_name,
            'score': 0
        }
        self.users[user_id]['room_id'] = room_id

        return {
            'response_type': "success"
        }

    def remove_user_from_room(self, user_id, room_id):
        """ Remove a user from a room. """
        del self.rooms[room_id]['players'][user_id]

    def can_join_room(self, user_id, room_id):
        """ Return a boolean after checking
            whether a user can join a room.
        """
        room = self.rooms[room_id]

        if room['game_stage'] != 0:
            # Game is started.
            return {
                'success': False,
                'reason': [
                    "Room Already Started",
                    "You cannot join an initiated room.",
                    "Please wait until the end of the game."
                ]
            }

        if len(room['players']) >= 4:
            # Max players hit (4).
            return {
                'success': False,
                'reason': [
                    "Room Full",
                    "There is a maximum of 4 players in a room.",
                    "Please wait for someone to leave, or try another room."
                ]
            }

        return {
            'success': True
        }

    def start_room(self, user_id, room_id):
        """ Initialize game parameters and draw
            the first set of active cards.
        """
        self.rooms[room_id]['game_stage'] = 1
        self.rooms[room_id]['active_cards'] = [
            self.rooms[room_id]['deck'].draw()
            for _ in range(12)
        ]

        return {
            'response_type': "start_room",
            'room': {
                'room_id': room_id,
                'players': self.rooms[room_id]['players'],
                'active_cards': [
                    c[0] for c in self.rooms[room_id]['active_cards']
                ]
            },
            'message': [
                "Game Started",
                "Let the matching begin!"
            ]
        }

    def leave_room(self, user_id):
        """ Remove user from room. """
        room_id = self.users[user_id]['room_id']
        self.remove_user_from_room(user_id, room_id)
        return {
            'response_type': "leave_room",
            'message': [
                "Left Room",
                "You have left the room with Room ID: {}".format(room_id)
            ]
        }

    def add_no_matches(self, user_id, room_id):
        """ Adds a user to the "no_matches" list.
            When all users in the room are on this list,
            we want to draw 3 cards.
        """
        room = self.rooms[room_id]

        room['no_matches'].add(user_id)
        message = [
            "No Matches Declared!",
            "Waiting on other players to declare no matches before proceeding."
        ]

        if sorted(room['no_matches']) == sorted(room['players'].keys()):
            # All players have voted for a card draw.
            if len(self.rooms[room_id]['deck']) > 0:
                room['active_cards'].extend([
                    room['deck'].draw() for _ in range(3)
                ])
                self.rooms[room_id]['no_matches'].clear()
                message = [
                    "No Matches Success",
                    "3 new cards have been added to the active cards."
                ]
                return {
                    'response_type': "no_matches",
                    'success': True,
                    'active_cards': [
                        c[0] for c in room['active_cards']
                    ],
                    'message': message
                }

            else:
                message = [
                    "Cannot Declare No Matches",
                    "There are no cards left in the deck."
                ]

        # Return False until all users have
        # toggled the no match option.
        return {
            'response_type': "no_matches",
            'success': False,
            'message': message
        }

    def handle_action(self, user_id, room_id, cards):
        # Get card definitions.
        card_defs = [
            card for card in self.rooms[room_id]['active_cards']
            if card[0] in cards
        ]
        success = self.check_cards(card_defs)
        message = [
            "Cards Do Not Match",
            "No match this time. Try again."
        ]
        if success:
            # Give the player a point.
            self.rooms[room_id]['players'][user_id]['score'] += 1

            # Remove the three cards picked.
            active_cards = [
                card for card in self.rooms[room_id]['active_cards']
                if card[0] not in cards
            ]

            message = [
                "Match Found!"
            ]

            if (len(active_cards) == 0
                    and len(self.rooms[room_id]['deck']) == 0):
                # Game complete.
                message.append("The game is completed!")
                return self.end_room(room_id, force=True, message=message)

            if (len(active_cards) < 12
                    and len(self.rooms[room_id]['deck']) > 0):
                # Draw three more cards.
                message.append("Three more cards are added to the table.")
                active_cards.extend(
                    [self.rooms[room_id]['deck'].draw() for _ in range(3)]
                )

            self.rooms[room_id]['active_cards'] = active_cards

        return {
            'response_type': "send_action",
            'success': success,
            'room': {
                'room_id': room_id,
                'players': self.rooms[room_id]['players'],
                'active_cards': [
                    c[0] for c in self.rooms[room_id]['active_cards']
                ]
            },
            'message': message
        }

    def end_room(self, room_id, user_id=None, force=False, message=[]):
        """ End the current game if all users vote.
            If force is True, end game anyway.
        """
        room = self.rooms[room_id]
        if not force and user_id is not None:
            room['end_room'].add(user_id)
            if len(room['end_room']) != len(room['players']):
                # Still waiting on other votes.
                return {
                    'response_type': "end_room",
                    'success': False,
                    'message': [
                        "Voted to End Room",
                        "Waiting for other players to react."
                    ]
                }

        winner = max(
            self.rooms[room_id]['players'].values(), key=lambda x: x['score']
        )

        self.rooms[room_id]['deck'] = Deck()
        self.rooms[room_id]['game_stage'] = 0
        self.rooms[room_id]['active_cards'] = []
        self.rooms[room_id]['no_matches'].clear()
        self.rooms[room_id]['end_room'].clear()
        self.rooms[room_id]['players'] = {
            u_id: {
                'name': val['name'],
                'score': 0
            } for u_id, val in self.rooms[room_id]['players'].items()
        }
        return {
            'response_type': "end_room",
            'success': True,
            'room': {
                'room_id': room_id,
                'players': self.rooms[room_id]['players'],
                'active_cards': []
            },
            'message': message.extend([
                "The winner is: {}".format(winner['name'])])
        }

    def check_cards(self, cards):
        """ Compare the cards passed in to
            determine whether they meet the
            matching criteria.
        """
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
            # All the same or all different.
            return 1
        return 0
