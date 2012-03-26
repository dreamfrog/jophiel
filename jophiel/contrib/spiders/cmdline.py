from __future__ import with_statement

from scrapy.crawler import CommonCrawler
from jophiel.spiders import CommonSpider

def execute(settings):
    #override settings
    """Our ad-hoc spider"""
    name = "myspider"
    start_urls = ["http://stackoverflow.com/"]
    
    settings = {
                "spiders.CommonSpider":{
                                        "spider_name":name,
                                        "start_urls":start_urls
                                        },
                "scrapy.crawler.CrawlerProcess":{  
                                                 },
                "scrapy.extension.ExtensionManager":{
                                                     
                                                     },
                "scrapy.spidermanager.SpiderManager":{
                                                      },
                "scrapy.core.engine.ExecutionEngine":{
                                                      },
                "scrapy.core.downloader.Downloader":{
                                                     },
                "scrapy.core.downloader.middleware.DownloaderMiddlewareManager":{
                                                                                 },
                "scrapy.core.spidermw.SpiderMiddlewareManager":{
                                            "middleware_lists":{
                                                'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware': 50,
                                                'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': 500,
                                                'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': 700,
                                                'scrapy.contrib.spidermiddleware.urllength.UrlLengthMiddleware': 800,
                                                'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': 900,
                                                }
                                                                
                                                                
                                        },
                "scrapy.core.scraper.Scraper":{
                                               },
                "scrapy.contrib.pipeline.ItemPipelineManager":{
                                                               },
                "scrapy.core.scheduler.Scheduler":{
                                                   },
                "scrapy.dupefilter.RFPDupeFilter":{
                                                   }
                }
    
    spider = CommonSpider(settings)
    crawler = CommonCrawler(settings, spider)
    crawler.run()


if __name__ == '__main__':
    from scrapy import settings
    execute(settings)
