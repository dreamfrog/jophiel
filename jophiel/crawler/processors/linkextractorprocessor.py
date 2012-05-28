'''
Created on 2012-5-3

@author: lzz
'''
import copy
from .base import BaseProcessor
from ..linkextractors.sgml import SgmlLinkExtractor

"""
    rules to extract links in Response,
    params:
        allow:allowed url regrex pattern
        deny: denied url regrex pattern
        allow_domain: allowed url domain
        deny_domains: denied url domains
"""
class Rule(object):
    
    def __init__(self,allow=(), deny=(), allow_domains=(), deny_domains=(),
                  restrict_xpaths=(),**kwargs):
        self.link_extractor = SgmlLinkExtractor(allow=allow, deny=deny, allow_domains=allow_domains,
                                deny_domains=deny_domains, restrict_xpaths=restrict_xpaths, 
                            )
    
    def extract_links(self,response):
        return self.link_extractor.extract_links(response)
        
"""
    used for extract url links from response
"""
class LinkExtractorProcessor(BaseProcessor):
    
    """
        rules = [{"allow":"","deny":""}]
    """
    def __init__(self,rules,*args,**kwargs):
        super(LinkExtractorProcessor,self).__init__(*args,**kwargs)
        self._compile_rules(rules)
 
    def _compile_rules(self,rules):
        self._rules = []
        for rule in rules:
            r = Rule(**rule)
            self._rules.append(r)
        
    def process_item(self, request,response, spider):
        results = []
        for rule in self._rules:
            links = rule.extract_links()
            results.extend(results)
        return results
        