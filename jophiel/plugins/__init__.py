
from .pools import BlockPool
from .items import RegisteredItem

block_pool = BlockPool()

def register(plugin_cls,**kwargs):
    item = RegisteredItem(**kwargs)
    plugin = plugin_cls(item)
    block_pool.register_plugin(plugin)