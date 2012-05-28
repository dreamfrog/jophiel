from django.contrib import admin
from .models import Spider

class SpiderAdmin(admin.ModelAdmin):
    list_display = ('name','description')

admin.site.register(Spider,SpiderAdmin)
