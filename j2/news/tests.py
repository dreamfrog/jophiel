"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .utils import url_first_page_fetch,fetch_url_content

class SimpleTest(TestCase):
    #def testFetchContent(self):
    #    url = "http://cloud.csdn.net/a/20120412/2804464.html"
    #    links = url_first_page_fetch(url)
    #    for link in links:
    #        result = fetch_url_content(url)
    #        if result:
    #            summary,text =result
                #print text
    def testExtractContent(self):
        url = "http://data.book.163.com/book/section/000BNdDB/000BNdDB7.html?zhuanlan"
        result = fetch_url_content(url)
        if result:
            summary,text =result   
            print text       