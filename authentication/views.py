from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from authentication.models import UserAccount
from rest_framework.response import Response
from .serializers import UserAccountSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_size = 10

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by('-date_joined')
    serializer_class = UserAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], parser_classes=[MultiPartParser, FormParser])
    def update_avatar(self, request):
        user = request.user
        if 'avatar' not in request.FILES:
            return Response({'error': 'No file provided'}, status=400)
        
        avatar = request.FILES['avatar']
        filename = 'avatar-1' + os.path.splitext(avatar.name)[1]
        filepath = os.path.join('avatars', filename)
        
        if default_storage.exists(filepath):
            default_storage.delete(filepath)
        
        path = default_storage.save(filepath, ContentFile(avatar.read()))
        
        user.avatar = path
        user.save()
        
        return Response({'status': 'avatar updated', 'avatar_url': default_storage.url(path)})
