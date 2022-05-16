import logging
import json
import sys
import os

from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol

from environs import Env

from twisted.internet import reactor, task
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from src.handler import Handler

handler = Handler()


class ServerProtocol(WebSocketServerProtocol):
    requests = []
    logger = logging.getLogger('main')

    def onMessage(self, payload, isBinary):
        try:
            # Add an item to the requests lists
            # which will be handled by the LoopingTask
            # run in run_server.
            self.requests.append([
                handler.distribute, [
                    self,
                    json.loads(payload)
                ]
            ])

        except Exception as e:
            self.logger.error(e)

    def onClose(self, wasClean, code, reason):
        print("Removing user: {}".format(self.user_id))
        handler.distribute(self, {
            'message_type': "unregister",
            'user_id': self.user_id
        })


def run_server():
    log.startLogging(sys.stdout)
    env = Env()
    env.read_env()
    location = "ws://127.0.0.1:8080"

    factory = WebSocketServerFactory(location)
    factory.protocol = ServerProtocol
    factory.setProtocolOptions(autoPingInterval=5, autoPingTimeout=60)

    resource = WebSocketResource(factory)

    # Root is / and we are in /server/ running `poetry run trois`
    # TODO: This needs to be fixed, relative pathing is bad.
    root = File("../client/public/")

    root.putChild(b"ws", resource)
    site = Site(root)

    def handle_requests():
        for request in factory.protocol.requests:
            f = request[0]
            arguments = request[1]
            f(*arguments)
        factory.protocol.requests = []
        handler.send_messages()

    handle = task.LoopingCall(handle_requests)
    handle.start(0.2)

    reactor.listenTCP(8080, site)

    reactor.run()


def main():
    run_server()
