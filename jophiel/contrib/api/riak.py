'''
Created on 2012-4-9

@author: lzz
'''

from django.contrib.auth.models import User
from tastypie.resources import Resource
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.bundle import Bundle

# We need a generic object to shove data in/get data from.
# Riak generally just tosses around dictionaries, so we'll lightly
# wrap that.
class RiakObject(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data


class MessageResource(Resource):
    # Just like a Django ``Form`` or ``Model``, we're defining all the
    # fields we're going to handle with the API here.
    uuid = fields.CharField(attribute='uuid')
    user_uuid = fields.CharField(attribute='user_uuid')
    message = fields.CharField(attribute='message')
    created = fields.IntegerField(attribute='created')

    class Meta:
        resource_name = 'riak'
        object_class = RiakObject
        #authorization = Authorization()

    # Specific to this resource, just to get the needed Riak bits.
    def _client(self):pass
        #return riak.RiakClient()

    def _bucket(self):
        client = self._client()
        # Note that we're hard-coding the bucket to use. Fine for
        # example purposes, but you'll want to abstract this.
        return client.bucket('messages')

    # The following methods will need overriding regardless of your
    # data source.
    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uuid
        else:
            kwargs['pk'] = bundle_or_obj.uuid

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

    def get_object_list(self, request):
        query = self._client().add('messages')
        query.map("function(v) { var data = JSON.parse(v.values[0].data); return [[v.key, data]]; }")
        results = []

        for result in query.run():
            new_obj = RiakObject(initial=result[1])
            new_obj.uuid = result[0]
            results.append(new_obj)

        return results

    def obj_get_list(self, request=None, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        bucket = self._bucket()
        message = bucket.get(kwargs['pk'])
        return RiakObject(initial=message.get_data())

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.obj = RiakObject(initial=kwargs)
        bundle = self.full_hydrate(bundle)
        bucket = self._bucket()
        new_message = bucket.new(bundle.obj.uuid, data=bundle.obj.to_dict())
        new_message.store()
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        return self.obj_create(bundle, request, **kwargs)

    def obj_delete_list(self, request=None, **kwargs):
        bucket = self._bucket()

        for key in bucket.get_keys():
            obj = bucket.get(key)
            obj.delete()

    def obj_delete(self, request=None, **kwargs):
        bucket = self._bucket()
        obj = bucket.get(kwargs['pk'])
        obj.delete()

    def rollback(self, bundles):
        pass