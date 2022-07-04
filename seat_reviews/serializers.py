import os
import uuid
from datetime import datetime
from django.conf import settings
from rest_framework.serializers import ModelSerializer
from .models import Review, Comment, ReviewImage
from accounts.models import User
from rest_framework import serializers
import boto3
from seeyaArchive.settings.base import SOCIAL_OAUTH_CONFIG

AWS_ACCESS_KEY_ID = SOCIAL_OAUTH_CONFIG['MY_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = SOCIAL_OAUTH_CONFIG['MY_AWS_SECRET_ACCESS_KEY']
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = '7th-team2-seeya-archive'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)


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
    image = serializers.SerializerMethodField()

    class Meta:
        model = ReviewImage
        fields = ['image']

    def get_image(self, obj):
        return obj.image.url


class SeatReviewListSerializer(ModelSerializer):
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'images', 'seat_area', 'artist', 'reviews']

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        review = Review.objects.create(**validated_data)
        s3r = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        bucket_name = 'review-images'
        current_date = datetime.now().strftime('%Y_%m_%d-%H:%M:%S')
        for image_data in images_data.getlist('image'):
            image_data._set_name(str(uuid.uuid4()))
            s3r.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key='%s/%s-%s' % (bucket_name, current_date, image_data),
                                                           Body=image_data, ContentType='jpg')
            ReviewImage.objects.create(review=review, image=AWS_S3_CUSTOM_DOMAIN + "/%s/%s-%s" % (
                bucket_name, current_date, image_data))
        return review


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

# class ViewComparisonSerializer(ModelSerializer):
#     images = serializers.SerializerMethodField()
#
#     def get_images(self, obj):
#         images = list(obj.reviewimage_set.all().values_list('image', flat=True))
#         return [os.path.join(settings.MEDIA_URL, image) for image in images]
#
#     class Meta:
#         model = Review
#         fields = ['id', 'images', 'reviews']
