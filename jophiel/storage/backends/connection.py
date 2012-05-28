import time
import socket
import sys

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol

from thrift import Thrift
from .hbase import Hbase
from .base import *

DEFAULT_SERVER = 'localhost:9160'
DEFAULT_PORT = 9160

_BASE_BACKOFF = 0.01

class Connection(Hbase.Client):
    """Encapsulation of a client session."""

    def __init__(self, server=DEFAULT_SERVER, framed_transport=False, timeout=None,
                 credentials=None, api_version=None):
        self.server = server
        server = server.split(':')
        if len(server) <= 1:
            port = DEFAULT_PORT
        else:
            port = server[1]
        host = server[0]
        socket = TSocket.TSocket(host, int(port))
        if timeout is not None:
            socket.setTimeout(timeout*1000.0)
        if framed_transport:
            self.transport = TTransport.TFramedTransport(socket)
        else:
            self.transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        #protocol = TBinaryProtocol.TBinaryProtocolAccelerated(self.transport)
        Hbase.Client.__init__(self, protocol)
        self.transport.open()

    def close(self):
        if self.transpoert:
            self.transport.close()

