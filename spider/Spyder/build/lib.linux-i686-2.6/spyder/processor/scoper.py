#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# scoper.py 24-Jan-2011
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
"""
The *Crawl Scope* defines which *URLs* the *Spyder* should process. The main
usecases for them are:

- only spider content from the *Seed* Hosts
- do not spider images, css, videos

and there are probably a lot of other reasons you want to have at least one the
scoper configured, otherwise you might end up downloading the internet.

So each scoper should iterate over the
``curi.optional_vars[CURI_EXTRACTED_URLS]`` and determine if it should be
downloaded or not.

The :class:`RegexScoper` maintains a list of regular expressions that define
the crawl scope. Two classes of expressions exist: positive and negative.
The initial decision of the scoper is to not download its content. If a regex
from the positive list matches, and no regex from the negative list matches,
the *URL* is marked for downloading. In any other case, the *URL* will be
abandoned.

.. note:: We should really split up the regex scoper and allow the user to
    configure more than just one scoper.
"""

import re

from spyder.core.constants import CURI_EXTRACTED_URLS


class RegexScoper(object):
    """
    The scoper based on regular expressions.

    There are two settings that influence this scoper:

    1. ``settings.REGEX_SCOPE_POSITIVE``
    2. ``settings.REGEX_SCOPE_NEGATIVE``

    Both have to be a ``list``. The scoper is executed in the
    :meth:`__call__` method.
    """

    def __init__(self, settings):
        """
        Compile the regular expressions.
        """
        self._positive_regex = []
        for regex in settings.REGEX_SCOPE_POSITIVE:
            self._positive_regex.append(re.compile(regex))

        self._negative_regex = []
        for regex in settings.REGEX_SCOPE_NEGATIVE:
            self._negative_regex.append(re.compile(regex))

    def __call__(self, curi):
        """
        Filter all newly extracted URLs for those we want in this crawl.
        """
        if CURI_EXTRACTED_URLS not in curi.optional_vars:
            return curi

        urls = []
        for url in curi.optional_vars[CURI_EXTRACTED_URLS].split("\n"):
            add_url = False
            for regex in self._positive_regex:
                if regex.match(url):
                    add_url = True

            for regex in self._negative_regex:
                if regex.match(url):
                    add_url = False

            if add_url:
                urls.append(url)

        curi.optional_vars[CURI_EXTRACTED_URLS] = "\n".join(urls)
        return curi
