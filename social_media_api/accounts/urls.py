from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import FollowViewSet
from .views import RegisterView, LoginView, UserProfile

router = DefaultRouter()
router.register(r'follow', FollowUserView, basename='follow_user')



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('api/', include(router.urls)),
    path('follow/', views.FollowUserView.as_view(), name='follow_user'),
    path('unfollow/', views.UnfollowUserView.as_view(), name='unfollow_user'),
]
