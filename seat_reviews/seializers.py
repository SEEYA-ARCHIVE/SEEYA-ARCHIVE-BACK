from django.conf import settings
from rest_framework.serializers import ModelSerializer
from .models import Review, ReviewImage, Likes
from concert_halls.models import ConcertHall, SeatArea
from rest_framework import serializers
import os


class SeatReviewsSerializer(ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = list(obj.reviewimage_set.all().values_list('image', flat=True))

        return {'preview_image': os.path.join(settings.MEDIA_URL, images[0]),
                'count_images': len(images)}

    class Meta:
        model = Review
        fields = ['id', 'create_at', 'images']


class ReviewSerializer(ModelSerializer):
    seat_area = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    concert_hall_name = serializers.SerializerMethodField()

    def get_seat_area(self, obj):
        return obj.seat_area.area

    def get_images(self, obj):
        images = list(obj.reviewimage_set.all().values_list('image', flat=True))
        return [os.path.join(settings.MEDIA_URL, image) for image in images]

    def get_concert_hall_name(self, obj):
        return obj.seat_area.concert_hall.name

    class Meta:
        model = Review
        fields = ['id', 'concert_hall_name', 'create_at', 'update_at', 'seat_area', 'images', 'artist', 'review', 'writer']

class PostImageSerializer(ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['image']


class SeatAreaSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'seat_area', 'review', 'images' ,'create_at','update_at','writer']


class ReviewUploadSerializer(ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'seat_area', 'review', 'images' ,'create_at','update_at','writer']

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        validated_data['writer'] = self.context['request'].user
        review = Review.objects.create(**validated_data)
        for image_data in images_data.getlist('images'):
            ReviewImage.objects.create(review=review, image=image_data)
        return review

class ViewComparisonSerializer(ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = list(obj.reviewimage_set.all().values_list('image', flat=True))
        return [os.path.join(settings.MEDIA_URL, image) for image in images]

    class Meta:
        model = Review
        fields = ['id', 'images', 'review']

class ReviewLikesSerializer(ModelSerializer):

    class Meta:
        model = Likes
        fields = '__all__'



class ConcertHallSerializer(serializers.ModelSerializer):
    concert_hall_id = serializers.IntegerField(source='id')

    class Meta:
        model = ConcertHall
        fields = ['concert_hall_id', 'name']

class SeatAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SeatArea
        fields = ['floor', 'area']