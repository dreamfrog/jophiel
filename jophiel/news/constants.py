import re

from django.conf import settings


# blocked html takes a list of tag names, i.e. ['script', 'img', 'embed']
NEWS_BLOCKED_HTML = getattr(settings, 'NEWS_BLOCKED_HTML', [])
NEWS_BLOCKED_REGEX = re.compile(r'<(%s)[^>]*(/>|.*?</\1>)' % \
    ('|'.join(NEWS_BLOCKED_HTML)), re.S | re.I)


# default disallow feed items to have html in their titles
NEWS_NO_HTML_TITLES = getattr(settings, 'NEWS_NO_HTML_TITLES', True)


# number of days after which articles should be marked expired, 0 for never
NEWS_EXPIRE_ARTICLES_DAYS = getattr(settings, 'EXPIRE_ARTICLES', 7)


NEWS_ARTICLE_PAGINATION = getattr(settings, 'NEWS_ARTICLE_PAGINATION', 10)


# whoa secret!  used to trigger feed downloads remotely
NEWS_KEY = getattr(settings, 'NEWS_KEY', '')
