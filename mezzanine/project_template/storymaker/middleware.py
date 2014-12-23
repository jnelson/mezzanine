
from django.contrib.auth import get_user_model

from storymaker.views import user_profile

import logging
logger = logging.getLogger(__name__)


class UserPagesMiddleware(object):
    """

        Look for requests for /username/... and handle those specially.

        This is done in a middleware since the mezzanine Pages app has a
        wildcard match, too. So we try to see if the request path starts
        with a valid username, and call directly in to the view.

        If the Pages app is ever removed (or confind to a sub-URL), this
        should be removed in favor of a wildcard URL pattern.
    """

    def process_request(self, request):

        UserModel = get_user_model()

        # this split returns a variable number of items depending on the URL.
        parts = request.path_info.split('/', 2)
        if len(parts) >= 2:
            username = parts[1]
        else:
            # no username in the URL
            return None

        logger.debug('got username: {0}'.format(username))
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            logger.debug("no user")
            # we're done, move on to the next middleware
            return None

        # if the user has their profile hidden, we could return that
        # response right here.

        return user_profile(request, user)
