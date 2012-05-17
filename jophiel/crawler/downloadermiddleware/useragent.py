"""Set User-Agent header per spider or use a default value from settings"""

from jophiel.crawler.conf import USER_AGENT

def user_agent(spider):
    if hasattr(spider, 'user_agent'):
        return spider.user_agent
    return USER_AGENT

class UserAgentMiddleware(object):
    """This middleware allows spiders to override the user_agent"""    
    
    @classmethod
    def process_request(self, request, spider):
        ua = user_agent(spider)
        if ua:
            request.headers.setdefault('User-Agent', ua)
