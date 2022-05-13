from django.conf import settings
from rest_framework.serializers import ModelSerializer
from .models import Review
from rest_framework import serializers
import os


class SeatReviewsSerializer(ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return {'preview_image': os.path.join(settings.MEDIA_URL, 'review-images', obj.images[0]),
                'count_images': len(obj.images)}

    class Meta:
        model = Review
        fields = ['id', 'create_at', 'images','update_at']


class ReviewSerializer(ModelSerializer):
    seat_area = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    concert_hall_name = serializers.SerializerMethodField()

    def get_seat_area(self, obj):
        return obj.seat_area.area

    def get_images(self, obj):
        return [os.path.join(settings.MEDIA_URL, 'review-images', image) for image in obj.images]

    def get_concert_hall_name(self, obj):
        return obj.seat_area.concert_hall.name

    class Meta:
        model = Review
        fields = ['id', 'concert_hall_name', 'create_at', 'update_at', 'seat_area', 'images', 'artist']
