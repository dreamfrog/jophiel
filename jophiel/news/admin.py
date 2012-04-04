from django.contrib import admin
from .models import Planet, Feed, Article
from .models import FeedMeta


class FeedAdmin(admin.ModelAdmin):pass

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'publish'
    list_display = ('id','publish', 'title')
    search_fields = ['title', 'content']

admin.site.register(Planet)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(FeedMeta)
