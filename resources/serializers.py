from rest_framework import serializers
from resources.models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'user_id', 'name', 'color', 'year', 'pantone_value', 'order']
        read_only_fields = ['user_id']
