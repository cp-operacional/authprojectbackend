from django.contrib import admin

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from authentication.views import UserViewSet
from resources.views import ResourceViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'resources', ResourceViewSet)
router.register(r'auth/users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
