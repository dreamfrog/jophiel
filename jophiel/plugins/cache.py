'''
Created on 2012-4-14

@author: lzz
'''


from jophiel.contrib.cache import memoize, MemoizeCache
# ----- cache stuff -----
_registry_lookup_cache = MemoizeCache('registry_lookup_cache')

def _convert_cache_args(mem_args):
    item_class = mem_args[0]
    return ('%s.%s' % (item_class.get_module(), item_class.get_class_name()), )

def clear_lookup_cache():
    _registry_lookup_cache.clear()

