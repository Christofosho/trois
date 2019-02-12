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
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        try:
            payload = json.loads(payload)
            if "type" in payload and payload["type"] == "ping":
                return

            data = handler.distribute(self, payload)
            if data:
                print("Sending data: {}".format(data))
                self.sendMessage(json.dumps(data).encode('utf8'))
            else:
                print("Invalid data: {}".format(data))
                print("Payload was: {}".format(payload))

        except Exception as e:
            raise e

        except:
            import sys
            import traceback
            tb = sys.exc_info()[2]
            traceback.print_tb(tb)
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]

            print('An error occurred on line {} in statement {}'.format(
                line, text
            ))
        
    def onClose(self, wasClean, code, reason):
        print("Removing user: {}".format(self.user_id))
        handler.distribute(self, {
            'message_type': "unregister",
            'user_id': self.user_id
        })
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            self.clients.remove(client)


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
