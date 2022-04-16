from rest_framework import serializers
from .models import ConcertHall, SeatArea


class ConcertHallSerializer(serializers.ModelSerializer):
    concert_hall_id = serializers.IntegerField(source='id')

    class Meta:
        model = ConcertHall
        fields = ['concert_hall_id', 'name', 'address', 'lat', 'lng']


class SeatAreaSerializer(serializers.ModelSerializer):
    count_reviews = serializers.SerializerMethodField()
    seat_area_id = serializers.IntegerField(source='id')

    def get_count_reviews(self, obj):
        return obj.reviews.count()

    class Meta:
        model = SeatArea
        fields = ['seat_area_id', 'floor', 'area', 'count_reviews']

# class ReviewNestingSeatAreaSerializer(serializers.ModelSerializer):
#     seat_area_id = serializers.IntegerField(source='id')
#     reviews = serializers.SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='images',
#     )
#
#     class Meta:
#         model = SeatArea
#         fields = ['seat_area_id', 'reviews']
#
#
# class ConcertHallNameReviewImageSerializer(serializers.ModelSerializer):
#     seat_areas = ReviewNestingSeatAreaSerializer(many=True, read_only=True)
#     concert_hall_id = serializers.IntegerField(source='id')
#
#     class Meta:
#         model = ConcertHall
#         fields = ['concert_hall_id', 'name', 'seat_areas']
#
#
# class SeatAreaSerializer(serializers.ModelSerializer):
#     count_reviews = serializers.SerializerMethodField()
#     seat_area_id = serializers.IntegerField(source='id')
#
#     def get_count_reviews(self, obj):
#         return obj.reviews.count()
#
#     class Meta:
#         model = SeatArea
#         fields = ['seat_area_id', 'floor', 'area', 'count_reviews']
#
#
# class ConcertHallSeatAreaSerializer(serializers.ModelSerializer):
#     seat_areas = SeatAreaSerializer(many=True, read_only=True)
#     concert_hall_id = serializers.IntegerField(source='id')
#
#     class Meta:
#         model = ConcertHall
#         fields = ['concert_hall_id', 'name', 'seat_areas']