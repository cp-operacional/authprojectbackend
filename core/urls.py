from django.contrib import admin

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from authentication.views import UserViewSet
from core import settings
from resources.views import ResourceViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'resources', ResourceViewSet, basename='resources')
router.register(r'auth/users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/users/me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('auth/users/upload_avatar/', UserViewSet.as_view({'post': 'upload_avatar'}), name='user-upload-avatar'),
    path('auth/users/avatar/<str:filename>', UserViewSet.as_view({'get': 'view_avatar'}), name='user-view-avatar'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)