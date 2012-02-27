#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# test_limiter.py 18-Jan-2011
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

import unittest

from spyder.core.constants import CURI_EXTRACTION_FINISHED, CURI_OPTIONAL_TRUE
from spyder.processor import limiter
from spyder.thrift.gen.ttypes import CrawlUri


class LimiterTestCase(unittest.TestCase):

    def test_do_not_process_robots_works(self):

        curi = CrawlUri()
        curi.effective_url = "http://127.0.0.1/robots.txt"
        curi.optional_vars = dict()

        l = limiter.DefaultLimiter(None)

        for i in range(2):
            l._do_not_process_robots(curi)
            self.assertEqual(CURI_OPTIONAL_TRUE,
                    curi.optional_vars[CURI_EXTRACTION_FINISHED])


if __name__ == '__main__':
    unittest.main()
