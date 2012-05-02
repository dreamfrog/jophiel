"""
Default settings for all of Mezzanine's apps. Each of these can be
overridden in your project's settings module, just like regular
Django settings. The ``editable`` argument for each controls whether
the setting is editable via Django's admin.

Thought should be given to how a setting is actually used before
making it editable, as it may be inappropriate - for example settings
that are only read during startup shouldn't be editable, since changing
them would require an application reload.
"""

from django.conf import settings
from django.utils.translation import ugettext as _

from . import register_setting


register_setting(
    name="ACCOUNTS_ENABLED",
    description="If True, users can create an account.",
    editable=False,
    default=False,
)

register_setting(
    name="ADMIN_MENU_ORDER",
    description=_("Controls the ordering and grouping of the admin menu."),
    editable=False,
    default=(
        (_("Content"), ("pages.Page", "blog.BlogPost",
           "generic.ThreadedComment", (_("Media Library"), "fb_browse"),)),
        (_("Site"), ("sites.Site", "redirects.Redirect", "conf.Setting")),
        (_("Users"), ("auth.User", "auth.Group",)),
    ),
)

register_setting(
    name="ADMIN_REMOVAL",
    description=_("Unregister these models from the admin."),
    editable=False,
    default=(),
)


register_setting(
    name="BLOG_USE_FEATURED_IMAGE",
    description=_("Enable featured images in blog posts"),
    editable=False,
    default=False,
)

register_setting(
    name="BLOG_URLS_USE_DATE",
    label=_("Use date URLs"),
    description=_("If ``True``, URLs for blog post include the month and "
        "year. Eg: /blog/yyyy/mm/slug/"),
    editable=False,
    default=False,
)



dashboard_tags = (
    ("mezzanine_tags.app_list",),
    ("mezzanine_tags.recent_actions",),
    (),
)

register_setting(
    name="DASHBOARD_TAGS",
    description=_("A three item sequence, each containing a sequence of "
        "template tags used to render the admin dashboard."),
    editable=False,
    default=dashboard_tags,
)

register_setting(
    name="DEVICE_DEFAULT",
    description=_("Device specific template sub-directory to use as the "
        "default device."),
    editable=False,
    default="",
)

register_setting(
    name="DEVICE_USER_AGENTS",
    description=_("Mapping of device specific template sub-directory names to "
        "the sequence of strings that may be found in their user agents."),
    editable=False,
    default=(
        ("mobile", ("2.0 MMP", "240x320", "400X240", "AvantGo", "BlackBerry",
            "Blazer", "Cellphone", "Danger", "DoCoMo", "Elaine/3.0",
            "EudoraWeb", "Googlebot-Mobile", "hiptop", "IEMobile",
            "KYOCERA/WX310K", "LG/U990", "MIDP-2.", "MMEF20", "MOT-V",
            "NetFront", "Newt", "Nintendo Wii", "Nitro", "Nokia",
            "Opera Mini", "Palm", "PlayStation Portable", "portalmmm",
            "Proxinet", "ProxiNet", "SHARP-TQ-GX10", "SHG-i900",
            "Small", "SonyEricsson", "Symbian OS", "SymbianOS",
            "TS21i-10", "UP.Browser", "UP.Link", "webOS", "Windows CE",
            "WinWAP", "YahooSeeker/M1A1-R2D2", "iPhone", "iPod", "Android",
            "BlackBerry9530", "LG-TU915 Obigo", "LGE VX", "webOS",
            "Nokia5800",)
        ),
    ),
)

register_setting(
    name="EXTRA_MODEL_FIELDS",
    description=_("A sequence of fields that will be injected into "
        "Mezzanine's (or any library's) models. Each item in the sequence is "
        "a four item sequence. The first two items are the dotted path to the "
        "model and its field name to be added, and the dotted path to the "
        "field class to use for the field. The third and fourth items are a "
        "sequence of positional args and a dictionary of keyword args, to use "
        "when creating the field instance. When specifying the field class, "
        "the path ``django.models.db.`` can be omitted for regular Django "
        "model fields."),
    editable=False,
    default=(),
)

register_setting(
    name="FORMS_DISABLE_SEND_FROM_EMAIL_FIELD",
    description=_("If ``True``, emails sent to extra recipients for form "
        "submissions won't be sent from an address taken from one of the "
        "form's email fields."),
    editable=False,
    default=False,
)

register_setting(
    name="FORMS_FIELD_MAX_LENGTH",
    description=_("Max length allowed for field values in the forms app."),
    editable=False,
    default=2000,
)

register_setting(
    name="FORMS_LABEL_MAX_LENGTH",
    description=_("Max length allowed for field labels in the forms app."),
    editable=False,
    default=200,
)

register_setting(
    name="FORMS_USE_HTML5",
    description=_("If ``True``, website forms created by the forms app will "
        "use HTML5 features."),
    editable=False,
    default=False,
)

register_setting(
    name="FORMS_CSV_DELIMITER",
    description=_("Char to use as a field delimiter when exporting form "
        "responses as CSV."),
    editable=False,
    default=",",
)

register_setting(
    name="FORMS_UPLOAD_ROOT",
    description=_("Absolute path for storing file uploads for the forms app."),
    editable=False,
    default="",
)

register_setting(
    name="GOOGLE_ANALYTICS_ID",
    label=_("Google Analytics ID"),
    editable=True,
    description=_("Google Analytics ID (http://www.google.com/analytics/)"),
    default="",
)

register_setting(
    name="HOST_THEMES",
    description=_("A sequence mapping host names to themes, allowing "
                  "different templates to be served per HTTP hosts "
                  "Each item in the sequence is a two item sequence, "
                  "containing a host such as ``othersite.example.com``, and "
                  "the name of an importable Python package for the theme. "
                  "If the host is matched for a request, the templates "
                  "directory inside the theme package will be first searched "
                  "when loading templates."),
    editable=False,
    default=(),
)


register_setting(
    name="MAX_PAGING_LINKS",
    label=_("Max paging links"),
    description=_("Max number of paging links to display when paginating."),
    editable=True,
    default=10,
)

register_setting(
    name="PAGES_MENU_SHOW_ALL",
    description=_("If ``True``, the pages menu will show all levels of "
        "navigation, otherwise child pages are only shown when viewing the "
        "parent page."),
    editable=False,
    default=True,
)

register_setting(
    name="RATINGS_MIN",
    description=_("Min value for a rating."),
    editable=False,
    default=1,
)

register_setting(
    name="RATINGS_MAX",
    description=_("Max value for a rating."),
    editable=False,
    default=5,
)

register_setting(
    name="RICHTEXT_WIDGET_CLASS",
    description=_("Dotted package path and class name of the widget to use "
        "for the ``RichTextField``."),
    editable=False,
    default="mezzanine.core.forms.TinyMceWidget",
)

register_setting(
    name="RICHTEXT_FILTER",
    description=_("Dotted path to the function to call on a ``RichTextField`` "
        "value before it is rendered to the template."),
    editable=False,
    default=None,
)

register_setting(
    name="SEARCH_PER_PAGE",
    label=_("Search results per page"),
    description=_("Number of results shown in the search results page."),
    editable=True,
    default=10,
)


register_setting(
    name="SSL_ENABLED",
    label=_("Enable SSL"),
    description="If ``True``, users will be automatically redirected to HTTPS "
                "for the URLs specified by the ``SSL_FORCE_URL_PREFIXES`` "
                "setting.",
    editable=True,
    default=False,
)

register_setting(
    name="SSL_FORCE_HOST",
    label=_("Force Host"),
    description="Host name that the site should always be accessed via that "
                "matches the SSL certificate.",
    editable=True,
    default="",
)

register_setting(
    name="SSL_FORCE_URL_PREFIXES",
    description="Sequence of URL prefixes that will be forced to run over "
                "SSL when ``SSL_ENABLED`` is ``True``. i.e. "
                "('/admin', '/example') would force all URLs beginning with "
                "/admin or /example to run over SSL.",
    editable=False,
    default=("/admin", "/account"),
)

register_setting(
    name="TAG_CLOUD_SIZES",
    label=_("Tag Cloud Sizes"),
    description=_("Number of different sizes for tags when shown as a cloud."),
    editable=True,
    default=4,
)

register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=_("Sequence of setting names available within templates."),
    editable=False,
    default=(
        "ACCOUNTS_ENABLED", "ADMIN_MEDIA_PREFIX",
        "BLOG_BITLY_USER", "BLOG_BITLY_KEY",
        #"COMMENTS_DISQUS_API_PUBLIC_KEY", "COMMENTS_DISQUS_API_SECRET_KEY",
        #"DEV_SERVER", "FORMS_USE_HTML5", "GRAPPELLI_INSTALLED",
        #"GOOGLE_ANALYTICS_ID", "JQUERY_FILENAME", "LOGIN_URL", "LOGOUT_URL",
        #"PAGES_MENU_SHOW_ALL", "SITE_TITLE", "SITE_TAGLINE", "RATINGS_MAX",
    ),
)


register_setting(
    name="TINYMCE_SETUP_JS",
    description=_("URL for the JavaScript file (relative to ``STATIC_URL``) "
        "that handles configuring TinyMCE when the default "
        "``RICHTEXT_WIDGET_CLASS`` is used."),
    editable=False,
    default="mezzanine/js/tinymce_setup.js",
)

# The following settings are defined here for documentation purposes
# as this file is used to auto-generate the documentation for all
# available settings. They are Mezzanine specific, but their values
# are *always* overridden by the project's settings or local_settings
# modules, so the default values defined here will never be used.

register_setting(
    name="USE_SOUTH",
    description=_("If ``True``, the south application will be "
        "automatically added to the ``INSTALLED_APPS`` setting."),
    editable=False,
    default=True,
)

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