"""Recursive webcrawler example.

For asynchronous DNS lookups install the `dnspython` package:

    $ pip install dnspython

Requires the `pybloom` module for the bloom filter which is used
to ensure a lower chance of recrawling an URL previously seen.

Since the bloom filter is not shared, but only passed as an argument
to each subtask, it would be much better to have this as a centralized
service.  Redis sets could also be a practical solution.

A BloomFilter with a capacity of 100_000 members and an error rate
of 0.001 is 2.8MB pickled, but if compressed with zlib it only takes
up 2.9kB(!).

We don't have to do compression manually, just set the tasks compression
to "zlib", and the serializer to "pickle".


"""

from __future__ import with_statement

import re
import time
import urlparse

from celery.task import task
from celery.task.sets import TaskSet
from eventlet import Timeout
from eventlet.green import urllib2

from jophiel.contrib.bloomfilter.pybloom import BloomFilter

# http://daringfireball.net/2009/11/liberal_regex_for_matching_urls
url_regex = re.compile(
    r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')


def domain(url):
    """Returns the domain part of an URL."""
    return urlparse.urlsplit(url)[1].split(":")[0]


@task(ignore_result=True, serializer="pickle", compression="zlib")
def crawl(url, seen=None):
    print("crawling: %r" % (url, ))
    if not seen:
        seen = BloomFilter(capacity=50000, error_rate=0.0001)

    with Timeout(5, False):
        try:
            data = urllib2.urlopen(url).read()
        except (urllib2.HTTPError, IOError):
            return

    location = domain(url)
    wanted_urls = []
    for url_match in url_regex.finditer(data):
        url = url_match.group(0)
        # To not destroy the internet, we only fetch URLs on the same domain.
        if url not in seen and location in domain(url):
            wanted_urls.append(url)
            seen.add(url)

    subtasks = TaskSet(crawl.subtask((url, seen)) for url in wanted_urls)
    subtasks.apply_async()
