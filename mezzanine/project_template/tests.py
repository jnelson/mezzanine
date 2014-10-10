from django.test import TestCase
from django.contrib.auth.models import User
from models import Shareable, ShareableBlogPost, StoryMakerGroup
import social
from actstream.models import user_stream, following, followers


class StoryMakerTestCase(TestCase):
    user1 = None
    user2 = None

    def setUp(self):
         self.user1 = User.objects.create(username="user1", email="a@b.com", password="password")
         self.user2 = User.objects.create(username="user2", email="a@b.com", password="password")


    def test_user_group_creation(self):
        """
        Test that the proper default user groups are created for Users
        """
        self.assertEqual(len(followers(self.user1)), 0)

        groups_following = following(self.user1, StoryMakerGroup)
        self.assertEqual(len(groups_following), 2)
        pub_group, created = self.user1.profile.get_or_create_public_group()
        priv_group, created = self.user1.profile.get_or_create_private_group()
        for group in groups_following:
            if group.id != pub_group.id and group.id != priv_group.id:
                self.fail("Initial user groups not as expected")


    def test_public_private_post_permissions(self):
        '''
        Two users each make a public and private post. Test post visibility as users
        follow and unfollow one another.
        '''

        user1_private_blog = ShareableBlogPost.objects.create(title="Visible to who user1 follows and is followed by", user=self.user1, visibility=Shareable.VISIBILITY_PRIVATE)
        user1_public_blog = ShareableBlogPost.objects.create(title="Visible to followers of user1", user=self.user1, visibility=Shareable.VISIBILITY_PUBLIC)

        user2_public_blog = ShareableBlogPost.objects.create(title="Visible to who follows user2", user=self.user2, visibility=Shareable.VISIBILITY_PUBLIC)
        user2_private_blog = ShareableBlogPost.objects.create(title="Visible only to nobody for now", user=self.user2, visibility=Shareable.VISIBILITY_PRIVATE)

        # group1.add_follower(self.user1)

        # User1 follows User2
        social.add_follower_to_user(self.user1, self.user2)

        # Assert: user2 should not see user1_private_blog
        user2_sees_user1_private_blog = False
        for action in user_stream(self.user2, with_user_activity=False):
            if action.action_object_object_id is not None:
                if int(action.action_object_object_id) == user1_private_blog.id:
                    user2_sees_user1_private_blog = True
                    break

        self.assertEqual(user2_sees_user1_private_blog, False)

        # user2 follows user1
        social.add_follower_to_user(self.user2, self.user1)

        # Assert: user2 should see user1_private_blog
        user2_sees_user1_private_blog = False
        for action in user_stream(self.user2, with_user_activity=False):
            if action.action_object_object_id is not None:
                if int(action.action_object_object_id) == user1_private_blog.id:
                    user2_sees_user1_private_blog = True
                    break

        self.assertEqual(user2_sees_user1_private_blog, True)

        # Assert: user1 should see user2_public_blog and user2_private_blog
        user1_sees_user2_public_blog = False
        user1_sees_user2_private_blog = False
        for action in user_stream(self.user1, with_user_activity=False):
            if action.action_object_object_id is not None:
                if int(action.action_object_object_id) == user2_public_blog.id:
                    user1_sees_user2_public_blog = True
                if int(action.action_object_object_id) == user2_private_blog.id:
                    user1_sees_user2_private_blog = True

        self.assertEqual(user1_sees_user2_public_blog, True)
        self.assertEqual(user1_sees_user2_private_blog, True)

        # User1 unfollows user2
        social.remove_follower_from_user(self.user1, self.user2)

        # Assert: user1 should not see user2_public_blog nor user2_private_blog
        user1_sees_user2_public_blog = False
        user1_sees_user2_private_blog = False
        for action in user_stream(self.user1, with_user_activity=False):
            if action.action_object_object_id is not None:
                if int(action.action_object_object_id) == user2_public_blog.id:
                    user1_sees_user2_public_blog = True
                if int(action.action_object_object_id) == user2_private_blog.id:
                    user1_sees_user2_private_blog = True

        self.assertEqual(user1_sees_user2_public_blog, False)
        self.assertEqual(user1_sees_user2_private_blog, False)

        # Assert: user2 should not see user1_private_blog but should see user2_public_blog
        user2_sees_user1_private_blog = False
        user2_sees_user2_public_blog = False
        for action in user_stream(self.user2, with_user_activity=False):
            if action.action_object_object_id is not None:
                if int(action.action_object_object_id) == user1_private_blog.id:
                    user2_sees_user1_private_blog = True
                if int(action.action_object_object_id) == user2_public_blog.id:
                    user2_sees_user2_public_blog = True

        self.assertEqual(user2_sees_user1_private_blog, False)
        self.assertEqual(user2_sees_user2_public_blog, True)

        # user1_public_blog becomes private
        user1_public_blog.visibility = Shareable.VISIBILITY_PRIVATE
        user1_public_blog.save()

        # Assert: user2 should not see user1_public_blog (now also private)
        user2_sees_user1_public_blog = False
        for action in user_stream(self.user2, with_user_activity=False):
            if action.action_object_object_id is not None:
                if int(action.action_object_object_id) == user1_public_blog.id:
                    user2_sees_user1_public_blog = True
                    break

        self.assertEqual(user2_sees_user1_public_blog, False)