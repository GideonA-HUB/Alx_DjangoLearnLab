from django.shortcuts import render
from rest_framework import filters
from rest_framework import viewsets, permissions, generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model


# Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['title', 'content']

    def get_queryset(self):
        # Modify the queryset to show posts from users the logged-in user follows
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Optionally, a custom action to get all comments for a specific post
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access the feed
    serializer_class = PostSerializer  # Use PostSerializer to serialize the posts

    def get_queryset(self):
        """
        This method filters the posts based on the users the current user follows.
        It returns posts created by users the current user is following, ordered by creation date.
        """
        user = self.request.user  # The currently authenticated user
        following_users = user.following.all()  # Get all the users that the current user is following
        
        # Filter posts that belong to the users the current user is following
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        This is the method that handles the GET request for the feed.
        It will return the posts serialized in the response.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)