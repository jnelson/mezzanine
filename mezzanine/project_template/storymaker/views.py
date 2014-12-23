from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


def home(request, template="index.html"):
    logger.debug('home bitches!')
    featured_users = User.objects.all()[:8]
    my_data_dictionary = {"featured_users": featured_users, "foo": "bar"}
    return render_to_response(template,
                          my_data_dictionary,
                          context_instance=RequestContext(request))


def user_profile(request, user):
    """
        Placeholder for user profile page, etc

        NOTE: This view is called directly by the UserPagesMiddleware
        when the request matches '/<username>/...'
    """

    name_len = len(user.username) + 2  # len(/<username>/)
    path = request.path[name_len:]

    if path.startswith('followers'):
        message = "{0}'s followers...".format(user.username)
    elif path.startswith('following'):
        message = "{0} is following...".format(user.username)

    # whatever else to match here? do better url routing?

    else:
        message = "{0}'s profile.".format(user.username)

    return HttpResponse(message)
