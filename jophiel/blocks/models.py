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

from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

import re


PLACES = (('all', _('All places')),
          ('leftsidebar', _('Left sidebar')),
          ('rightsidebar', _('Right sidebar')),
          ('aftercontenttitle', _('After content title')),
          ('beforecontent', _('Before content body')),
          ('homepage', _('Home page')),
          ('aftercontent', _('After content body')),
          ('header', _('Header')),
          ('footer', _('Footer')),
          ('meta', _('Meta-information, links, js...')))

PLACES_DICT = dict(PLACES)

class RegisteredBlock(object):
    name = None
    placed_at = "all"
    shown_in_urls = ""
    hidden_in_urls = ""
    is_fixed = False
    fixed_place = False
    # caching parameters
    is_cached = False
    cache_timeout = 0
    cache_only_anonymous = False
    cache_vary_on_user = False
    cache_vary_on_url = False
    cache_vary_on_language = True
    # fields for blocks related to contents
    content = ""
    overwrite_if_place = True
    overwrite_always = False

    def show_in_url(self, url):

        def _matches(url, exp):
            for e in exp:
                try:
                    urlre = re.compile(e, re.IGNORECASE)
                    if urlre.search(url):
                        return True
                except re.error, err:  # pyflakes:ignore
                    continue
            return False

        if self.shown_in_urls:
            return _matches(url, self.shown_in_urls.split())
        elif self.hidden_in_urls:
            return not _matches(url, self.hidden_in_urls.split())
        else:
            return True

    def print_block(self, placed_at, url):
        if self.placed_at in ['all', placed_at]:
            return self.show_in_url(url)
        return False

    def __unicode__(self):
        return self.name

