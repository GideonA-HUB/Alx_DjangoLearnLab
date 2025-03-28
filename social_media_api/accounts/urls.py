from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FollowViewSet
from .views import RegisterView, LoginView, UserProfile

router = DefaultRouter()
router.register(r'follow', FollowViewSet, basename='follow')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('api/', include(router.urls)),
]
