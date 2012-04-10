from django.contrib import admin
from .models import Planet, Feed, Article
from .models import FeedMeta,UserFeeds


class FeedAdmin(admin.ModelAdmin):
    list_display = ('id','name','url','active','updated')

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'publish'
    list_display = ('id','publish', 'title')
    search_fields = ['title', 'content']

class FeedMetaAdmin(admin.ModelAdmin):
    list_display = ('feed','name', 'title','image_url','image_link')
    search_fields = ['name', 'title']

class UserFeedsAdmin(admin.ModelAdmin):
    list_display = ('user','feed')

admin.site.register(Planet)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(FeedMeta,FeedMetaAdmin)
admin.site.register(UserFeeds,UserFeedsAdmin)
