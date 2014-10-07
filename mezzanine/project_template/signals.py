from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    '''
    Create UserProfile for each Django User
    '''

    if created:
        profile = instance.profile
        if not profile:
            UserProfile.objects.create(user=instance)

        profile.check_create_and_join_default_groups()
