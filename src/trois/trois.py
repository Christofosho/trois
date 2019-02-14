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


class EchoServerProtocol(WebSocketServerProtocol):
    def onMessage(self, payload, isBinary):
        try:
            data = handler.distribute(self, json.loads(payload))
            if data.broadcast:
                self.factory.broadcast(data)

            else:
                self.sendMessage(data.to_json_utf8())

        except Exception as e:
            raise e

    def onClose(self, wasClean, code, reason):
        print("Removing user: {}".format(self.user_id))
        handler.distribute(self, {
            'message_type': "unregister",
            'user_id': self.user_id
        })
        self.factory.unregister(self.user_id)


class BroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = {}

    def register(self, client_id, client):
        if client not in self.clients:
            self.clients[client_id] = client

    def unregister(self, client_id):
        if client_id in self.clients:
            del self.clients[client_id]

    def broadcast(self, data):
        for user_id in data.payload['room']['players'].keys():
            if user_id in self.clients:
                self.clients[user_id].sendMessage(data.to_json_utf8())


def run_server():
    log.startLogging(sys.stdout)
    factory = BroadcastServerFactory(u"ws://127.0.0.1:5000")
    factory.protocol = EchoServerProtocol
    resource = WebSocketResource(factory)
    root = File("./public/")
    root.putChild(b"ws", resource)
    site = Site(root)
    reactor.listenTCP(5000, site)
    reactor.run()


if __name__ == "__main__":
    run_server()
