
from __future__ import with_statement


from mezzanine import template

register = template.Library()


@register.inclusion_tag("feeds/feeds_list.html", takes_context=True)
def feed_for(context, current_page):
    """
    Include the pagination template and data for persisting querystring in
    pagination links.
    """
    querystring = context["request"].GET.copy()
    if "page" in querystring:
        del querystring["page"]
    if "feed_id" in querystring:
        del querystring["feed_id"]
    querystring = querystring.urlencode()
    context.update( {"feeds_list": current_page, "querystring": querystring})
    return context


@register.inclusion_tag("common/includes/pagination.html", takes_context=True)
def article_for(context, current_page):
    """
    Include the pagination template and data for persisting querystring in
    pagination links.
    """
    querystring = context["request"].GET.copy()
    if "page" in querystring:
        del querystring["page"]
    querystring = querystring.urlencode()
    context.update({"current_page": current_page, "querystring": querystring})
    return context