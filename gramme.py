# -*- coding: utf-8 -*-

try:
    import gevent.monkey
    gevent.monkey.patch_all()
    #gevent.monkey.patch_thread()
except ImportError:
    pass

import time
import socket
import threading
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

from logbook import Logger
import msgpack

log = Logger(__name__)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    """ Mixin class """
    pass

class GrammeServer(socketserver.BaseRequestHandler):

    def handle(self):
        data = msgpack.unpackb(self.request[0])
        socket = self.request[1]
        log.info('Recieved message from: {0}'.format(str(socket)))
        log.debug(dict(raw=self.request[0], data=data, socket=socket))
        return GrammeServer._handler(data)


def server(host, port):

    def wrapper(fn):

        log.info('Starting up server: {0}:{1}'.format(host, port))
        GrammeServer._handler = fn
        _server = ThreadedUDPServer((host, port), GrammeServer)
        try:
            server_thread = threading.Thread(target=_server.serve_forever)
            # Exit the server thread when the main thread terminates
            server_thread.daemon = True
            server_thread.start()
        except KeyboardInterrupt:
            log.info('Cleaning up')
            #_server.shutdown()
        return fn

    return wrapper


class GrammeClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        packaged = msgpack.packb(data)
        log.info('Sending data to: {0}:{1}'.format(self.host, self.port))
        log.debug(dict(raw=data, packaged=packaged, host=self.host, port=self.port))
        self._sock.sendto(packaged, (self.host, self.port))
        #_sock.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))

client = GrammeClient


@server('0.0.0.0', 3030)
def data_handler(data):
    print data

sender = client('0.0.0.0', 3030)

sender.send('hello world!')
time.sleep(2)