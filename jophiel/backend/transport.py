"""
kombu.transport
===============

Built-in transports.

:copyright: (c) 2009 - 2012 by Ask Solem.
:license: BSD, see LICENSE for more details.

"""
import sys

DEFAULT_TRANSPORT = "jophiel.backend.redis.Transport"

_transport_cache = {}

def resolve_transport(transport=None):
    transport_module_name, _, transport_cls_name = transport.rpartition(".")
    if not transport_module_name:
        raise KeyError("No such transport: %s" % (transport, ))
    return transport_module_name, transport_cls_name

def _get_transport_cls(transport=None):
    transport_module_name, transport_cls_name = resolve_transport(transport)
    __import__(transport_module_name)
    transport_module = sys.modules[transport_module_name]
    print transport_module
    return getattr(transport_module, transport_cls_name)


def get_transport_cls(transport=None):
    """Get transport class by name.

    The transport string is the full path to a transport class, e.g.::

        "kombu.transport.amqplib.Transport"

    If the name does not include `"."` (is not fully qualified),
    the alias table will be consulted.

    """
    transport = DEFAULT_TRANSPORT
    if transport not in _transport_cache:
        _transport_cache[transport] = _get_transport_cls(transport)
    return _transport_cache[transport]
