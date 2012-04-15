'''
Created on 2012-4-14

@author: lzz
'''


# Copyright (c) 2010 by Yaco Sistemas
#
# This file is part of Merengue.
#
# Merengue is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Merengue is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Merengue.  If not, see <http://www.gnu.org/licenses/>.

from django import template
from django.conf import settings
from django.template.loader import render_to_string
from jophiel.plugins import block_pool

register = template.Library()

class RenderBlockNode(template.Node):

    def __init__(self, block):
        self.block = block

    def render(self, context):
        request = context.get('request', None)
        block = self.block
        if not block:
            return ''
        try:
            place = ''
            render_args = [request, place,context,]
            return block.get_rendered_content(request, render_args)
        except template.VariableDoesNotExist:
            return ''
        
@register.tag(name='render_block')
def do_render_block(parser, token):
    """
    Usage::
      {% render_single_block "block_name" %}
    """
    bits = token.split_contents()
    tag_name = bits[0]
    if len(bits) != 2:
        raise template.TemplateSyntaxError('"%r" tag requires two '
                                           'arguments' % tag_name)
    block_name = bits[1][1:-1]
    block = block_pool.get_plugin(block_name)
    return RenderBlockNode(block)

