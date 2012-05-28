
def settings(request):
    """
    Add the settings object to the template context.
    """
    from django.conf import settings
    return {"settings": settings}
