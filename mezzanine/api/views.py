from rest_framework import generics
from django.contrib.auth.models import User
from mezzanine.blog.models import BlogPost
from serializers import UserSerializer, BlogPostSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BlogPostList(generics.ListCreateAPIView):
        queryset = BlogPost.objects.all()
        serializer_class = BlogPostSerializer


class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer