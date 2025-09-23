from .models import UrlMapping
from rest_framework import serializers

class UrlMappingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UrlMapping
        fields = ['shortcode', 'original_url']