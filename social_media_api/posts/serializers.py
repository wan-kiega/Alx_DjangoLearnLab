# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment
from django.conf import settings

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    author = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Automatically set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model
    """
    author = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    comments = CommentSerializer(many=True, read_only=True)  # Nested comments
    comments_count = serializers.SerializerMethodField()  # Count of comments
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comments_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'comments']
    
    def get_comments_count(self, obj):
        """Return the count of comments for this post"""
        return obj.comments.count()
    
    def create(self, validated_data):
        # Automatically set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_title(self, value):
        """Validate that title is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()
    
    def validate_content(self, value):
        """Validate that content is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty")
        return value.strip()

class PostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Post (simplified version for creation)
    """
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def validate_title(self, value):
        """Validate that title is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()
    
    def validate_content(self, value):
        """Validate that content is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty")
        return value.strip()

class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Comment (simplified version for creation)
    """
    class Meta:
        model = Comment
        fields = ['post', 'content']
    
    def validate_content(self, value):
        """Validate that content is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Comment cannot be empty")
        return value.strip()
    
    def validate_post(self, value):
        """Validate that post exists"""
        if not value:
            raise serializers.ValidationError("Post is required")
        return value