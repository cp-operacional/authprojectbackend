from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserViewSet
from core import settings
from resources.views import ResourceViewSet

router = DefaultRouter()
router.register(r'resources', ResourceViewSet, basename='resources')
router.register(r'auth/users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/users/me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('resources/<int:pk>/move_up/', ResourceViewSet.as_view({'post': 'move_up'}), name='resource-move-up'),
    path('resources/<int:pk>/move_down/', ResourceViewSet.as_view({'post': 'move_down'}), name='resource-move-down'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]