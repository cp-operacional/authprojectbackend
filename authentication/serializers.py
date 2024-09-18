from rest_framework import serializers
from authentication.models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'color', 'year', 'pantone_value']