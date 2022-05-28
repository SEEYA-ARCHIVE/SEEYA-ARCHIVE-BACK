import os

from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.files.storage import default_storage

from concert_halls.models import SeatArea, ConcertHall
from .seializers import SeatReviewsSerializer, ReviewSerializer, ReviewUploadSerializer
from .models import Review
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 6


class SeatReviewsViewSet(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = SeatReviewsSerializer
    pagination_class = Pagination

    def get_queryset(self):
        seat_area_id = self.kwargs['seat_area_id']
        queryset = Review.objects.filter(seat_area_id=seat_area_id).order_by('-create_at')
        return queryset


class DetailReview(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'review_id'

    def get_queryset(self):
        return self.queryset.select_related('seat_area').filter(seat_area_id=self.kwargs['seat_area_id'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        queryset = self.get_queryset()
        if queryset.filter(id__gt=self.kwargs['review_id']).first() is None:
            next_id = None
        else:
            next_id = queryset.filter(id__gt=self.kwargs['review_id']).first().id

        if queryset.filter(id__lt=self.kwargs['review_id']).last() is None:
            previous_id = None
        else:
            previous_id = queryset.filter(id__lt=self.kwargs['review_id']).last().id

        serialized_data = serializer.data
        serialized_data['next_id'] = next_id
        serialized_data['previous_id'] = previous_id

        return Response(serialized_data)


class ReviewUploadView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Review.objects.all()
    serializer_class = ReviewUploadSerializer

    def perform_create(self, serializer):
        concert_hall = self.request.data['concert_hall']
        concert_hall_floor = self.request.data['floor']
        concert_hall_area = self.request.data['area']
        concnerthall_id = ConcertHall.objects.all().filter(name=concert_hall).first().id
        seatarea_id = SeatArea.objects.all().filter(concert_hall=concnerthall_id).filter(
            floor=concert_hall_floor).filter(area=concert_hall_area).first().id
        request_data = self.request.data
        request_data['seat_area'] = seatarea_id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        image_files = self.request.data.getlist('images')
        for image_file in image_files:
            image_full_url = os.path.join('review-images', image_file.name)
            default_storage.save(image_full_url, image_file)
