from rest_framework import mixins, generics
from django.contrib.auth.models import User, Group
from mezzanine.blog.models import BlogPost
from serializers import UserSerializer, GroupSerializer, BlogPostSerializer
from rest_framework import permissions
from actstream import action


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    fields = ('password', 'first_name', 'last_name', 'email')
    #permission_classes = (permissions.IsAuthenticated,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    fields = ('password', 'first_name', 'last_name', 'email')
    write_only_fields = ('password',)


class UserGroupList(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = super(UserGroupList, self).get_queryset()
        return queryset.filter(id=self.kwargs.get('pk'))


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class BlogPostList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("-----------------------------")
        print(request.user)
        group_ids = request.DATA.get("group_ids", default=None)
        print("-----------------------------")
        for group_id in group_ids:
            group = Group.objects.get_by_natural_key(group_id)
            action.send(request.user, verb='posted story', object=self, target=group)
        return self.create(request, *args, **kwargs)


class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer