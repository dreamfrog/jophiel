#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import sys
from .searchengine import SharedService

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class SearchClient:
    def __init__(self, address, port):
        try:
            self.transport = TSocket.TSocket(address,port)
            self.transport = TTransport.TBufferedTransport(self.transport)
            protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
            self.client = SharedService.Client(protocol)
            self.transport.open()
        except Thrift.TException, tx:
            print '%s' % (tx.message)
    def get_service(self):
        return self.client;
    
    def close(self):
        self.transport.close()     

class SearchClientFactory:
    
    def __init__(self):pass
    
    @classmethod
    def get_search_client(cls):
        return SearchClient('172.17.40.54', 9090)

