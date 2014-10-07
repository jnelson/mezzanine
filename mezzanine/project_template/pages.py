from django.contrib import admin
from mezzanine.pages.models import Page
from mezzanine.pages.admin import PageAdmin

class FollowingFeed(Page):
    pass

admin.site.register(FollowingFeed, PageAdmin)
