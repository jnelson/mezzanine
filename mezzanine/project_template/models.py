from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User, Group
from actstream import registry, action
from actstream.actions import follow, unfollow
from actstream.models import following, followers, Follow, Action
from mezzanine.blog.models import BlogPost
from django.core.exceptions import PermissionDenied


class StoryMakerGroup(models.Model):
    """
    This represents an entity that acts as an Action target.
    e.g : It can be posted to, and followed
    """

    name = models.CharField(max_length=255)

    # Group Privacy
    # e.g: Should it be discoverable?
    private = models.BooleanField(default=False)

    # Single user status
    # e.g: When direct messaging a set of groups,
    # should a single new group be created for the subset of single_user groups
    single_user = models.BooleanField(default=False)
    invite_ony = models.BooleanField(default=False)

    # Members
    users = models.ManyToManyField(User, related_name="member_groups")

    # Users with permission to add / remove users from group
    admins = models.ManyToManyField(User, related_name="administered_groups")

    # Users invited to follow. Used in conjunction with groups where invite_only is True
    invited_users = models.ManyToManyField(User, related_name="invited_to_groups")

    # Users who may not follow or post to this group
    banned_users = models.ManyToManyField(User, related_name="banned_from_groups")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def add_follower(self, user):
        """
        Add user as follower of this group, return True if successful.
        Operation will return false and take no action if user is banned from this group
        """
        if self.banned_users.filter(id=user.id).exists():
            # User is banned
            return False
        if self.invite_ony and not self.invited_users.filter(id=user.id).exists():
            # User requires invite
            return False
        # Subscribe user to all Actions involving group
        self.users.add(user)
        follow(user, self, actor_only=False)
        return True

    def remove_follower(self, user):
        """
        Remove user as follower of this group
        """
        self.users.remove(user)
        unfollow(user, self)


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User, related_name="profile")

    def check_create_and_join_default_groups(self):
        """
        Create the default groups for Private and Public user feeds, if they don't yet exist.
        Called on UserProfile creation
        """

        if self.default_user_groups_created():
            return

        # Create private and public groups.
        public_group, created = self.get_or_create_public_group()
        private_group, created = self.get_or_create_private_group()

        # Subscribe user to all Actions involving group
        follow(self.user, private_group, actor_only=False, send_action=False)
        follow(self.user, public_group, actor_only=False, send_action=False)

    def default_user_groups_created(self):
        '''
        Returns whether the given user follows the default groups appropriate
        for a newly created user.
        '''

        public_group, created = self.get_or_create_public_group()
        private_group, created = self.get_or_create_private_group()

        if Follow.objects.filter(
                content_type=ContentType.objects.get_for_model(public_group),
                object_id=public_group.pk,
                user_id=self.user.pk).exists() and \
                Follow.objects.filter(
                        content_type=ContentType.objects.get_for_model(private_group),
                        object_id=private_group.pk,
                        user_id=self.user.pk).exists():
            return True
        return False

    def get_or_create_private_group(self):
        return StoryMakerGroup.objects.get_or_create(name=self.get_private_group_name(), private=True, single_user=True)

    def get_private_group_name(self):
        return self.user.get_username() + "-private"

    def get_or_create_public_group(self):
        return StoryMakerGroup.objects.get_or_create(name=self.get_public_group_name(), private=False, single_user=True)

    def get_public_group_name(self):
        return self.user.get_username() + "-public"


class Shareable(models.Model):
    """
    Abstract representation of a model that is involved in the StoryMaker Activity Stream.
    All such objects have an associated visibility required to describe the associated Action
    created upon instantiation of this object.
    """

    VISIBILITY_PUBLIC = 1
    VISIBILITY_PRIVATE = 2
    VISIBILITY_GROUP = 3

    VISIBILITY_CHOICES = [(VISIBILITY_PUBLIC, 'Public'),
                          (VISIBILITY_PRIVATE, 'Visible to followers that I follow back'),
                          (VISIBILITY_GROUP, 'Visible to selected Users or Communities')]

    visibility = models.IntegerField(choices=VISIBILITY_CHOICES, null=False, blank=False)
    # If visibility = VISIBILITY_GROUP, this represents those groups this item is shraed with
    visible_to = models.ManyToManyField(StoryMakerGroup, related_name="items_shared_with", null=True, blank=True)

    __original_visibility = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(Shareable, self).__init__(*args, **kwargs)
        self.__original_visibility = self.visibility


    def save(self, *args, **kwargs):
        '''
        If the target has changed since last save, treat this as a new
        Action representing a visibility change.

        e.g: Bob had posted "HelloThere" to his followers and then later
             extended that post's visibility to public.

             Here two Actions will be generated:
             + <Bob> <posts> <"HelloThere"> to <followers>
             + <Bob> <posts> <"HelloThere"> to <public>

        Subclasses should deal with side effects of visibility
        reduction.

        e.g: Bob had posted "HelloThere" publicly and then later
             reduced that visibility to his followers.

             We need to counteract the effects of the initial
             public visibility. For example, we'd remove the Action
             corresponding to the initial public posting to prevent
             appearance in the Bob-Public stream.

             Here one Action is generated, then deleted and replaced
             by another Action:
             + <Bob> <posts> <"HelloThere"> to <public>
             - <Bob> <posts> <"HelloThere"> to <public>
             + <Bob> <posts> <"HelloThere"> to <followers>
        '''



        # Check that an Action does not exist where:
        # self is the action object and visibility (target) is expanded
        create_new_action = False
        if self.pk is None:
            create_new_action = True
        else:
            if self.visibility != self.__original_visibility:
                # Visibility was changed
                create_new_action = True
                if self.visibility > self.__original_visibility:
                    # The visibility scope was reduced, so we should delete all previous Actions
                    # that posted this content to an expanded visibility target
                    content_type = self.get_content_type()
                    # Can't filter based on GenericForeignKey (like actor), so we have to query and manually inspect
                    # other all creation actions with this object. This should be a very small list
                    conflicting_actions = Action.objects.filter(verb=self.get_action_verb(),
                                                              action_object_object_id=self.id,
                                                              action_object_content_type=content_type)
                    conflicting_actions.delete()

        super(Shareable, self).save(*args, **kwargs)

        if create_new_action:
            self.create_action()

    def get_action_verb(self):
        '''
        Return the verb describing the act of creating an instance of this object.
        e.g: posted, commented etc.
        '''
        return 'did'

    def get_action_targets(self):
        '''
        Return a list of Target objects for the Django Activity Stream Action corresponding
        to an instance of this class. This is typically a Django Group
        '''
        sm_groups = []
        visibility = self.visibility
        user_profile = self.get_action_actor().profile
        if visibility == Shareable.VISIBILITY_PUBLIC:
            # Ignore the created value in get_or_create_public_group
            sm_groups = [user_profile.get_or_create_public_group()[0]]

        elif visibility == Shareable.VISIBILITY_PRIVATE:
            # Ignore the created value in get_or_create_private_group
            sm_groups = [user_profile.get_or_create_private_group()[0]]

        elif visibility == Shareable.VISIBILITY_GROUP:
            # Create a DM group encompassing all user entities in visibility_entries
            # these are entities where the group.user is not None (e.g:
            if self.visible_to is None or self.visible_to.count() == 0:
                raise NotImplementedError("Have to implement a way to delay emitting creation Action until visible_to set")
            sm_groups = self.visible_to

        return sm_groups

    def get_action_actor(self):
        """
        Return the Actor object for the Django Activity Stream Action corresponding
        to an instance of this class
        """
        raise NotImplementedError("Shareable does not implement get_action_actor")

    def create_action(self):
        """
        Generate the actual Django Activity Stream Action corresponding
        to a new instance of this class being created.
        """
        for target in self.get_action_targets():
            # print 'actor ' + str(self.get_action_actor().username) + ' ' + self.get_action_verb() + ' to target: ' + str(target) + ' with object: ' + str(self.id)
            action.send(self.get_action_actor(), verb=self.get_action_verb(), action_object=self, target=target)


    def get_content_type(self):
        raise NotImplementedError("Not yet done")

class ShareableBlogPost(BlogPost, Shareable):
    def get_action_verb(self):
        return 'posted blog'

    def get_action_actor(self):
        return self.user

    def get_content_type(self):
         return ContentType.objects.get_for_model(self)

# Register all models involved as Actor, Target, or Object by Django Activity Stream

registry.register(ShareableBlogPost)
registry.register(StoryMakerGroup)
registry.register(User)
registry.register(Group)
