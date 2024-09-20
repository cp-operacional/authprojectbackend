from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from authentication.models import UserAccount
from rest_framework.response import Response
from .serializers import UserAccountSerializer
from rest_framework.parsers import MultiPartParser
from django.conf import settings
import os

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by('-date_joined')
    serializer_class = UserAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def upload_avatar(self, request):
        user = request.user
        avatar = request.FILES.get('avatar')
        if avatar:
            # Delete old avatar if exists
            if user.avatar:
                old_path = user.avatar.path
                if os.path.isfile(old_path):
                    os.remove(old_path)
            
            # Set new avatar path
            avatar_dir = os.path.join(settings.MEDIA_ROOT, f'avatars/{user.id}')
            os.makedirs(avatar_dir, exist_ok=True)
            
            # Save new avatar
            user.avatar = avatar
            user.save()
            
            avatar_path = user.avatar.path
            return Response({'message': 'Avatar uploaded successfully', 'avatar_path': avatar_path}, status=status.HTTP_200_OK)
        return Response({'error': 'No avatar file provided'}, status=status.HTTP_400_BAD_REQUEST)
