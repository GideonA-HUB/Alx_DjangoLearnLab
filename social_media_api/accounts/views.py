from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer,  LoginSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()  # This creates the user
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data['token']
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get the authenticated user's profile.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        """
        Update the authenticated user's profile.
        """
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can follow/unfollow
    queryset = CustomUser.objects.all()  # Use CustomUser directly to fetch all users

    def get_object(self, pk):
        """
        Retrieve a specific user based on the pk (primary key).
        """
        return CustomUser.objects.get(pk=pk)

    @action(detail=True, methods=['post'])
    def follow_user(self, request, pk=None):
        """
        Follow another user by adding to the following relationship.
        """
        try:
            user_to_follow = self.get_object(pk)  # Get the user to be followed
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user  # The user who is making the follow request
        
        # Prevent users from following themselves
        if user == user_to_follow:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user_to_follow to the current user's following field
        user.following.add(user_to_follow)
        user.save()

        return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow_user(self, request, pk=None):
        """
        Unfollow a user by removing from the following relationship.
        """
        try:
            user_to_unfollow = self.get_object(pk)  # Get the user to be unfollowed
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user  # The user who is making the unfollow request
        
        # Prevent users from unfollowing themselves
        if user == user_to_unfollow:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the user_to_unfollow from the current user's following field
        user.following.remove(user_to_unfollow)
        user.save()

        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def follow_user(request, user_id):
    """
    Follow a user by adding the user_id to the current user's following list.
    """
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

    current_user = request.user
    # Get the user to be followed
    user_to_follow = get_object_or_404(User, id=user_id)

    # Avoid self-following
    if current_user == user_to_follow:
        return JsonResponse({'detail': 'You cannot follow yourself.'}, status=400)

    # Add the user to the following list if not already followed
    if user_to_follow not in current_user.following.all():
        current_user.following.add(user_to_follow)
        return JsonResponse({'detail': f'You are now following {user_to_follow.username}.'}, status=200)
    else:
        return JsonResponse({'detail': 'You are already following this user.'}, status=400)

@api_view(['POST'])
def unfollow_user(request, user_id):
    """
    Unfollow a user by removing the user_id from the current user's following list.
    """
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

    current_user = request.user
    # Get the user to be unfollowed
    user_to_unfollow = get_object_or_404(User, id=user_id)

    # Ensure the user is following the user they want to unfollow
    if user_to_unfollow not in current_user.following.all():
        return JsonResponse({'detail': 'You are not following this user.'}, status=400)

    # Remove the user from the following list
    current_user.following.remove(user_to_unfollow)
    return JsonResponse({'detail': f'You have unfollowed {user_to_unfollow.username}.'}, status=200)