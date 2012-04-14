'''
Created on 2012-4-13

@author: lzz
'''
from jophiel.contrib.scrapely import extractors

def get_text_summary(html):
    t = lambda s: extractors.text(extractors.htmlregion(s))
    return t(html)