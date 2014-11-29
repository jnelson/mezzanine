from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

def home(request, template="index.html"):
    logger.debug('home bitches!')
    featured_users = User.objects.all()[:8]
    my_data_dictionary = {"featured_users": featured_users, "foo": "bar"}
    return render_to_response(template,
                          my_data_dictionary,
                          context_instance=RequestContext(request))
