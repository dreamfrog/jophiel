'''
Created on 2012-4-10

@author: lzz
'''
from django.conf import settings
from django.utils.translation import ugettext as _

from mezzanine.conf import register_setting


register_setting(
    name="SITE_TITLE",
    label=_("Site Title"),
    description=_("Title that will display at the top of the site, and be "
        "appended to the content of the HTML title tags on every page."),
    editable=True,
    default="Jophiel",
)

register_setting(
    name="SITE_TAGLINE",
    label=_("Tagline"),
    description=_("A tag line that will appear at the top of all pages."),
    editable=True,
    default=_("Web Information Aggregration"),
)


register_setting(
    name="JQUERY_FILENAME",
    label=_("Name of the jQuery file."),
    description=_("Name of the jQuery file found in "
                  "mezzanine/core/static/mezzanine/js/"),
    editable=False,
    default="jquery-1.7.1.min.js",
)
