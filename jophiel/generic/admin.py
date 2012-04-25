from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin
from django.utils.translation import ugettext_lazy as _



class ThreadedCommentAdmin(CommentsAdmin):
    """
    Admin class for comments.
    """

    list_display = ("avatar_link", "intro", "submit_date", "is_public",
                    "is_removed", "admin_link")
    list_display_links = ("intro", "submit_date")
    fieldsets = (
        (_("User"), {"fields": ("user_name", "user_email", "user_url")}),
        (None, {"fields": ("comment", ("is_public", "is_removed"))}),
    )

    def get_actions(self, request):
        actions = super(CommentsAdmin, self).get_actions(request)
        actions.pop("delete_selected")
        actions.pop("flag_comments")
        return actions

