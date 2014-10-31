from rest_framework import serializers
from django.contrib.auth.models import User
from mezzanine.blog.models import BlogPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost