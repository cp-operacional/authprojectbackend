from django.shortcuts import render
from rest_framework import viewsets
from authentication.models import Resource
from authentication.serializers import ResourceSerializer

# Create your views here.

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
