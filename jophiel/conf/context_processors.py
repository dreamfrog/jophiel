

def settings(request):
    """
    Add the settings object to the template context.
    """
    from jophiel.conf import settings
    print settings
    settings.use_editable()
    return {"settings": settings}
