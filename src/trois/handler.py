import logging

from trois.message import Message
from trois.room import Room
from trois.user import User
from trois.validator import Validator


class Handler():
    logger = logging.getLogger('handler')

    def __init__(self):
        """ Create two dicts:

            self.rooms: Contains a reference to each active room.
            self.users: Contains a reference to each active user.
        """
        self.rooms = {}
        self.users = {}
        self.messages = set()

        self.validator = Validator(self)

        self.logger.setLevel(logging.INFO)
        eh = logging.FileHandler('error.log')
        eh.setLevel(logging.ERROR)
        ih = logging.FileHandler('info.log')
        ih.setLevel(logging.INFO)
        self.logger.addHandler(eh)
        self.logger.addHandler(ih)

    def send_messages(self):
        """ Sends messages over websocket. """
        for message in self.messages:
            for r in message.recipients:
                r.sendMessage(
                    message.to_json_utf8()
                )
        self.messages.clear()

    def distribute(self, client, payload):
        """ Distribute the payload to the correct handler function
            by determining the type of action the payload is requesting.

            client: socket object
            payload: dict of information including a type

            Must return a Message object.
        """
        message_type = payload.get('message_type', None)
        valid_message = self.validator.validate_message_type(message_type)
        if not valid_message:
            self.messages.add(Message(
                payload={
                    'message_type': "error",
                    'message': [
                        "Invalid Action",
                        "You have attempted to perform an invalid action.",
                        "Contact _ if you need assistance."
                    ]
                },
                recipients=[client]
            ))
            self.logger.error("Invalid message sent by {}".format(
                client.user_id
            ))
            return

        user_id = payload.get('user_id', None)
        if message_type == "register":
            # Register a user in the system.
            user = self.add_user(client)
            self.messages.add(Message(
                payload={
                    'message_type': "register",
                    'user_id': user.user_id
                },
                recipients=[user.socket_identifier]
            ))
            self.logger.info("Added user {}".format(
                user.user_id
            ))
            return

        # All other routes assume the user is authenticated.
        user = self.validator.validate_user_id(user_id)
        if not user:
            self.messages.add(Message(
                payload={
                    'message_type': "error",
                    'message': [
                        "Invalid User ID",
                        "Oops! Looks like your User ID is"
                        " not showing up in our system.",
                        "Reload the page to fix the problem."
                    ]
                },
                recipients=[client]
            ))
            self.logger.error("Invalid user {}.".format(
                user_id
            ))
            return

        if message_type == "unregister":
            # Remove a user from the handler.
            name = user.name
            room = self.validator.validate_room_id(user.room_id)
            self.logger.info("Removed user {}.".format(
                user_id
            ))
            self.remove_user(user)
            # TODO: Send an update if user was in _room_
            self.messages.add(Message(
                payload={
                    'message_type': "unregister",
                    'message': [
                        "{} has disconnected.".format(name)
                    ]
                },
                recipients=[
                    p.socket_identifier for p in room.players.values()
                ]
            ))

        elif message_type == "new_room":
            # Create a new room and add the user to it.
            room = self.add_room()
            error = self.add_user_to_room(user, room)
            if error:
                self.messages.add(Message(
                    payload={
                        'message_type': "error",
                        "message": error
                    },
                    recipients=[user.socket_identifier]
                ))
                self.logger.error("Error joining room {} for user {}.".format(
                    room.room_id, user.user_id
                ))

            else:
                self.messages.add(Message(
                    payload={
                        'message_type': "init_room",
                        'room': room.get_public_information(),
                        'message': [
                            "New Room",
                            "You have created a new room.",
                            "Your Room ID is: {}".format(room.room_id)
                        ]
                    },
                    recipients=[
                        p.socket_identifier for p in room.players.values()
                    ]
                ))
                self.logger.info("User {} joined room {}.".format(
                    user.user_id, room.room_id
                ))
            return

        # All other routes assume the room exists.
        room_id = payload.get('room_id', None)
        room = self.validator.validate_room_id(room_id)
        if not room:
            self.messages.add(Message(
                payload={
                    'message_type': "error",
                    'message': [
                        "Invalid Room ID",
                        "Please verify the ID you have used and try again."
                    ]
                },
                recipients=[user.socket_identifier]
            ))
            self.logger.error("Invalid room {} for user {}.".format(
                room_id, user.user_id
            ))
            return

        if message_type == "join_room":
            # Player joins room if game has not begun.
            error = self.add_user_to_room(user, room)
            if error:
                self.messages.add(Message(
                    payload={
                        'message_type': "error",
                        'message': error
                    },
                    recipients=[user.socket_identifier]
                ))
                self.logger.error("Failed to add user {} to room {}.".format(
                    user.user_id, room.room_id
                ))

            else:
                self.messages.add(Message(
                    payload={
                        'message_type': "init_room",
                        'room': room.get_public_information(),
                        'message': [
                            "New Player",
                            "{} has joined the room.".format(
                                user.name
                            )
                        ]
                    },
                    recipients=[
                        p.socket_identifier for p in room.players.values()
                    ]
                ))
                self.logger.info("User {} joined room {}.".format(
                    user.user_id, room.room_id
                ))
            return

        elif message_type == "start_room":
            # Start the game.
            self.messages.add(Message(
                payload={
                    'message_type': "start_room",
                    'message': self.start_room(user, room),
                    'room': room.get_public_information()
                },
                recipients=[
                    p.socket_identifier for p in room.players.values()
                ]
            ))
            self.logger.info("User {} has requested to start_room.".format(
                user.user_id
            ))
            return

        elif message_type == "leave_room":
            self.messages.add(Message(
                payload={
                    'message_type': "leave_room",
                    'message': self.leave_room(user, room)
                },
                recipients=[user.socket_identifier]
            ))
            self.messages.add(Message(
                payload={
                    'message_type': "update_room",
                    'room': room.get_public_information(),
                    'message': [
                        "User Left Room",
                        "{} has left the room.".format(user.name)
                    ]
                },
                recipients=[
                    p.socket_identifier for p in room.players.values()
                ]
            ))
            self.logger.error("User {} has left room {}.".format(
                user.user_id, room.room_id
            ))
            return

        # The following actions must have a game started.
        if not room.started:
            self.logger.error(
                "User {} attempted to perform {}"
                " while not in room {}.".format(
                    user.user_id, message_type, room.room_id
                )
            )
            return

        if message_type == "send_action":
            # Check the user submitted cards to see if
            # they are a match.
            cards = payload.get('cards', None)
            valid_cards = self.validator.validate_cards(room, cards)
            if not valid_cards:
                self.messages.add(Message(
                    payload={
                        'message_type': "error",
                        "message": [
                            "Invalid Cards",
                            "Please try another set of cards."
                        ]
                    },
                    recipients=[user.socket_identifier]
                ))
                self.logger.error("User {} attempted to use invalid cards.".format(
                    user.user_id, room.room_id
                ))
                self.logger.error(cards)

            else:
                self.messages.add(Message(
                    payload={
                        'message_type': "update_room",
                        'message': self.handle_action(user, room, cards),
                        'room': room.get_public_information()
                    },
                    recipients=[
                        p.socket_identifier for p in room.players.values()
                    ]
                ))
                self.logger.info("User {} has performed {}.".format(
                    user.user_id, message_type
                ))
            return

        elif message_type == "draw_cards":
            self.messages.add(Message(
                payload={
                    'message_type': "update_room",
                    'message': self.draw_cards(user, room),
                    'room': room.get_public_information()
                },
                recipients=[
                    p.socket_identifier for p in room.players.values()
                ]
            ))
            self.logger.error("User {} has declared draw_cards.".format(
                user.user_id
            ))

        elif message_type == "end_room":
            self.messages.add(Message(
                payload={
                    'message_type': "init_room",
                    'message': self.vote_to_end_room(user, room),
                    'room': room.get_public_information()
                },
                recipients=[
                    p.socket_identifier for p in room.players.values()
                ]
            ))
            self.logger.error("User {} has voted to end the room.".format(
                user.user_id
            ))
            return

    def add_user(self, client):
        """ Add a user to the user dict and return the id.

            client: socket object
        """
        return User(self, client)

    def remove_user(self, user):
        """ Remove a user from the user dict. """
        room_id = None
        if user.user_id not in self.users:
            return

        room_id = user.room_id

        if room_id and room_id in self.rooms:
            room = self.rooms[room_id]
            if user.user_id in room.players:
                del room.players[user.user_id]

            if len(room.players) < 1:
                self.remove_room(room)

        del self.users[user.user_id]

    def add_room(self):
        """ Add a new room to the self.rooms dict
            and generate a room_id for sharing.
            Return the room information generated.
        """
        return Room(self)

    def remove_room(self, room_id):
        """ Remove an empty room. """
        if room_id in self.rooms:
            del self.rooms[room_id]

    def add_user_to_room(self, user, room):
        """ Add a user to a room, if they can join. """
        can_join_error = self.can_join_room(user, room)
        if can_join_error:
            return can_join_error

        for r in self.rooms.values():
            if user.user_id in r.players:
                self.remove_user_from_room(user, r)

        active_players = len(room.players)
        fake_name = "Player {}".format(active_players + 1)

        user.name = fake_name
        user.room_id = room.room_id
        room.add_user(user)

    def remove_user_from_room(self, user, room):
        """ Remove a user from a room. """
        del room.players[user.user_id]

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

    def start_room(self, user, room):
        """ Initialize game parameters and draw
            the first set of active cards.
        """
        if user.user_id not in room.players:
            return [
                "Invalid Request",
                "Something went wrong with your request."
            ]

        room.start_room.add(user.user_id)

        if len(room.start_room) != len(room.players):
            # Still waiting on other votes.
            return [
                "Time to Play",
                "Waiting for all players to press the \"Start\" button."
            ]

        room.start()

        return [
            "Game Started",
            "Let the matching begin!"
        ]

    def leave_room(self, user, room):
        """ Remove user from room. """
        self.remove_user_from_room(user, room)
        for i, p in enumerate(room.players.values()):
            p.name = "Player {}".format(i + 1)
        return [
            "Left Room",
            "You have left the room."
        ]

    def draw_cards(self, user, room):
        """ Adds a user to the "draw_cards" list.
            When all users in the room are on this list,
            we want to draw 3 cards.
        """
        room.draw_cards.add(user.user_id)

        if sorted(room.draw_cards) == sorted(room.players.keys()):
            # All players have voted for a card draw.
            room.draw_cards.clear()
            room.end_room.clear()

            added_new_cards = room.add_cards()
            if added_new_cards:
                return [
                    "Cards Added",
                    "3 new cards have been added to the game."
                ]

            else:
                return [
                    "Cannot Draw Cards",
                    "There are no cards left in the deck."
                ]

        return [
            "Draw 3 Cards",
            "{} would like to draw 3 new cards.".format(user.name),
            "Click \"Draw\" if you agree."
        ]

    def handle_action(self, user, room, cards):
        """ Determine matching cards, and whether the
            game should continue after the action is
            complete.
        """
        # Get card definitions.
        card_defs = [
            card for card in room.active_cards
            if card[0] in cards
        ]
        success = room.deck.check_cards(card_defs)
        message = [
            "Failed Match",
            "The cards {} chose did not match.".format(user.name)
        ]
        if success:
            # Give the player a point.
            user.score += 1

            message = [
                "Match Found by {}!".format(user.name)
            ]

            # Remove the three cards picked.
            room.remove_cards(cards)
            room.end_room.clear()
            room.draw_cards.clear()
            
            if len(room.active_cards) < 12:
                added_new_cards = room.add_cards()
                if added_new_cards:
                    message.append("Three more cards are added to the table.")

        return message

    def vote_to_end_room(self, user, room):
        """ End the current game if all users vote.
            If force is True, end game anyway.
        """
        room.end_room.add(user.user_id)
        if len(room.end_room) != len(room.players):
            # Still waiting on other votes.
            return [
                "Vote To End",
                "A vote to end the room has been initiated."
            ]
        return self.end_room(room)

    def end_room(self, room):
        """ Reset a given room and return
            game over message.
        """
        room.reset()
        return [
            "Game Over | Room ID: {}".format(room.room_id),
            "The winner of this round: {}!".format(
                max(
                    room.players.values(),
                    key=lambda x: x.score
                ).name
            )
        ]
