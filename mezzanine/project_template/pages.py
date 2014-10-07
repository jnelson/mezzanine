from django.contrib import admin
from mezzanine.pages.models import Page
from mezzanine.pages.admin import PageAdmin

class FollowingFeed(Page):
    '''
    The activity of entities the user follows
    '''
    pass

class FollowersFeed(Page):
    '''
    The activity of entities that follow the user
    '''
    pass

admin.site.register(FollowingFeed, PageAdmin)
admin.site.register(FollowersFeed, PageAdmin)
