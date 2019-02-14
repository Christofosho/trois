import json


class Message():
    """ Handles messages sent to users.
        Also outputs debug print statements (TODO: Proper logging).
    """
    def __init__(self, message_type="", payload={},
                 broadcast=False, debug_print=None):
        self.message_type = message_type
        self.payload = payload
        self.broadcast = broadcast

        if debug_print:
            print(debug_print)

    def to_json_utf8(self):
        return json.dumps({
            'message_type': self.message_type,
            'payload': self.payload
        }).encode('utf8')
