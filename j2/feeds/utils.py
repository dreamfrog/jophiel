'''
Created on 2012-4-14

@author: lzz
'''
from .models import Article
from . import defaults
from mezzanine.utils import views

def default_article_sql(feed_id = None):
    sql = """select feeds_article.* from feeds_article where 1=1 """        
    sql += "and feeds_article.feed_id = %s "%feed_id if feed_id else ""
    return sql
def fetch_default_article(feed_id):
    sql = default_article_sql(feed_id)
    qs = Article.objects.raw(sql) 
    return qs    

def user_article_sql(user,feed_id = None):
    sql = """select feeds_article.* from feeds_article ,feeds_feed,feeds_userfeeds 
                 where feeds_article.feed_id = feeds_feed.id and feeds_feed.id = feeds_userfeeds.feed_id  
                 and feeds_userfeeds.user_id = %s 
          """ %user.id   
    if feed_id:
        sql += "and feeds_article.feed_id = %s "%feed_id
    return sql  

def fetch_user_article(user,feed_id):
    sql = user_article_sql(user,feed_id)
    qs = Article.objects.raw(sql) 
    return qs


def process_page(request,qs,page_num):
    qs = views.paginate(qs,page_num,defaults.DEFAULT_PER_PAGE_NUM,defaults.DEFAULT_MAX_LINKS_PER_PAGE)
    return qs  