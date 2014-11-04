from rest_framework import serializers
from django.contrib.auth.models import User, Group
from mezzanine.blog.models import BlogPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost