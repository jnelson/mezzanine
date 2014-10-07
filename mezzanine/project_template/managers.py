from collections import defaultdict
from datetime import datetime

from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from actstream.managers import ActionManager, stream
from actstream.registry import check
from mezzanine.utils.models import get_model


class StoryMakerActionManager(ActionManager):

    @stream
    def followers(self, obj, **kwargs):
        """
        Stream of most recent actions by entities that follow the passed User obj
        """
        q = Q()
        qs = self.public()

        if not obj:
            return qs.none()

        check(obj)
        actors_by_content_type = defaultdict(lambda: [])
        others_by_content_type = defaultdict(lambda: [])

        if kwargs.pop('with_user_activity', False):
            object_content_type = ContentType.objects.get_for_model(obj)
            actors_by_content_type[object_content_type.id].append(obj.pk)


        follower_gfks = get_model('actstream', 'follow').objects.filter(
            object_id=obj.id).values_list('content_type_id',
                                  'user_id', 'actor_only')

        # Get all objects the user follows
        for content_type_id, object_id, actor_only in follower_gfks.iterator():
            actors_by_content_type[content_type_id].append(object_id)
            if not actor_only:
                others_by_content_type[content_type_id].append(object_id)

        if len(actors_by_content_type) + len(others_by_content_type) == 0:
            return qs.none()

        # a.k.a: All actions by any follower user (and current user if with_user_activity)
        for content_type_id, object_ids in actors_by_content_type.items():
            q = q | Q(
                actor_content_type=content_type_id,
                actor_object_id__in=object_ids,
            )

        # all actions with followed user as target
        # OR
        # all actions with followed user as object
        for content_type_id, object_ids in others_by_content_type.items():
            q = q | Q(
                target_content_type=content_type_id,
                target_object_id__in=object_ids,
            ) | Q(
                action_object_content_type=content_type_id,
                action_object_object_id__in=object_ids,
            )
        return qs.filter(q, **kwargs)