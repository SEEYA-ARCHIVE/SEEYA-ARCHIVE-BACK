from django.conf import settings
from rest_framework.serializers import ModelSerializer, Serializer
from .models import Review
from rest_framework import serializers
from concert_halls.models import SeatArea
import os

class SeatReviewsUploadSerializer(ModelSerializer):
    images = serializers.SerializerMethodField()
    # num_reviews = serializers.SerializerMethodField()


    def get_images(self, obj):
        return {'preview_images' : obj.images[0] ,'num_images' : len(obj.images)}

    # def get_num_reviews(self, obj):
    #     # return len(self.root.instance)
    #
    #     return len(self.instance)
    class Meta:
        model = Review
        fields = ["id", "create_at", "images"]

class SeatAreaSerializer(ModelSerializer):
    # seat_areas = serializers.SerializerMethodField()
    #
    # def get_seat_areas(self, obj):
    #     return obj.seat_area

    class Meta:
        model = SeatArea
        fields = ["area"]



class ReivewSerializer(ModelSerializer):
    seat_areas = serializers.SerializerMethodField()
    # images = serializers.SerializerMethodField()

    def get_seat_areas(self, obj):
        return obj.seat_area.area

    # def get_images(self, obj):
    #     return [os.path.join(settings.MEDIA_URL ,x) for x in obj.images]


    class Meta:
        model = Review
        fields = ["id", "create_at", "update_at","seat_areas", "images", "artist"]
