from mezzanine.pages.page_processors import processor_for
from .pages import FollowingFeed
from actstream.models import user_stream

@processor_for(FollowingFeed)
def get_feed_items(request, page):
    return {"feed_items": user_stream(request.user, with_user_activity=True)}
