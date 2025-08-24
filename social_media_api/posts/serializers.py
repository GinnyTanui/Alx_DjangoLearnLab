from rest_framework import serializers
from .models import Post, Comment, Like

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_username',
            'title', 'content',
            'created_at', 'updated_at',
            'comments_count',
        ]
        read_only_fields = ['id', 'author', 'author_username', 'created_at', 'updated_at', 'comments_count']


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    post_title = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title',
            'author', 'author_username',
            'content', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'author', 'author_username', 'created_at', 'updated_at', 'post_title']

from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]
        read_only_fields = ["user", "created_at"]
