from django.conf import settings
from rest_framework.serializers import ModelSerializer

from concert_halls.models import ConcertHall, SeatArea
from .models import Review, Comment, ReviewImage, Likes
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
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'create_at', 'images', 'likes_count']


    def get_likes_count(self, obj):
        return len(Likes.objects.filter(review_id=obj.id))

    def get_images(self, obj):
        images = list(obj.reviewimage_set.all().values_list('image', flat=True))

        return {'preview_image': os.path.join(settings.MEDIA_URL, images[0]),
                'count_images': len(images)}




class DetailReviewSerializer(ModelSerializer):
    seat_area = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    concert_hall_name = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'concert_hall_name', 'create_at',
                  'update_at', 'seat_area', 'images', 'artist', 'review', 'comments', 'likes_count']

    def get_likes_count(self, obj):
        return len(Likes.objects.filter(review_id=obj.id))


    def get_seat_area(self, obj):
        return obj.seat_area.area

    def get_images(self, obj):
        images = list(obj.reviewimage_set.all().values_list('image', flat=True))
        return [os.path.join(settings.MEDIA_URL, image) for image in images]


    def get_concert_hall_name(self, obj):
        return obj.seat_area.concert_hall.name

    def get_user(self, obj):
        return {'user_kakao_id': obj.user.kakao_id, 'email': obj.user.email,
                'user_pk': obj.user.pk}



class SeatAreaSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'seat_area', 'review', 'images' ,'create_at','update_at','user']

class PostImageSerializer(ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['image']



class ReviewUploadSerializer(ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'seat_area', 'review', 'images' ,'create_at','update_at','user']

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        validated_data['user'] = self.context['request'].user
        review = Review.objects.create(**validated_data)
        for image_data in images_data.getlist('images'):
            ReviewImage.objects.create(review=review, image=image_data)
        return review


class ReviewLikesSerializer(ModelSerializer):

    class Meta:
        model = Likes
        fields = '__all__'


class ViewComparisonSerializer(ModelSerializer):
    images = serializers.SerializerMethodField()
    seat_area = serializers.SerializerMethodField()
    concert_hall = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    # likes = ReviewLikesSerializer(source='likes_set', many=True)
    user_nickname = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return len(Likes.objects.filter(review_id=obj.id))


    def get_images(self, obj):
        images = list(obj.reviewimage_set.all().values_list('image', flat=True))
        # return [os.path.join(settings.MEDIA_URL, image) for image in images]
        return os.path.join(settings.MEDIA_URL, images[0])

    def get_seat_area(self, obj):
        return obj.seat_area.area

    def get_concert_hall(self, obj):
        return obj.seat_area.concert_hall.name

    def get_user_nickname(self, obj):
        return obj.user.nickname

    class Meta:
        model = Review
        fields = ['id', 'images', 'review', 'seat_area', 'concert_hall', 'likes_count','user_nickname']



class ConcertHallSerializer(serializers.ModelSerializer):
    concert_hall_id = serializers.IntegerField(source='id')

    class Meta:
        model = ConcertHall
        fields = ['concert_hall_id', 'name']

class SeatAreaUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = SeatArea
        fields = ['floor', 'area']