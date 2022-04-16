from django.conf import settings
from rest_framework.serializers import ModelSerializer
from .models import Review
from rest_framework import serializers
import os


class SeatReviewsSerializer(ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return {'preview_images': os.path.join(settings.MEDIA_URL, 'review-images', obj.images[0]),
                'num_images': len(obj.images)}

    class Meta:
        model = Review
        fields = ['id', 'create_at', 'images']


class ReivewSerializer(ModelSerializer):
    seat_areas = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_seat_areas(self, obj):
        return obj.seat_area.area

    def get_images(self, obj):
        return [os.path.join(settings.MEDIA_URL, 'review-images', image) for image in obj.images]

    class Meta:
        model = Review
        fields = ['id', 'create_at', 'update_at', 'seat_areas', 'images', 'artist']
