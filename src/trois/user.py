import uuid


class User():
    def __init__(self, handler, socket_identifier):
        self.user_id = str(uuid.uuid4())
        self.socket_identifier = socket_identifier
        self.socket_identifier.user_id = self.user_id

        self.room_id = None
        self.name = ""
        self.score = 0

        handler.users[self.user_id] = self
