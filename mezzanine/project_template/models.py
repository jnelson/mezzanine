from django.db import models
from django.contrib.auth.models import User, Group


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User, related_name="profile")

    # Storymaker fields below one day...

    def check_create_and_join_default_groups(self):
        '''
        Create the default groups for Private and Public user feeds, if they don't yet exist.
        Called on UserProfile creation
        '''

        if self.default_user_groups_created():
            return

        public_group_name = self.get_public_group_name()
        public_group, created = Group.objects.get_or_create(name=public_group_name)
        public_group.user_set.add(self.user)

        private_group_name = self.get_private_group_name()
        private_group, created = Group.objects.get_or_create(name=private_group_name)
        private_group.user_set.add(self.user)


    def default_user_groups_created(self):
        '''
        Returns whether the given user belongs to the default groups appropriate
        for a newly created user.
        '''
        user = self.user

        if user.groups.filter(name=self.get_private_group_name()).exists() and \
            user.groups.filter(name=self.get_public_group_name()).exists():
            return True
        return False

    def get_private_group_name(self):
        return self.user.get_username() + "-private"

    def get_public_group_name(self):
        return self.user.get_username() + "-public"

