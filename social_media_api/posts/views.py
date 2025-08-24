from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


class PostViewSet(viewsets.ModelViewSet):
    """
    /api/posts/           GET (list), POST (create)
    /api/posts/{id}/      GET (retrieve), PUT/PATCH (update), DELETE
    Search: ?search=<text>  (title/content)
    Ordering: ?ordering=created_at or -created_at (default global)
    """
    queryset = Post.objects.select_related('author').prefetch_related('comments')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    /api/comments/             GET (list), POST
    /api/comments/{id}/        GET, PUT/PATCH, DELETE
    Filter by post: ?post=<post_id>
    """
    queryset = Comment.objects.select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get('post')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        # Require ?post=<id> in payload or set post in the body
        # We accept post from validated data; just enforce author here:
        serializer.save(author=self.request.user)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed(request):
    # get all users I follow
    following_users = request.user.following.all()
    
    # filter posts only from them
    posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
    
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class LikePostView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"detail": "You already liked this post."}, status=400)

        # Create notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked",
            target=post,
            target_ct=ContentType.objects.get_for_model(Post),
            target_id=post.id,
        )

        return Response(LikeSerializer(like).data, status=201)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            return Response({"detail": "You have not liked this post."}, status=400)

        like.delete()
        return Response({"detail": "Like removed."}, status=204)
