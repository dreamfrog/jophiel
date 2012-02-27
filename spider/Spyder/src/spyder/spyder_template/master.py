#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# master.py 21-Apr-2011
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
"""
Master module starting a crawl.
"""
from spyder import CrawlUri

from sink import MySink


def initialize(settings, zmq_ctx, io_loop, frontier):
    """
    Initialize the **Master**.

    You may access and manipulate the `settings`, the process global `zmq_ctx`,
    *pyzmq's* `io_loop` and the `frontier`.
    """
    frontier.add_uri(CrawlUri("http://www.dmoz.org/Recreation/Boating/Sailing/")))
    frontier.add_sink(MySink(settings))
