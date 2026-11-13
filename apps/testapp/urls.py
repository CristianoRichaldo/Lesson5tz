from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import GoogleAuthView, LessonViewSet

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('api/v1/auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('api/v1/auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('api/v1/auth/google/', GoogleAuthView.as_view(), name='google_auth'),
    path('api/v1/', include(router.urls)),
]