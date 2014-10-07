from mezzanine.pages.page_processors import processor_for
from .pages import FollowingFeed, FollowersFeed
from actstream.models import Action, user_stream


@processor_for(FollowingFeed)
def get_feed_items(request, page):
    return {"feed_items": user_stream(request.user, with_user_activity=True)}

@processor_for(FollowersFeed)
def get_feed_items(request, page):
    return {"feed_items": Action.objects.followers(request.user, with_user_activity=False)}
