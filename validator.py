
class Validator():
    valid_message_types = set([
        "register",
        "join_room",
        "start_game",
        "send_action",
        "end_game",
        "leave_game"
    ])

    def __init__(self):
        pass

    def validate_message_type(self, message_type):
        if message_type in self.valid_message_types:
            return message_type

        return None
    