from actstream import registry, action, actions
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from organizations.utils import create_organization
from organizations.models import Organization, OrganizationUser, OrganizationOwner
from mezzanine.blog.models import BlogPost

registry.register(BlogPost)
registry.register(Organization)
registry.register(User)

def new_blogpost_handler(sender, instance, created, **kwargs):
    if created:
        # TODO we need to figure out how to target these are the right org, just assuming _public for testing
        print "saved new blogpost: %s" % instance
        org = Organization.objects.get(name="%s_public" % instance.user.username)
        action.send(instance.user, verb='posted blog', action_object=instance, target=org)
    
def new_user_handler(sender, instance, created, **kwargs):
    if created:
        print "saved new user, setting up their orgs and follows: %s" % instance
        name = "%s_public" % instance.username
        org_public = create_organization(instance, name)
        
        name = "%s_private" % instance.username
        org_private = create_organization(instance, name)
        
        # should always follow your own public and private
        actions.follow(instance, org_public, actor_only=False)
        actions.follow(instance, org_private, actor_only=False)
        
        # TODO we need a global follower for the public areas of the site
    

post_save.connect(new_blogpost_handler, sender=BlogPost)

# FIXME this is for every save, we need to do it for record creation only
post_save.connect(new_user_handler, sender=User)

# TODO create user_public and user_private whenever a new user is created
