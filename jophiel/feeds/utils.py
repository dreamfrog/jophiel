'''
Created on 2012-4-10

@author: lzz
'''
from jophiel.contrib.feedparser import feedparser as parser
from . import config

def fetch_feed(url):
    info = parser.parse(url,agent=config.user_agent
                            #etag=self.url_etag, modified=self.url_modified,
                        )
    return info