import uuid
from trois.message import Message
from trois.room import Room
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
            return Message(
                message_type="error",
                payload={
                    'message': [
                        "Invalid Action",
                        "You have attempted to perform an invalid action.",
                        "Contact _ if you need assistance."
                    ]
                },
                debug_print="Invalid message: {}".format(message_type)
            )

        if message_type == "register":
            # Register a user in the system.
            user_id = self.add_user(client)
            return Message(
                message_type="register",
                payload={
                    'user_id': user_id
                },
                debug_print="User registered: {}".format(user_id)
            )

        # All other routes assume the user is authenticated.
        valid_user = self.validator.validate_user_id(user_id)
        if not valid_user:
            return Message(
                message_type="error",
                payload={
                    'message': [
                        "Invalid User ID",
                        "Oops! Looks like your User ID is"
                        " not showing up in our system.",
                        "Reload the page to fix the problem."
                    ]
                },
                debug_print="Invalid user: {}".format(user_id)
            )

        if message_type == "unregister":
            # Remove a user from the handler.
            user_id = self.remove_user(user_id)
            return Message( # TODO: Handle this? Maybe.
                message_type="unregister",
                payload={}
            )

        elif message_type == "new_room":
            # Create a new room and add the user to it.
            room = self.add_room(user_id)
            error = self.add_user_to_room(user_id, room)
            if error:
                return Message(
                    message_type="error",
                    payload={
                        "message": error
                    }
                )

            return Message(
                message_type="init_room",
                payload={
                    'room': self.getRoomInformation(room),
                    'message': [
                        "New Room",
                        "You have created a new room.",
                        "Your Room ID is: {}".format(room.room_id)
                    ]
                },
                debug_print="Creating a new room with user: {}".format(user_id)
            )

        # All other routes assume the room exists.
        room_id = payload.get('room_id', None)
        valid_room = self.validator.validate_room_id(room_id)
        if not valid_room:
            return Message(
                message_type="error",
                payload={
                    'message': [
                        "Invalid Room ID",
                        "Please verify the ID you have used and try again."
                    ]
                },
                debug_print="Invalid room_id for user: {}".format(user_id)
            )

        if message_type == "join_room":
            # Player joins room if game has not begun.
            error = self.add_user_to_room(user_id, valid_room)
            if error:
                return Message(
                    message_type="error",
                    payload={
                        'message': error
                    }
                )

            return Message(
                message_type="init_room",
                payload={
                    'room': self.getRoomInformation(valid_room),
                    'message': [
                        "New Player",
                        "{} has joined the room.".format(
                            valid_room.players[user_id]['name']
                        )
                    ]
                },
                broadcast=True,
                debug_print="User ID {} has joined Room ID {}".format(
                    user_id, valid_room.room_id
                )
            )

        elif message_type == "start_room":
            # Start the game.
            self.start_room(user_id, valid_room)
            return Message(
                message_type="start_room",
                payload={
                    'room': self.getRoomInformation(valid_room),
                    'message': [
                        "Game Started",
                        "Let the matching begin!"
                    ]
                },
                broadcast=True
            )

        elif message_type == "send_action":
            # Check the user submitted cards to see if
            # they are a match.
            cards = payload.get('cards', None)
            valid_cards = self.validator.validate_cards(valid_room, cards)
            if not valid_cards:
                return Message(
                    message_type="error",
                    payload={
                        "message": [
                            "Invalid Cards",
                            "Please try another set of cards."
                        ]
                    }
                )

            message = self.handle_action(user_id, valid_room, cards)
            return Message(
                message_type="update_room",
                payload={
                    'room': self.getRoomInformation(valid_room),
                    'message': message
                },
                broadcast=True
            )

        elif message_type == "no_matches":
            message = self.add_no_matches(user_id, valid_room)
            return Message(
                message_type="update_room",
                payload={
                    'room': self.getRoomInformation(valid_room),
                    'message': message
                },
                broadcast=True
            )

        elif message_type == "end_room":
            vote_complete = self.vote_to_end_room(user_id, valid_room)
            if not vote_complete:
                return Message(
                    message_type="error",
                    payload={
                        'message': [
                            "Vote To End",
                            "A vote to end the room has been initiated."
                        ]
                    },
                    broadcast=True
                )

            message = self.end_room(valid_room)
            return Message(
                message_type="init_room",
                payload={
                    'room': self.getRoomInformation(valid_room),
                    'message': message
                },
                broadcast=True
            )

        elif message_type == "leave_room":
            # TODO: How to broadcast this?
            return Message(
                message_type="leave_room",
                payload={
                    'message': self.leave_room(user_id, valid_room)
                }
            )

    def add_user(self, client):
        """ Add a user to the user dict and return the id.

            client: socket object
        """
        user_id = str(uuid.uuid4())
        client.user_id = user_id
        client.factory.register(user_id, client)

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
            if user_id in room.players:
                del room.players[user_id]

            if len(room.players) < 1:
                self.remove_room(room_id)

        return user_id

    def add_room(self, owner_id):
        """ Add a new room to the self.rooms dict
            and generate a room_id for sharing.
            Return the room information generated.
        """
        return Room(self)

    def remove_room(self, room_id):
        """ Remove an empty room. """
        if room_id in self.rooms:
            del self.rooms[room_id]

    def add_user_to_room(self, user_id, room):
        """ Add a user to a room, if they can join. """
        can_join_error = self.can_join_room(user_id, room)
        if can_join_error:
            return can_join_error

        for r in self.rooms.values():
            if user_id in r.players:
                self.remove_user_from_room(user_id, r)

        active_players = len(room.players)
        fake_name = "Player 1"
        if active_players == 1:
            fake_name = "Player 2"

        elif active_players == 2:
            fake_name = "Player 3"

        elif active_players == 3:
            fake_name = "Player 4"

        room.players[user_id] = {
            'name': fake_name,
            'score': 0
        }
        self.users[user_id]['room_id'] = room.room_id

    def remove_user_from_room(self, user_id, room):
        """ Remove a user from a room. """
        del room.players[user_id]

    def can_join_room(self, user_id, room):
        """ Return an error if user_id cannot join room. """

        if room.game_stage != 0:
            # Game is started.
            return [
                "Room Already Started",
                "You cannot join an initiated room.",
                "Please wait until the end of the game."
            ]

        if len(room.players) >= 4:
            # Max players hit (4).
            return [
                "Room Full",
                "There is a maximum of 4 players in a room.",
                "Please wait for someone to leave, or try another room."
            ]

        return

    def start_room(self, user_id, room):
        """ Initialize game parameters and draw
            the first set of active cards.
        """
        room.game_stage = 1
        room.active_cards = [
            room.deck.draw()
            for _ in range(12)
        ]

    def leave_room(self, user_id, room):
        """ Remove user from room. """
        self.remove_user_from_room(user_id, room)
        return [
            "Left Room",
            "You have left the room."
        ]

    def add_no_matches(self, user_id, room):
        """ Adds a user to the "no_matches" list.
            When all users in the room are on this list,
            we want to draw 3 cards.
        """
        room.no_matches.add(user_id)

        if sorted(room.no_matches) == sorted(room.players.keys()):
            # All players have voted for a card draw.
            if len(room.deck) > 0:
                room.active_cards.extend([
                    room.deck.draw() for _ in range(3)
                ])
                room.no_matches.clear()
                room.end_room.clear()
                return [
                    "No Matches Success",
                    "3 new cards have been added to the active cards."
                ]

            else:
                return [
                    "Cannot Declare No Matches",
                    "There are no cards left in the deck."
                ]

        return [
            "No Matches Declared!",
            "Waiting on other players to declare no matches before proceeding."
        ]

    def handle_action(self, user_id, room, cards):
        # Get card definitions.
        card_defs = [
            card for card in room.active_cards
            if card[0] in cards
        ]
        success = self.check_cards(card_defs)
        message = [
            "Cards Do Not Match",
            "No match this time. Try again."
        ]
        if success:
            # Give the player a point.
            room.players[user_id]['score'] += 1

            # Remove the three cards picked.
            active_cards = [
                card for card in room.active_cards
                if card[0] not in cards
            ]

            message = [
                "Match Found!"
            ]

            if (len(active_cards) == 0
                    and len(room.deck) == 0):
                # Game complete.
                return self.end_room(room)

            if (len(active_cards) < 12
                    and len(room.deck) > 0):
                # Draw three more cards.
                message.append("Three more cards are added to the table.")
                active_cards.extend(
                    [room.deck.draw() for _ in range(3)]
                )

            room.active_cards = active_cards
            room.end_room.clear()
            room.no_matches.clear()

        return message

    def vote_to_end_room(self, user_id, room):
        """ End the current game if all users vote.
            If force is True, end game anyway.
        """
        if user_id is not None:
            room.end_room.add(user_id)
            if len(room.end_room) != len(room.players):
                # Still waiting on other votes.
                return False
        return True

    def end_room(self, room):
        room.reset()
        return [
            "Game Over",
            "The winner of this round: {}!".format(
                max(
                    room.players.values(),
                    key=lambda x: x['score']
                )['name']
            )
        ]

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

    def getRoomInformation(self, room):
        return {
            'room_id': room.room_id,
            'players': room.players,
            'active_cards': [
                c[0] for c in room.active_cards
            ]
        }
