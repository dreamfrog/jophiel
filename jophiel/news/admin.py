from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name', 'priority', 'created')
    list_filter = ('domain', 'priority', 'name')
    ordering = ['priority', 'created']
    search_fields = ('description', 'name')

admin.site.register(Task, TaskAdmin)
