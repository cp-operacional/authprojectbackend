from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from resources.models import Resource
from resources.serializers import ResourceSerializer
from django.db import models
from rest_framework.decorators import action

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_size = 10

class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Resource.objects.filter(user_id=self.request.user).order_by('order')

    def perform_create(self, serializer):
        Resource.objects.filter(user_id=self.request.user).update(order=models.F('order') + 1)
        serializer.save(user_id=self.request.user, order=1)

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
