'''
Created on 2012-2-15

@author: liu
'''

import re

from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.meta import StringField
from scrapy.meta import ListField

class CommonSpider(BaseSpider):

    spider_name = StringField(default="spider")
    start_urls = ListField(default=[])
    
    def __init__(self, settings, *a, **kw):
        super(BaseSpider, self).__init__(settings, *a, **kw)
        self.extractor = SgmlLinkExtractor()
        self.name = self.spider_name.to_value()
        self.start_urls = self.start_urls.to_value()

    def parse(self, response):
        print "beging", response.url
        results = []
        links = self.extractor.extract_links(response)
        for link in links:
            results.append(Request(link.url))

        return results
