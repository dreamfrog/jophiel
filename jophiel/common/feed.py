'''
Created on 2012-4-13

@author: lzz
'''

from jophiel.contrib.feedparser import feedparser
from jophiel.contrib.feedparser import sanitize
from jophiel.logger import log

from .items import TypeItem
from .html import escape
from .encoding import utf8
from .dateutil import get_as_date

def fetch_feed(url,agent = None,etag = None,modified  = None ):
    values = feedparser.parse(url,agent=agent,etag= etag,
                         modified=modified)
    return values

def get_feed_date(key,data):
    if not key.endswith("_parsed"):
        key += "_parsed"
    if data.has_key(key):
        return get_as_date(data[key])
    return None 
            

def parse_feed_basic():pass

"""
    analysis the parsed feed 
"""

IGNORE_KEYS = ("links", "contributors", "textinput", "cloud", "categories",
           "url", "href", "url_etag", "url_modified", "tags", "itunes_explicit")   

def parse_feed_meta(url,feed,egnore_keys = IGNORE_KEYS,):
    result = TypeItem()
    for key in feed.keys():
        if key in egnore_keys or key + "_parsed" in egnore_keys:
            # Ignored fields
            pass
        elif feed.has_key(key + "_parsed"):
            # Ignore unparsed date fields
            pass
        elif key.endswith("_detail"):
            # retain name and  email sub-fields
            if feed[key].has_key('name') and feed[key].name:
                result.set_as_string(key.replace("_detail","_name"), \
                    feed[key].name)
            if feed[key].has_key('email') and feed[key].email:
                result.set_as_string(key.replace("_detail","_email"), \
                    feed[key].email)
        elif key == "items":
            # Ignore items field
            pass
        elif key.endswith("_parsed"):
            # Date fields
            if feed[key]:
                result.set_as_date(key[:-len("_parsed")], feed[key])
        elif key == "image":
            # Image field: save all the information
            if feed[key].has_key("url"):
                result.set_as_string(key + "_url", feed[key].url)
            if feed[key].has_key("link"):
                result.set_as_string(key + "_link", feed[key].link)
            if feed[key].has_key("title"):
                result.set_as_string(key + "_title", feed[key].title)
            if feed[key].has_key("width"):
                result.set_as_string(key + "_width", str(feed[key].width))
            if feed[key].has_key("height"):
                result.set_as_string(key + "_height", str(feed[key].height))
        elif isinstance(feed[key], (str, unicode)):
            # String fields
            try:
                detail = key + '_detail'
                if feed.has_key(detail) and feed[detail].has_key('type'):
                    if feed[detail].type == 'text/html':
                        feed[key] = sanitize.HTML(feed[key])
                    elif feed[detail].type == 'text/plain':
                        feed[key] = escape(feed[key])
                result.set_as_string(key, feed[key])
            except KeyboardInterrupt:
                raise
            except:
                log.exception("Ignored '%s' of <%s>:<%s>, unknown format",key, url,feed[key])

def parse_feed_content(self,entry):
    """Update the item from the feedparser entry given."""
    result = TypeItem()
    for key in entry.keys():
        real_key = key
        if key =="id":
            continue
        if key.endswith("_parsed"):
            real_key = key[:-len("_parsed")]
        if not hasattr(self,real_key):
            continue
                
        if key in self.IGNORE_KEYS or key + "_parsed" in self.IGNORE_KEYS:
            # Ignored fields
            pass
        elif entry.has_key(key + "_parsed"):
            # Ignore unparsed date fields
            pass
        elif key.endswith("_detail"):
            # retain name, email, and language sub-fields
            if entry[key].has_key('name') and entry[key].name:
                result.set_as_string(key.replace("_detail","_name"), \
                    entry[key].name)
            if entry[key].has_key('email') and entry[key].email:
                result.set_as_string(key.replace("_detail","_email"), \
                    entry[key].email)
            if entry[key].has_key('language') and entry[key].language and \
               (not self._channel.has_key('language') or \
               entry[key].language != self._channel.language):
                result.set_as_string(key.replace("_detail","_language"), \
                    entry[key].language)
        elif key.endswith("_parsed"):
            # Date fields
            if entry[key] is not None:
                result.set_as_date(key[:-len("_parsed")], entry[key])
        elif key == "source":
            # Source field: save both url and value
            if entry[key].has_key("value"):
                result.set_as_string(key + "_name", entry[key].value)
            if entry[key].has_key("url"):
                result.set_as_string(key + "_link", entry[key].url)
        elif key == "content":
            # Content field: concatenate the values
            value = ""
            for item in entry[key]:
                if item.type == 'text/html':
                    item.value = sanitize.HTML(item.value)
                elif item.type == 'text/plain':
                    item.value = escape(item.value)
                if item.has_key('language') and item.language and \
                   (not self._channel.has_key('language') or
                   item.language != self._channel.language) :
                    self.set_as_string(key + "_language", item.language)
                value += utf8(item.value)
            result.set_as_string(key, value)
        elif isinstance(entry[key], (str, unicode)):
            # String fields
            try:
                detail = key + '_detail'
                if entry.has_key(detail):
                    if entry[detail].has_key('type'):
                        if entry[detail].type == 'text/html':
                            entry[key] = sanitize.HTML(entry[key])
                        elif entry[detail].type == 'text/plain':
                            entry[key] = escape(entry[key])
                result.set_as_string(key, entry[key])
            except KeyboardInterrupt:
                raise
            except:
                log.exception("Ignored '%s' of <%s>, unknown format",key, self.id)
    return result

def parse_feed_status(info):
    if info.has_key("status"):
        url_status = str(info.status)
    elif info.has_key("entries") and len(info.entries)>0:
        url_status = str(200)
    elif info.bozo and info.bozo_exception.__class__.__name__=='Timeout':
        url_status = str(408)
    else:
        url_status = str(500)    
    return url_status            