#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# htmlextractor.py 21-Jan-2011
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
The :class:`DefaultHtmlLinkExtractor` will try to extract new links from the
``curi.content_body``. In order to find them two regular expressions are used.

1. The ``RELEVANT_TAG_EXTRACTOR`` extracts the following tags:
    - ``<script>..</script>``
    - ``<style>..</style>``
    - ``<meta>``
    - or any other open tag with at least one attribute (e.g. not ``<br>``).

2. The ``LINK_EXTRACTOR`` extracts links from tags using `href` or `src`
attributes.

If the link is relative, the appropriate prefix is automatically added here.

The regular expressions have been adopted from Heritrix. See the Heritrix 3
source code:

``modules/src/main/java/org/archive/modules/extractor/ExtractorHTML.java``

.. note:: Heritrix has a newer way of extracting links, i.e. with different
    regular expressions. Since these are working for me at the moment, I am
    fine with it.
"""
import re
import htmlentitydefs

import urlparse

from spyder.core.constants import CURI_EXTRACTED_URLS
from spyder.core.constants import CURI_OPTIONAL_TRUE, CURI_EXTRACTION_FINISHED
from spyder.encoding import get_content_type_encoding

# Maximum number of chars an element name may have
MAX_ELEMENT_REPLACE = "MAX_ELEMENT_REPLACE"

# Pattern for extracting relevant tags from HTML
#
# This pattern extracts:
#  1: <script>...</script>
#  2: <style>...</style>
#  3: <meta...>
#  4: any other open tag with at least one attribute
#     (eg matches "<a href='boo'>" but not "</a>" or "<br>")
#
# Groups in this pattern:
#
#  1: script src=foo>boo</script
#  2: just the script open tag
#  3: style type=moo>zoo</style
#  4: just the style open tag
#  5: entire other tag, without '<' '>'
#  6: element
#  7: meta
#  8: !-- comment --
RELEVANT_TAG_EXTRACTOR = "<(?:((script[^>]*)>[^(</script)]*</script)" + "|" + \
    "((style[^/]*)>[^(</style)]*</style)" + "|" + \
    "(((meta)|(?:\\w{1,MAX_ELEMENT_REPLACE}))\\s+[^>]*)" + "|" + \
    "(!--.*?--))>"


# The simpler pattern to extract links from tags
#
# Groups in this expression:
#
#  1: the attribute name
#  2: href | src
#  3: the url in quotes
LINK_EXTRACTOR = "(\w+)[^>]*?(?:(href|src))\s*=\s*" + \
    "(?:(\"[^\"]+\"|'[^']+'))"


class DefaultHtmlLinkExtractor(object):
    """
    The default extractor for Links from HTML pages.

    The internal regular expressions currently are not modifiable. Only the
    maximum length of an opening tag can be configured using the
    ``settings.REGEX_LINK_XTRACTOR_MAX_ELEMENT_LENGTH``.
    """

    def __init__(self, settings):
        """
        Initialize the regular expressions.
        """
        max_size = settings.REGEX_LINK_XTRACTOR_MAX_ELEMENT_LENGTH
        self._tag_extractor = re.compile(
                RELEVANT_TAG_EXTRACTOR.replace(MAX_ELEMENT_REPLACE,
                    str(max_size)), re.I | re.S)

        self._link_extractor = re.compile(LINK_EXTRACTOR, re.I | re.S)
        self._base_url = ""

    def __call__(self, curi):
        """
        Actually extract links from the html content if the content type
        matches.
        """
        if not self._restrict_content_type(curi):
            return curi

        if CURI_EXTRACTION_FINISHED in curi.optional_vars and \
            curi.optional_vars[CURI_EXTRACTION_FINISHED] == CURI_OPTIONAL_TRUE:
            return curi

        (_type, encoding) = get_content_type_encoding(curi)

        try:
            content = curi.content_body.decode(encoding)
        except Exception:
            content = curi.content_body

        parsed_url = urlparse.urlparse(curi.url)
        self._base_url = curi.url

        # iterate over all tags
        for tag in self._tag_extractor.finditer(content):

            if tag.start(8) > 0:
                # a html comment, ignore
                continue

            elif tag.start(7) > 0:
                # a meta tag
                curi = self._process_meta(curi, parsed_url, content,
                        (tag.start(5), tag.end(5)))

            elif tag.start(5) > 0:
                # generic <whatever tag
                curi = self._process_generic_tag(curi, parsed_url, content,
                        (tag.start(6), tag.end(6)),
                        (tag.start(5), tag.end(5)))

            elif tag.start(1) > 0:
                # <script> tag
                # TODO no script handling so far
                pass

            elif tag.start(3) > 0:
                # <style> tag
                # TODO no tag handling so far
                pass

        return curi

    def _process_generic_tag(self, curi, parsed_url, content,
            element_name_tuple, element_tuple):
        """
        Process a generic tag.

        This can be anything but `meta`, `script` or `style` tags.

        `content` is the decoded content body.
        `element_name_tuple` is a tuple containing (start,end) integers of
            the current tag name.
        `element_tuple` is a tuple containing (start,end) integers of the
            current element
        """
        (start, end) = element_name_tuple
        el_name = content[start:end]
        if "a" == el_name.lower():
            curi = self._extract_links(curi, parsed_url, content,
                    element_tuple)
        elif "base" == el_name.lower():
            self._base_url = self._get_links(content, element_tuple)[0]

        return curi

    def _get_links(self, content, element_tuple):
        """
        Do the actual link extraction and return the list of links.

        `content` is the decoded content body.
        `element_tuple` is a tuple containing (start,end) integers of the
            current element
        """
        links = []
        (start, end) = element_tuple
        element = self._unescape_html(content[start:end])

        for link_candidate in self._link_extractor.finditer(element):
            link = link_candidate.group(3)[1:-1]
            if link.find("mailto:") > -1 or link.find("javascript:") > -1:
                continue
            if link.find("://") == -1:
                link = urlparse.urljoin(self._base_url, link)
            links.append(link)

        return links

    def _extract_links(self, curi, parsed_url, content, element_tuple):
        """
        Extract links from an element, e.g. href="" attributes.
        """
        links = self._get_links(content, element_tuple)

        linkstring = "\n".join(links).encode('ascii', 'replace')
        if not CURI_EXTRACTED_URLS in curi.optional_vars:
            curi.optional_vars[CURI_EXTRACTED_URLS] = linkstring
        else:
            curi.optional_vars[CURI_EXTRACTED_URLS] += "\n" + linkstring

        return curi

    def _process_meta(self, curi, _parsed_url, _content, _element_tuple):
        """
        Process a meta tag.
        """
        return curi

    def _restrict_content_type(self, curi):
        """
        Decide based on the `CrawlUri`s Content-Type whether we want to process
        it.
        """
        allowed = ["text/html", "application/xhtml", "text/vnd.wap.wml",
            "application/vnd.wap.wml", "application/vnd.wap.xhtm"]
        (ctype, _enc) = get_content_type_encoding(curi)
        return ctype in allowed

    def _unescape_html(self, link):
        """
        Unescape the link.

        keep &amp;, &gt;, &lt; in the source code.

        http://effbot.org/zone/re-sub.htm#unescape-html
        """
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text
        return re.sub("&#?\w+;", fixup, link)
