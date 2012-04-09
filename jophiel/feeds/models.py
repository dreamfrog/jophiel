import datetime
import feedparser
import re
import time
import md5

from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from .constants import (NEWS_EXPIRE_ARTICLES_DAYS, 
                        NEWS_BLOCKED_HTML,NEWS_BLOCKED_REGEX, NEWS_NO_HTML_TITLES)
from . import config
from jophiel.contrib.feedparser import feedparser as parser
from jophiel.contrib import feedparser
from jophiel.contrib.feedparser import sanitize
from jophiel.contrib.scrapely import extractors,htmlpage

import logging
log = logging.getLogger("jophiel.news")
       
class Feed(models.Model):
    """
    A feed is the actual RSS/Atom feed that will be downloaded
    """
    name = models.CharField(max_length=255,default = "")
    url = models.URLField(unique = True)
    orig_url = models.URLField(blank=True)
    
    active = models.BooleanField(default=True)
    
    url_etag = models.CharField(max_length=255,default = "") #E-Tag of the feed URL.
    url_modified = models.DateTimeField(blank = True,auto_now_add=True) #Last modified time of the feed URL.
    url_status = models.CharField(max_length=100,default = "200") #Last HTTP status of the feed URL.

    updated = models.DateTimeField(blank = True,auto_now_add = True) # Correct UTC-Normalised update time of the feed.
    last_updated = models.DateTimeField(blank = True,auto_now_add = True) #Correct UTC-Normalised time the feed was last updated.
    
    #feed other info
    title = models.TextField(default = "")    #One-line title (*).
    author = models.CharField(max_length=255,default="") #Name of the author (*).
    link = models.URLField(blank=True)  
    image_url = models.URLField(blank = True) # URL of an associated image (*).
    image_link = models.URLField(blank = True) #Link to go with the associated image (*).
    image_title = models.CharField(max_length=255,default="") #Alternative text of the associated image (*).
     
    article_num = models.IntegerField(default = 0)
     
    class Meta:
        ordering = ('name',)

    def feed_information(self):
        """Returns a description string for the feed embedded in this channel."""
        return "<%s>:<%s>" %(self.name,self.url)
    
    def __unicode__(self):
        return u'%s' % (self.name)

    def has_item(self, id_):
        """Check whether the item exists in the channel."""
        if self.articles.get(article_id = id_):
            return True
        return False

    def get_item(self, id_):
        """Return the item from the channel."""
        article = None
        try:
            article  = Article.objects.get(article_id=id_)
        except ObjectDoesNotExist:
            return None
        return article
    
    def fetch_feed(self):
        info = parser.parse(self.url,
                                etag=self.url_etag, modified=self.url_modified,
                                agent=config.user_agent)
        return info

    def update_entry(self,info):
        
        if info.has_key("status"):
            self.url_status = str(info.status)
        elif info.has_key("entries") and len(info.entries)>0:
            self.url_status = str(200)
        elif info.bozo and info.bozo_exception.__class__.__name__=='Timeout':
            self.url_status = str(408)
        else:
            self.url_status = str(500)
        """
        todo:the feed moved need to be processed 
        """
        if self.url_status == '301' and \
           (info.has_key("entries") and len(info.entries)>0):
            log.warning("Feed has moved from <%s> to <%s>", self.url, info.url)
            self.orig_url = self.url
            self.url = info.url
            
        elif self.url_status == '304':
            log.info("Feed %s unchanged", self.feed_information())
            return
        elif self.url_status == '410':
            log.info("Feed %s gone", self.feed_information())
            return
        elif self.url_status == '408':
            log.warning("Feed %s timed out", self.feed_information())
            return
        elif int(self.url_status) >= 400:
            log.error("Error %s while updating feed %s",
                      self.url_status, self.feed_information())
            return
        else:
            log.info("Updating feed %s", self.feed_information())

        self.url_etag = info.has_key("etag") and info.etag or ""
        if info.has_key("modified_parsed") and info.modified_parsed:
            self.url_modified = feedparser.get_as_date(info.modified_parsed) 
        
        #log.debug("E-Tag: %s,Last Modified: %s", self.url_etag,time.strftime(config.TIMEFMT_ISO, self.url_modified))
                
    def update_articles(self, entries):
        """Update entries from the feed.
        """
        if not len(entries):
            return 0

        self.last_updated = self.updated
        self.updated = datetime.datetime.now()
        article_num = 0
        for entry in entries:
            try:
                entry_id = Article.get_entry_id(self.url,entry)
                if not entry_id:
                    log.error("Unable to find or generate id, entry ignored")
                    continue
                
                # Create the item if necessary and update
                item = self.get_item(entry_id)
                if not item:
                    item = self.articles.create(article_id = entry_id) 
                item.update_entry(entry)
                item.save()
                article_num +=1
            except:
                log.error("article can not be added",exc_info=True,)
        return article_num
    
    def update_feed(self,data):
        
        self.update_entry(data)
        self.save()
        feedmeta = FeedMeta.objects.filter(feed = self)
        if "feed" in data:
            if not feedmeta:
                feedmeta = FeedMeta()
                feedmeta.feed = self
            else:
                feedmeta = feedmeta[0]
            feedmeta.update_entity(data.feed) 
        
            #add some duplicate infomation in feeds
            self.title = feedmeta.title
            self.author = feedmeta.author
            self.image_title = feedmeta.image_title
            self.image_link = feedmeta.image_link
            self.image_url = feedmeta.image_url
        
        entry_num = 0
        if "entries" in data:
            entry_num = self.update_articles(data.entries)
        self.article_num += entry_num
        self.save()  
                       
    def process_feed(self):
        data = self.fetch_feed()
        self.update_feed(data)

    def get_title(self):
        for name in ("name","title","url"):
            value = getattr(self,name)
            if value:
                return value
    
    def get_owner_link(self):
        return self.link
    
    def get_article_num(self):
        return self.article_num
    
class FeedMeta(models.Model):
    name = models.CharField(max_length=255,blank=True)  #Name of the feed owner, or feed title.   
    modified =  models.DateTimeField(null = True)  # Date the feed claims to have been modified (*).
    title = models.TextField(default = "") #One-line title (*).
    link = models.URLField(blank=True) #Link to the original format feed (*).
    tagline = models.TextField(default = "") #Short description of the feed (*).
    info = models.TextField(default = "") #Longer description of the feed (*). 
    
    author = models.CharField(max_length=255,default="") #Name of the author (*).
    publisher = models.CharField(max_length=255,default="") #Name of the publisher (*).
    generator = models.CharField(max_length=255,default="") #Name of the feed generator (*).
    category = models.CharField(max_length=255,default="") # Category name (*).
    copyright = models.CharField(max_length=255,default="") # Copyright information for humans to read (*).
    license = models.CharField(max_length=255,default="") #Link to the licence for the content (*).
    docs = models.CharField(max_length=255,default = "") #Link to the specification of the feed format (*).
    language = models.CharField(max_length=255,default="") #Primary language (*).
    errorreportsto = models.CharField(max_length=255,default="") #E-Mail address to send error reports to (*).

    image_url = models.URLField(blank = True) # URL of an associated image (*).
    image_link = models.URLField(blank = True) #Link to go with the associated image (*).
    image_title = models.CharField(max_length=255,default="") #Alternative text of the associated image (*).
    image_width = models.IntegerField(default = 0) # Width of the associated image (*).
    image_height = models.IntegerField(default = 0) # Height of the associated image (*).

    feed = models.OneToOneField(Feed,primary_key=True) 

    IGNORE_KEYS = ("links", "contributors", "textinput", "cloud", "categories",
               "url", "href", "url_etag", "url_modified", "tags", "itunes_explicit")        
    
    def update_entity(self, feed):
        """Update information from the feed.
        """
        result = feedparser.PrettyItem()

        for key in feed.keys():
            if key in self.IGNORE_KEYS or key + "_parsed" in self.IGNORE_KEYS:
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
                            feed[key] = feedparser.escape(feed[key])
                    result.set_as_string(key, feed[key])
                except KeyboardInterrupt:
                    raise
                except:
                    log.exception("Ignored '%s' of <%s>:<%s>, unknown format",key, self.url,feed[key])
        try:
            feedparser.save_attr(self, result)
            self.save() 
        except:
            log.error("feed met info can not be add:%s",feed,exc_info=True,)
                 
class Planet(models.Model):
    """
    A source is a general news source, like CNN, who may provide multiple feeds.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    owner_url = models.URLField(blank = True)   
    owner_name= models.CharField(max_length=255,blank=True)
    owner_email = models.EmailField(max_length=255,blank = True)
        
    logo = models.ImageField(blank=True, upload_to='images/news_logos')
    feeds  = models.ManyToManyField(Feed)
        
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return u'%s' % self.name


class ArticleManager(models.Manager):
    
    def expired_articles(self):
        if NEWS_EXPIRE_ARTICLES_DAYS:
            delta = datetime.timedelta(days=NEWS_EXPIRE_ARTICLES_DAYS)
            expire_date = datetime.datetime.now() - delta
            return self.filter(date_added__lt=expire_date)
        else:
            return self.none()
        
    def expire_articles(self):
        return self.expired_articles().update(expired=True)

class Article(models.Model):
    
    objects = ArticleManager()
    
    article_id = models.CharField(max_length=255,unique = True) #Channel-unique identifier for this item.
    id_hash = models.CharField(max_length=255)  #Relatively short, printable cryptographic hash of id
    
    publish = models.DateTimeField(auto_now_add=True)  #Corrected UTC-Normalised update time, for sorting.
    date_added = models.DateTimeField(auto_now_add=True)   
        
    hidden = models.CharField(max_length=255,default = False) #Item should be hidden (True if exists).
    isexpired = models.BooleanField(default = False)
    
    title = models.CharField(max_length=255,default ="")  #One-line title (*).
    link = models.URLField(blank = True)   #Link to the original format text (*).
    summary = models.TextField(default = "")  #Short first-page summary (*).
    content = models.TextField(default = "")  #Full HTML content.
    description = models.TextField(default = "") 

    modified = models.DateTimeField(null = True) #   Date the item claims to have been modified (*).
    issued = models.DateTimeField(null=True) #     Date the item claims to have been issued (*).
    created = models.DateTimeField(null=True) #    Date the item claims to have been created (*).
    expired = models.DateTimeField(null=True) #    Date the item claims to expire (*).
    updated = models.DateTimeField(null=True) #   Date the item claims to have been modified (*).

    author = models.CharField(max_length=255,blank = True) #      Name of the author (*).
    publisher = models.CharField(max_length=255,blank = True) #   Name of the publisher (*).
    category = models.CharField(max_length=255,blank = True) #    Category name (*).
    comments = models.CharField(max_length=255,blank = True) #    Link to a page to enter comments (*).
    license = models.CharField(max_length=255,blank = True) #    Link to the licence for the content (*).
   
    source_name = models.CharField(max_length=255,blank = True) #   Name of the original source of this item (*).
    source_link = models.URLField(blank = True) #   Link to the original source of this item (*).

    feed = models.ForeignKey(Feed, related_name='articles')    

    IGNORE_KEYS = ("categories", "contributors", "enclosures", "links",
                   "guidislink", "date", "tags")
    
    class Meta:
        ordering = ('publish', 'title')
    
    def __unicode__(self):
        return u'%s' % self.title
    
    @classmethod
    def get_entry_id(cls,url,entry):
        entry_id = None
        if entry.has_key("id"):
            entry_id = entry.id
        elif entry.has_key("link"):
            entry_id = entry.link
        elif entry.has_key("title"):
            entry_id = (url + "/" + md5.new(feedparser.utf8(entry.title)).hexdigest())
        elif entry.has_key("summary"):
            entry_id = (url + "/" + md5.new(feedparser.utf8(entry.summary)).hexdigest()) 
        return entry_id 
    

    def update_entry(self, entry):
        """Update the item from the feedparser entry given."""
        result = feedparser.PrettyItem()
        
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
                        item.value = feedparser.escape(item.value)
                    if item.has_key('language') and item.language and \
                       (not self._channel.has_key('language') or
                       item.language != self._channel.language) :
                        self.set_as_string(key + "_language", item.language)
                    value += feedparser.utf8(item.value)
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
                                entry[key] = feedparser.escape(entry[key])
                    result.set_as_string(key, entry[key])
                except KeyboardInterrupt:
                    raise
                except:
                    import traceback 
                    traceback.print_exc()
                    #log.exception("Ignored '%s' of <%s>, unknown format",
                    #              key, self.id)
        # Generate the date field if we need to
        result.set_as_date("publish",self.get_publish(entry))
        feedparser.save_attr(self, result)
        self.save()
 
    def get_absolute_url(self):
        return self.link
          
    def get_publish(self, item):
        """Get (or update) the date key.
        """
        date = None
        for other_key in ("updated_", "modified", "published","date","issued", "created"):
            parsed_key = other_key+"_parsed"
            if item.has_key(parsed_key):
                date = item.get(parsed_key)
                break    
        if date:
            return date

        return time.gmtime()

    def get_summary(self):
        for key in ("summary","content","description"):
            if hasattr(self,key) and getattr(self,key):
                return getattr(self,key)
        return u""
    
    def get_summary_text(self):
        t = lambda s: extractors.text(extractors.htmlregion(s))
        html = self.get_summary()
        return t(html)
    
    def get_content(self):
        """Return the key containing the content."""
        for key in ("content", "tagline", "summary"):
            if hasattr(self,key) and getattr(self,key):
                return getattr(self,key)
        return ""
