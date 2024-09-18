from rest_framework import serializers
from resources.models import Resource



class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'color', 'year', 'pantone_value']
