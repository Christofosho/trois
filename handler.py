
import uuid
from deck import Deck
from validator import Validator


class Handler():

    validator = Validator()

    def __init__(self):
        """ Create two dicts:

            self.rooms: Contains a reference to each active room.
            self.users: Contains a reference to each active user.
        """
        self.rooms = {}
        self.users = {}

    def distribute(self, payload):
        message_type = payload.get("type", None)
        if not(message_type and self.validator.validate_message_type(message_type)):
            return

        # TODO: register
        if message_type == "register":
            return {
                "type": "register",
                "user_id": self.add_user()
            }

        # TODO: unregister
        elif message_type == "unregister":
            pass

        # TODO: join_room
        elif message_type == "join_room":
            pass

        # TODO: start_game
        elif message_type == "start_game":
            pass

        # TODO: send_action
        elif message_type == "send_action":
            pass

        # TODO: end_game
        elif message_type == "end_game":
            pass

        # TODO: leave_game
        elif message_type == "leave_game":
            pass

    def add_user(self):
        """ Add a user to the user dict and return the id """
        user_id = str(uuid.uuid4())

        # Set to None until a room is assigned.
        self.users[user_id] = None
        return user_id

    def remove_user(self, user_id):
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

    """ Room Functions """
    def add_room(self, owner_id):
        """ Add a new room to the self.rooms dict
            and generate a room_id for sharing.
            Return the room_id generated.

            owner_id: uuid representing the first user in the room.
        """
        room_id = uuid.uuid1()
        self.games[room_id] = {
            'room_id': room_id,
            'players': [owner_id],
            'deck': Deck()
        }
        self.users[owner_id] = room_id
        return room_id

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.games[room_id]
