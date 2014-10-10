from actstream.models import following, followers

def remove_follower_from_user(user_actor, user_target):
    public_group_to_unfollow = get_public_group_for_user(user_target)
    public_group_to_unfollow.remove_follower(user_actor)

    set_private_sharing(user_actor, user_target, enabled=False)

def add_follower_to_user(user_actor, user_target):
    """
    Attempt to add user_actor as a follower of user_target.
    This operation will return False and have no effect if
    user_actor is banned from user_target's public group

    :param user_actor: the user wishing to follow user_target
    :param user_target: the user to be followed
    :return: whether user_actor successfully followed user_target
    """
    group_to_follow = get_public_group_for_user(user_target)
    if user_actor not in followers(group_to_follow):
        success = group_to_follow.add_follower(user_actor)
        if not success:
            # user_actor is banned or without necessary invite
            return False
        # Check to see if user_target follows user_actor
        # and enable private subscription if so
        actor_public_group = get_public_group_for_user(user_actor)
        if user_target in followers(actor_public_group):
            set_private_sharing(user_actor, user_target)

    return True


def set_private_sharing(user1, user2, enabled=True):
    """
    Enable/Disable private sharing between user1 and user2
    To minimize duplicate queries, this method does not
    perform any validation that user1 and user2 already follow
    one another. Any such checking should be done by caller.
    """

    user1_private_group = get_private_group_for_user(user1)
    if enabled:
        user1_private_group.add_follower(user2)
    else:
        user1_private_group.remove_follower(user2)

    user2_private_group = get_private_group_for_user(user2)
    if enabled:
        user2_private_group.add_follower(user1)
    else:
        user2_private_group.remove_follower(user1)


def get_public_group_for_user(user):
    # Ignore created return value for get_or_create_public_group
    return user.profile.get_or_create_public_group()[0]


def get_private_group_for_user(user):
    # Ignore created return value for get_or_create_public_group
    return user.profile.get_or_create_private_group()[0]