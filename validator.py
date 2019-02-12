
class Validator():
    valid_message_types = set([
        "register",
        "unregister",
        "new_room",
        "join_room",
        "start_room",
        "send_action",
        "end_room",
        "leave_room"
    ])

    def __init__(self, handler):
        self.handler = handler

    def validate_message_type(self, message_type):
        if message_type and (message_type in self.valid_message_types):
            return True
        return False

    def validate_user_id(self, user_id):
        if user_id and (user_id in self.handler.users):
            return True
        return False

    def validate_room_id(self, room_id):
        if room_id and (room_id in self.handler.rooms):
            return True
        return False

    def validate_cards(self, room_id, cards):
        if not isinstance(cards, list):
            return False

        matches = 0
        for card in range(len(self.handler.rooms[room_id]['deck'].cards)):
            if card in cards:
                matches += 1
        return matches == 3
