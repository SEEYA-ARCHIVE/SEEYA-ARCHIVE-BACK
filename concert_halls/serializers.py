from rest_framework import serializers
from .models import ConcertHall, SeatArea


class ReviewNestingSeatAreaSerializer(serializers.ModelSerializer):
    reviews = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='images',
    )

    class Meta:
        model = SeatArea
        fields = ['id', 'reviews']


class ConcertHallNameReviewImageSerializer(serializers.ModelSerializer):
    seat_areas = ReviewNestingSeatAreaSerializer(many=True, read_only=True)

    class Meta:
        model = ConcertHall
        fields = ['id', 'name', 'seat_areas']


class SeatAreaSerializer(serializers.ModelSerializer):
    count_reviews = serializers.SerializerMethodField()

    def get_count_reviews(self, obj):
        return obj.reviews.count()

    class Meta:
        model = SeatArea
        fields = ['id', 'floor', 'area', 'count_reviews']


class ConcertHallSeatLayoutSerializer(serializers.ModelSerializer):
    seat_areas = SeatAreaSerializer(many=True, read_only=True)

    class Meta:
        model = ConcertHall
        fields = ['name', 'seat_areas']