from rest_framework import serializers
from mezzanine.pages.models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page