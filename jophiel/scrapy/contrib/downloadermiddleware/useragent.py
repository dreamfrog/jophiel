"""Set User-Agent header per spider or use a default value from settings"""

from scrapy.utils.python import WeakKeyCache

from scrapy.middleware import BaseMiddleware

class UserAgentMiddleware(BaseMiddleware):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, settings):
        super(UserAgentMiddleware, self).__init__(settings)
        self.cache = WeakKeyCache(self._user_agent)

    def _user_agent(self, spider):
        if hasattr(spider, 'user_agent'):
            return spider.user_agent
        return spider.settings['USER_AGENT']

    def process_request(self, request, spider):
        ua = self.cache[spider]
        if ua:
            request.headers.setdefault('User-Agent', ua)
