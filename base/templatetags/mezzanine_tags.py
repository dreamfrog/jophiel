
from __future__ import with_statement
import os
from urllib import urlopen, urlencode

from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Model
from django.template import Context, Template
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.utils.simplejson import loads
from django.utils.text import capfirst
from PIL import Image, ImageOps

from django import template

register = template.Library()


@register.inclusion_tag("common/includes/form_fields.html", takes_context=True)
def fields_for(context, form):
    """
    Renders fields for a form.
    """
    return {"form": form}


@register.filter
def is_installed(app_name):
    """
    Returns ``True`` if the given app name is in the
    ``INSTALLED_APPS`` setting.
    """
    return app_name in settings.INSTALLED_APPS


@register.inclusion_tag("includes/pagination.html", takes_context=True)
def pagination_for(context, current_page):
    """
    Include the pagination template and data for persisting querystring in
    pagination links.
    """
    querystring = context["request"].GET.copy()
    if "page" in querystring:
        del querystring["page"]
    querystring = querystring.urlencode()
    return {"current_page": current_page, "querystring": querystring}


@register.simple_tag
def thumbnail(image_url, width, height):
    """
    Given the URL to an image, resizes the image using the given width and
    height on the first time it is requested, and returns the URL to the new
    resized image. if width or height are zero then original ratio is
    maintained.
    """
    if not image_url:
        return ""

    image_url = unicode(image_url)
    if image_url.startswith(settings.MEDIA_URL):
        image_url = image_url.replace(settings.MEDIA_URL, "", 1)
    image_dir, image_name = os.path.split(image_url)
    image_prefix, image_ext = os.path.splitext(image_name)
    filetype = {".png": "PNG", ".gif": "GIF"}.get(image_ext, "JPEG")
    thumb_name = "%s-%sx%s%s" % (image_prefix, width, height, image_ext)
    thumb_dir = os.path.join(settings.MEDIA_ROOT, image_dir,
                             settings.THUMBNAILS_DIR_NAME)
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    thumb_path = os.path.join(thumb_dir, thumb_name)
    thumb_url = "%s/%s/%s" % (os.path.dirname(image_url),
                              settings.THUMBNAILS_DIR_NAME, thumb_name)

    # Abort if thumbnail exists or original image doesn't exist.
    if os.path.exists(thumb_path):
        return thumb_url
    elif not default_storage.exists(image_url):
        return image_url

    image = Image.open(default_storage.open(image_url))
    width = int(width)
    height = int(height)

    # If already right size, don't do anything.
    if width == image.size[0] and height == image.size[1]:
        return image_url
    # Set dimensions.
    if width == 0:
        width = image.size[0] * height / image.size[1]
    elif height == 0:
        height = image.size[1] * width / image.size[0]
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")
    try:
        image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
        image = image.save(thumb_path, filetype, quality=100)
        # Push a remote copy of the thumbnail if MEDIA_URL is
        # absolute.
        if "://" in settings.MEDIA_URL:
            with open(thumb_path, "r") as f:
                default_storage.save(thumb_url, File(f))
    except:
        return image_url
    return thumb_url



@register.simple_tag
def try_url(url_name):
    """
    Mimics Django's ``url`` template tag but fails silently. Used for url
    names in admin templates as these won't resolve when admin tests are
    running.
    """
    try:
        url = reverse(url_name)
    except NoReverseMatch:
        return ""
    return url
