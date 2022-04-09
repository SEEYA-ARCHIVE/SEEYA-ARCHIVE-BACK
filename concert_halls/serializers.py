from rest_framework import serializers
from .models import ConcertHall, Floor, Seat
from seat_reviews import Post


class ConcertHallNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcertHall
        fields = ['name']


class SeatReviewImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['images']


class ConcertHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcertHall
        fields = ['name', 'address', 'lat', 'lng']


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['concert_hall', 'floor']


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['seat_floor', 'area', 'seat_row', 'seat_num']


class ConcertHallNameReviewImageSerializer(serializers.ModelSerializer):
    concert_hall_name = ConcertHallNameListSerializer
    review_image = SeatReviewImageListSerializer

    class Meta:
        fields = ['concert_hall_name', 'review_image']


class ConcertHallSeatLayoutSerializer(serializers.ModelSerializer):
    concert_hall_name = ConcertHallNameListSerializer(many=True)
    seat = SeatSerializer(many=True)

    class Meta:
        fields = ['concert_hall_name', 'seat']