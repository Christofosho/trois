import json
import sys

from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from handler import Handler

handler = Handler()


class EchoServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        try:
            payload = json.loads(payload)
            data = handler.distribute(payload)
            self.sendMessage(json.dumps(data).encode('utf8'))

        except:
            import sys
            import traceback
            tb = sys.exc_info()[2]
            traceback.print_tb(tb)
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]

            print('An error occurred on line {} in statement {}'.format(line, text))



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

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    factory = BroadcastServerFactory(u"ws://127.0.0.1:5000")
    factory.protocol = EchoServerProtocol
    resource = WebSocketResource(factory)
    root = File("./public/")
    root.putChild(b"ws", resource)
    site = Site(root)
    reactor.listenTCP(5000, site)
    reactor.run()
