'''
Created on 2012-4-1

@author: lzz
'''

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from scrapy.conf import settings
from .crawler import CrawlerProcess

from .taskspider import TaskSpider
from scrapy import log
      
def catch_item(sender, item, **kwargs):
    print "Got:", item
        
def start_crawl(task_name):
    spider = TaskSpider.load(task_name)
    """Setups item signal and run the spider"""
    dispatcher.connect(catch_item, signal=signals.item_passed)

    settings.overrides['LOG_ENABLED'] = False
    settings.overrides["LOG_STDOUT"] = False
    settings.overrides["LOG_LEVEL"] = 'DEBUG'
    #settings.overrides["LOG_FILE"] = "scrapy.log"
    print settings.defaults
    print settings["LOG_STDOUT"]
    if not log.started:
        log.start()
    # set up crawler
    crawler = CrawlerProcess(settings)
    crawler.configure()
    # schedule spider
    print spider.start_urls
    print spider.rules
    crawler.crawl(spider)

    print "STARTING ENGINE"
    crawler.start()
    print "ENGINE STOPPED"
    
if __name__=="__main__":
    start_crawl("dianping")