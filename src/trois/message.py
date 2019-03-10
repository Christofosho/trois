import json


class Message():
    """ Handles messages sent to users.
        Also outputs debug print statements.
    """
    def __init__(self, payload=None, recipients=None):
        if payload is None:
            payload = {}
        if recipients is None:
            recipients = []
        self.payload = payload
        self.recipients = recipients

    def to_json_utf8(self):
        return json.dumps(self.payload).encode('utf8')
