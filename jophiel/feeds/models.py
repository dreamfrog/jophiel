import datetime
import re
import time
import md5

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from jophiel import config 
from jophiel.contrib import feedparser
from jophiel.contrib.feedparser import sanitize
from jophiel.contrib.scrapely import extractors,htmlpage

from jophiel.common.feed import parse_feed_meta,parse_feed_content,parse_feed_status,get_feed_date
from jophiel.common import dateutil
from jophiel.common.encoding import utf8
from jophiel.common.summary import get_text_summary

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
             
    user = models.ManyToManyField(User,through = "UserFeeds")
     
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return u'%s' % (self.url)
    
    def update_info(self,status,info):        
        self.url_status = status
        
        if self.url_status in ('304','410','408'):
            log.warning("Feed %s: status = s% ", self.url_status,self)
            return            
        elif int(self.url_status) >= 400:
            log.error("Error %s while updating feed %s",self.url_status, self)
            return   
             
        #todo:the feed moved need to be processed 
        if self.url_status == '301' and \
           (info.has_key("entries") and len(info.entries)>0):
            log.warning("Feed has moved from <%s> to <%s>", self.url, info.url)
            self.orig_url = self.url
            self.url = info.url
            
        log.info("Updating feed %s", self)
        self.url_etag = info.has_key("etag") and info.etag or ""
        modify = get_feed_date("modified_parsed",info)
        if modify:
            self.url_modified = modify
        self.save()
        
           
    def update_articles(self, entries):
        """Update entries from the feed.
        """
        self.last_updated = self.updated
        self.updated = dateutil.now()
        article_num = 0
        for entry in entries:
            try:
                entry_id = Article.get_entry_id(self.url,entry)
                if not entry_id:
                    log.error("Unable to find or generate id, entry ignored")
                    continue
                item,created = Article.objects.get_or_create(article_id = entry_id)
                item.update_entry(entry)
                item.save()
                if created:
                    article_num +=1
            except:
                log.error("article can not be added",exc_info=True,)
        log.info("update articles  = %s",str(article_num))
        return article_num
    
    def process_feed(self,data):
        status = parse_feed_status(data)
        self.update_info(status,data)
        feedmeta = FeedMeta.objects.get_or_create(feed = self)
        
        created_num = 0
        if "entries" in data:
            created_num = self.update_articles(data.entries) 
                
        if "feed" in data:
            feedmeta.update_entity(data.feed,created_num) 
        
            #add some duplicate infomation in feeds
            self.title = feedmeta.title
            self.author = feedmeta.author
            self.image_title = feedmeta.image_title
            self.image_link = feedmeta.image_link
            self.image_url = feedmeta.image_url
            self.article_num = feedmeta.article_num
        


    def get_title(self):
        for name in ("name","title","url"):
            value = getattr(self,name)
            if value:
                return value
    
    def get_owner_link(self):
        return self.link
    
    def get_article_num(self):
        return self.article_num

class UserFeeds(models.Model):
    user = models.ForeignKey(User)
    feed = models.ForeignKey(Feed)
    date_joined = models.DateField(auto_now_add = True)
    alias_name = models.CharField(max_length = 255,blank = True)
    
class FeedMeta(models.Model):
    name = models.CharField(max_length=255,blank=True)
    modified =  models.DateTimeField(null = True)  # Date the feed claims to have been modified
    title = models.TextField(default = "") #feed title (*).
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
    
    article_num = models.IntegerField(default = 0)
    
    feed = models.OneToOneField(Feed,primary_key=True)     
    
    def update_entity(self, feed,created_num):
        """Update information from the feed.
        """
        meta = parse_feed_meta(self.link,feed)
        try:
            self.article_num +=created_num
            self.save_attr(self)
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
            entry_id = (url + "/" + md5.new(utf8(entry.title)).hexdigest())
        elif entry.has_key("summary"):
            entry_id = (url + "/" + md5.new(utf8(entry.summary)).hexdigest()) 
        return entry_id 
 
    def get_absolute_url(self):
        return self.link
          
    def get_publish(self, item):
        """Get (or update) the date key.
        """
        date = None
        for other_key in ("updated", "modified", "published","date","issued", "created"):
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
        return get_text_summary(self.get_summary())
    
    def get_content(self):
        """Return the key containing the content."""
        for key in ("content", "tagline", "summary"):
            if hasattr(self,key) and getattr(self,key):
                return getattr(self,key)
        return ""


    def update_entry(self, entry):
        result = parse_feed_content(entry)
        result.set_as_date("publish",self.get_publish(entry))
        result.save_attr(self)
        self.save()
