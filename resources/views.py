from rest_framework import viewsets, permissions
from resources.models import Resource
from resources.serializers import ResourceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models

class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resource.objects.filter(user_id=self.request.user).order_by('order')

    def perform_create(self, serializer):
        max_order = Resource.objects.filter(user_id=self.request.user).aggregate(models.Max('order'))['order__max'] or 0
        serializer.save(user_id=self.request.user, order=max_order + 1)

    @action(detail=True, methods=['POST'])
    def move_up(self, request, pk=None):
        return self._move_item(pk, 'up')

    @action(detail=True, methods=['POST'])
    def move_down(self, request, pk=None):
        return self._move_item(pk, 'down')

    def _move_item(self, pk, direction):
        item = self.get_object()
        if direction == 'up':
            swap_item = Resource.objects.filter(user_id=self.request.user, order__lt=item.order).order_by('-order').first()
        else:
            swap_item = Resource.objects.filter(user_id=self.request.user, order__gt=item.order).order_by('order').first()

        if swap_item:
            item_order, swap_item_order = item.order, swap_item.order
            item.order, swap_item.order = swap_item_order, item_order
            item.save()
            swap_item.save()

        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def perform_create(self, serializer):
        max_order = Resource.objects.filter(user_id=self.request.user).aggregate(models.Max('order'))['order__max'] or 0
        serializer.save(user_id=self.request.user, order=max_order + 1)
