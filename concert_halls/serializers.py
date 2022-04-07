from rest_framework import serializers
from .models import ConcertHall, Floor, Seat


class ConcertHallNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcertHall
        fields = ['name']


class ConcertHallSeatLayoutSerializer(serializers.ModelSerializer):
    floor_model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='')

    class Meta:
        model = ConcertHall
        fields = []