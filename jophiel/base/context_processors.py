
def settings(request):
    """
    Add the settings object to the template context.
    """
    from jophiel.base import settings
    settings.use_editable()
    return {"settings": settings}
