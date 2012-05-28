from django.test import TestCase

from .models import Feed, Article


class FakeFeed(object):
    encoding = 'utf-8'
    
    def __init__(self):
        self.entries = []

class FakeFeedItem(dict):
    def __getattr__(self, attr):
        if self.__contains__(attr):
            return self[attr]
        raise AttributeError


class NewsTestCase(TestCase):
    fixtures = ['news_test_data']
    urls = 'news.news_tests.urls'
    
    fake_feed_data = {
        'Django': [],
        'Python': [],
        'Programming': [
            {'title': 'Git rules', 'summary': '<p>vcs troll</p>', 'link': '/git/'},
            {'title': 'Hg rules and its python', 'summary': '<p>trolled</p>', 'link': '/hg/'},
            {'title': 'Django stuff', 'summary': '', 'link': '/django/'},
            {'title': 'Python and Django rock', 'summary': '<p>Programming article about python and django</p>', 'link': '/p+d+rokk/'},
        ],
        'Geek': [
            {'title': 'Apple <b>gear</b>', 'summary': '<script>/* hax0r3d */</script>I <3 apple', 'link': '/apple/'},
            {'title': 'Homemade wallets', 'description': 'In forty three <b>easy</b> steps <iframe src="somesuch" />', 'link': '/wtf/'},
        ],
        'Hacker News RSS': [
            {'title': 'Being a startup', 'summary': 'damn hard', 'link': '/momoney/'},
            {'title': 'VC Angels', 'summary': 'where dey', 'link': '/whodat/'},
            {'title': 'A python article', 'summary': 'awesome', 'link': '/python/'},
            {'title': 'A django article', 'summary': 'awesome', 'link': '/django/'},
        ]
    }
    
    def get_feed(self, key):
        ff = FakeFeed()
        for item in self.fake_feed_data[key]:
            ff.entries.append(FakeFeedItem(item))
        return ff
    
    def setUp(self):
        #   /~\
        #  C oo
        #  _( ^)
        # /   ~\
        self.orig_fetch_feed = Feed.fetch_feed
        Feed.fetch_feed = lambda f: self.get_feed(f.name)
    
    def tearDown(self):
        Feed.fetch_feed = self.orig_fetch_feed
    
    def test_item_sanitization(self):
        feed = Feed.objects.get(name='Geek')
        feed_data = feed.fetch_feed()
        apple, wallet = feed_data.entries
        
        # apple article had some innocuous HTML in the title, but lets the
        # settings are configured to remove it, so do it.  also remove the
        # script tags within the summary
        apple_article = feed.convert_item(apple)
        self.assertEqual(apple_article.headline, 'Apple gear')
        self.assertEqual(apple_article.content, 'I <3 apple')
        self.assertEqual(apple_article.url, '/apple/')
        self.assertEqual(apple_article.guid, '/apple/')
        
        # here just making sure that the html blacklist will kill the iframe
        # tag while leaving the bold tags intact
        wallet_article = feed.convert_item(wallet)
        self.assertEqual(wallet_article.headline, 'Homemade wallets')
        self.assertEqual(wallet_article.content, 'In forty three <b>easy</b> steps ')
        self.assertEqual(wallet_article.url, '/wtf/')
        self.assertEqual(wallet_article.guid, '/wtf/')
    
    def test_for_duping(self):
        geek_data = self.fake_feed_data['Geek']
        geek = Feed.objects.get(name='Geek')
        geek.process_feed()
        
        self.assertEqual(Article.objects.count(), 2)
        
        geek_data[1]['title'] = 'Homemade wallets !!!'
        geek.process_feed()
        geek_data[1]['title'] = 'Homemade wallets'
        
        self.assertEqual(Article.objects.count(), 2)
        
        wallet = Article.objects.get(guid='/wtf/')
        self.assertEqual(wallet.headline, 'Homemade wallets !!!')
    
  
    def test_feed_repeatability(self):
        # feed fetching needs to be repeatable so it can get cron'd up, lets
        # test that
        feed = Feed.objects.get(name='Programming')
        results = feed.process_feed()
        self.assertEqual(results, 4)
        
        results = feed.process_feed()
        self.assertEqual(results, 0)
    
    def test_feed_processing(self):
        # double check that the articles are categorized properly even though
        # the underlying methods are covered elsewhere in the tests
        feed = Feed.objects.get(name='Programming')
        results = feed.process_feed()
        
        self.assertEqual(Article.objects.all().count(), 4)
        
        # load everything up from the db
        git = Article.objects.get(headline='Git rules')
        hg = Article.objects.get(headline='Hg rules and its python')
        dj = Article.objects.get(headline='Django stuff')
        py = Article.objects.get(headline='Python and Django rock')
        
    
    def test_list_view(self):
        feed = Feed.objects.get(name='Programming')
        results = feed.process_feed()
        
        resp = self.client.get('/news/')
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['categories']), 4)
        self.assertEqual(len(resp.context['article_list']), 4)
    
    def test_detail_view(self):
        feed = Feed.objects.get(name='Programming')
        results = feed.process_feed()
        
        resp = self.client.get('/news/programming/')
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['categories']), 4)
        self.assertEqual(len(resp.context['article_list']), 4)
        self.assertEqual(resp.context['category'].name, 'Programming')
        
        resp = self.client.get('/news/programming/python/')
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['categories']), 4)
        self.assertEqual(str(resp.context['article_list']), '[<Article: Python and Django rock>, <Article: Hg rules and its python>]')
        self.assertEqual(resp.context['category'].name, 'Python')
        
        resp = self.client.get('/news/programming/python/django/')
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['categories']), 4)
        self.assertEqual(str(resp.context['article_list']), '[<Article: Python and Django rock>, <Article: Django stuff>]')
        self.assertEqual(resp.context['category'].name, 'Django')

        resp = self.client.get('/news/programming/python/django/?q=rock')
        self.assertEqual(resp.context['search_query'], 'rock')
        self.assertEqual(str(resp.context['article_list']), '[<Article: Python and Django rock>]')
    
    def test_web_hook(self):
        resp = self.client.get('/news/run-download/?key=wrong')
        self.assertEqual(Article.objects.count(), 0)
        
        resp = self.client.get('/news/run-download/?key=test')
        self.assertEqual(Article.objects.count(), 10)
    
