'''
Created on 2012-4-9

@author: lzz
'''
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from .models import Article,Feed

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }


#class EntryResource(ModelResource):
#    user = fields.ForeignKey(UserResource, 'user')
#
#    class Meta:
#        queryset = Entry.objects.all()
#        resource_name = 'entry'
#        authorization = Authorization()
#        filtering = {
#            'user': ALL_WITH_RELATIONS,
#            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
#        }


class ArticleResource(ModelResource):
    #user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Article.objects.all()
        resource_name = 'entry'