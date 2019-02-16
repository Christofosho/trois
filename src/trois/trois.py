import json
import sys

from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from trois.handler import Handler

handler = Handler()


class ServerProtocol(WebSocketServerProtocol):
    def onMessage(self, payload, isBinary):
        try:
            handler.distribute(self, json.loads(payload))
            for message in handler.messages:
                for r in message.recipients:
                    r.sendMessage(
                        message.to_json_utf8()
                    )
            handler.messages.clear()

        except Exception as e:
            raise e

    def onClose(self, wasClean, code, reason):
        print("Removing user: {}".format(self.user_id))
        handler.distribute(self, {
            'message_type': "unregister",
            'user_id': self.user_id
        })


def run_server():
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory(u"ws://127.0.0.1:8080")
    factory.protocol = ServerProtocol
    resource = WebSocketResource(factory)
    root = File("./public/")
    root.putChild(b"ws", resource)
    site = Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()


if __name__ == "__main__":
    run_server()
