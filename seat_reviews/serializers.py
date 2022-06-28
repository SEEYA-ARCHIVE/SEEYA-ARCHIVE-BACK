from django.conf import settings
from rest_framework.serializers import ModelSerializer
from .models import Review, Comment
from accounts.models import User
from rest_framework import serializers
import os


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user', 'kakao_id', 'email']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'comment', 'create_at', 'update_at']


class SeatReviewListSerializer(ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'create_at', 'images']

    def get_images(self, obj):
        return {'preview_image': os.path.join(settings.MEDIA_URL, 'review-images', obj.images[0]),
                'count_images': len(obj.images)}


class DetailReviewSerializer(ModelSerializer):
    seat_area = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    concert_hall_name = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'concert_hall_name', 'create_at',
                  'update_at', 'seat_area', 'images', 'artist', 'reviews', 'comments']

    def get_seat_area(self, obj):
        return obj.seat_area.area

    def get_images(self, obj):
        return [os.path.join(settings.MEDIA_URL, 'review-images', image) for image in obj.images]

    def get_concert_hall_name(self, obj):
        return obj.seat_area.concert_hall.name

    def get_user(self, obj):
        return {'user_kakao_id': obj.user.kakao_id, 'email': obj.user.email,
                'user_pk': obj.user.pk}