from rest_framework import serializers
from .models import Books, BookImage, Star, Comment, Like
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg

User = get_user_model()

class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = ['id', 'image']

class StarSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Star
        fields = ['id', 'user', 'book', 'rating']
        extra_kwargs = {
            'user': {'read_only': True},
            'book': {'read_only': True},
        }

class StarAvgSerializer(serializers.ModelSerializer):
    star_avg = serializers.SerializerMethodField()

    class Meta:
        model = Books
        fields = ['id', 'title', 'star_avg']

    def get_star_avg(self, obj):
        stars = Star.objects.filter(book=obj)
        avg = stars.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else 0

class LikeDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']


class BooksLikeSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    liked_users = LikeDetailSerializer(source='likes', many=True, read_only=True)

    class Meta:
        model = Books
        fields = ['id', 'title', 'like_count', 'liked_users']

    def get_like_count(self, obj):
        return obj.like.count()

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'book', 'text', 'created_at']
        extra_kwargs = {
            'book': {'read_only': True},
        }


class BooksSerializer(serializers.ModelSerializer):
    images = BookImageSerializer(many=True, read_only=True)
    star_avg = serializers.SerializerMethodField()
    comment = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Books
        fields = [
            'id', 'user', 'title', 'info', 'isbn', 'author', 'book_language',
            'writing', 'translator', 'pages', 'publisher', 'cover',
            'publication_date', 'quantity', 'page_surface', 'country',
            'created_at', 'price', 'images', 'star_avg', 'comment', 'like_count',
        ]

    def get_star_avg(self, obj):
        stars = Star.objects.filter(book=obj)
        avg = stars.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else 0

    def get_like_count(self, obj):
        return obj.like.count()

