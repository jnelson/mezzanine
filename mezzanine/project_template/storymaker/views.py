from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from actstream.models import user_stream

from django.http import Http404
from django.shortcuts import get_object_or_404
from mezzanine.utils.views import render, paginate

from mezzanine.conf import settings
from mezzanine.blog.views import blog_post_list

import logging

logger = logging.getLogger(__name__)

def index(request, template="index.html"):
    featured_users = User.objects.all()[:8]
    my_data_dictionary = {"featured_users": featured_users, "foo": "bar"}
    return render_to_response(template,
                          my_data_dictionary,
                          context_instance=RequestContext(request))

def home(request, template="home.html"):
    """
    Display this users home screen, which is a list of blog posts from people they follow
    """
    category=None
    tag=None
    year=None 
    month=None
    
    settings.use_editable()
    templates = []
    stream = user_stream(request.user)
    blog_posts = []
    for action in stream:
        if action.verb == 'posted blog':
            logger.debug("action id %s" % action.id)
            obj = action.action_object
            logger.debug("action_objects: id %s, %s" % (obj.id, obj))
            blog_posts.append(action.action_object)        
        
    #blog_posts = BlogPost.objects.published(for_user=request.user)
    #if tag is not None:
    #    tag = get_object_or_404(Keyword, slug=tag)
    #    blog_posts = blog_posts.filter(keywords__keyword=tag)
    #if year is not None:
    #    blog_posts = blog_posts.filter(publish_date__year=year)
    #    if month is not None:
    #        blog_posts = blog_posts.filter(publish_date__month=month)
    #        try:
    #            month = month_name[int(month)]
    #        except IndexError:
    #            raise Http404()
    #if category is not None:
    #    category = get_object_or_404(BlogCategory, slug=category)
    #    blog_posts = blog_posts.filter(categories=category)
    #    templates.append(u"blog/blog_post_list_%s.html" %
    #                      str(category.slug))
    author = None
    #username = "johnscalio1" # FIXME 
    #if username is not None:
    #    author = get_object_or_404(User, username=username)
    #    blog_posts = blog_posts.filter(user=author)
    #    templates.append(u"blog/blog_post_list_%s.html" % username)

    #prefetch = ("categories", "keywords__keyword")
    #   blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)
    blog_posts = paginate(blog_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"blog_posts": blog_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    templates.append(template)
    return render(request, templates, context)    
    

def app(request, template="app.html"):
    logger.debug('App upsell')
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


def burundi_blog_view(request):
    """
        Since this is pinned to the 'burundi' category, it's using the template
        blog_post_list_burundi.html
    """
    return blog_post_list(request, category='burundi')
