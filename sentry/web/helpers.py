"""
sentry.web.views
~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import logging

from django.conf import settings as dj_settings
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse
from django.template import loader, RequestContext, Context
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe

from sentry.conf import settings
from sentry.models import ProjectMember, Project, View, \
  MEMBER_USER, Option, ProjectOption
from sentry.permissions import can_create_projects

logger = logging.getLogger('sentry.errors')


def get_project_list(user=None, access=None, hidden=False):
    """
    Returns a set of all projects a user has some level of access to.
    """
    if access is None:
        access = MEMBER_USER

    # If we're not requesting specific access include all
    # public projects
    if access <= MEMBER_USER:
        qs = Project.objects.filter(public=True)
        if not hidden:
            qs = qs.filter(status=0)
        projects = SortedDict((p.pk, p) for p in qs)
    else:
        projects = SortedDict()

    # If the user is authenticated, include their memberships
    if user and user.is_authenticated():
        qs = ProjectMember.objects.filter(user=user)\
              .select_related('project')
        if not hidden:
            qs = qs.filter(project__status=0)
        projects.update(SortedDict((pm.project_id, pm.project)
            for pm in qs if pm.type <= access))

    return projects

_LOGIN_URL = None


def get_login_url(reset=False):
    global _LOGIN_URL

    if _LOGIN_URL is None or reset:
        # if LOGIN_URL resolves force login_required to it instead of our own
        # XXX: this must be done as late as possible to avoid idempotent requirements
        try:
            resolve(dj_settings.LOGIN_URL)
        except:
            _LOGIN_URL = settings.LOGIN_URL
        else:
            _LOGIN_URL = dj_settings.LOGIN_URL

        if _LOGIN_URL is None:
            _LOGIN_URL = reverse('sentry-login')
    return _LOGIN_URL


def iter_data(obj):
    for k, v in obj.data.iteritems():
        if k.startswith('_') or k in ['url']:
            continue
        yield k, v


def get_default_context(request, existing_context=None):
    from sentry.plugins import plugins

    context = {
        'HAS_SEARCH': settings.USE_SEARCH,
        'MESSAGES_PER_PAGE': settings.MESSAGES_PER_PAGE,
        'PROJECT_ID': int(settings.PROJECT),
        'VIEWS': list(View.objects.all()),
        'URL_PREFIX': settings.URL_PREFIX,
        'PLUGINS': plugins,
        'USE_JS_CLIENT': settings.USE_JS_CLIENT,
    }

    if request:
        context.update({
            'request': request,
            'can_create_projects': can_create_projects(request.user),
        })
        if not existing_context or 'project_list' not in existing_context:
            context['project_list'] = get_project_list(request.user).values()

    return context


def render_to_string(template, context=None, request=None):
    default_context = get_default_context(request, context)

    if context is None:
        context = default_context
    else:
        context = dict(context)
        context.update(default_context)

    if request:
        context = RequestContext(request, context)
    else:
        context = Context(context)

    return loader.render_to_string(template, context)


def render_to_response(template, context=None, request=None, status=200):
    response = HttpResponse(render_to_string(template, context, request))
    response.status_code = status

    return response


def plugin_config(plugin, project, request):
    """
    Configure the plugin site wide.

    returns a tuple composed of a redirection boolean and the content to
    be displayed.
    """
    NOTSET = object()

    plugin_key = plugin.get_conf_key()
    if project:
        form_class = plugin.project_conf_form
        template = plugin.project_conf_template
    else:
        form_class = plugin.site_conf_form
        template = plugin.site_conf_template

    initials = plugin.get_form_initial(project)
    for field in form_class.base_fields:
        key = '%s:%s' % (plugin_key, field)
        if project:
            value = ProjectOption.objects.get_value(project, key, NOTSET)
        else:
            value = Option.objects.get_value(key, NOTSET)
        if value is not NOTSET:
            initials[field] = value

    form = form_class(
        request.POST or None,
        initial=initials,
        prefix=plugin_key
    )
    if form.is_valid():
        for field, value in form.cleaned_data.iteritems():
            key = '%s:%s' % (plugin_key, field)
            if project:
                ProjectOption.objects.set_value(project, key, value)
            else:
                Option.objects.set_value(key, value)

        return ('redirect', None)

    from django.template.loader import render_to_string
    return ('display', mark_safe(render_to_string(template, {
            'form': form,
            'request': request,
            'plugin_description': plugin.get_description() or '',
        }, context_instance=RequestContext(request))))