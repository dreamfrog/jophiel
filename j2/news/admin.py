'''
Created on 2012-4-11

@author: lzz
'''
from django.contrib import admin
from .models import UrlSeeds,ExtractResults

class TaskAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name', 'priority', 'created')
    list_filter = ('domain', 'priority', 'name')
    ordering = ['priority', 'created']
    search_fields = ('description', 'name')

admin.site.register(UrlSeeds)
admin.site.register(ExtractResults)