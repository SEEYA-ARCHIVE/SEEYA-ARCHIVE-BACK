from rest_framework.serializers import ModelSerializer
from .models import Review, Comment, ReviewImage
from accounts.models import User
from rest_framework import serializers


class LikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'kakao_id', 'nickname']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'comment', 'create_at', 'update_at']


class ReviewImageSerializer(ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'image']


class SeatReviewListSerializer(ModelSerializer):
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'create_at', 'images', 'seat_area']


class DetailReviewSerializer(ModelSerializer):
    seat_area = serializers.SerializerMethodField()
    concert_hall_name = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    like_users = LikeUserSerializer(many=True, read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'concert_hall_name', 'images', 'create_at',
                  'update_at', 'seat_area', 'artist', 'reviews', 'comments', 'like_users']

    def get_seat_area(self, obj):
        return obj.seat_area.area

    def get_concert_hall_name(self, obj):
        return obj.seat_area.concert_hall.name