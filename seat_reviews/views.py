from rest_framework.generics import ListAPIView, RetrieveAPIView

from .seializers import SeatReviewsSerializer, ReivewSerializer
from .models import Review
from rest_framework.pagination import LimitOffsetPagination


class Pagination(LimitOffsetPagination):
    default_limit = 5


class SeatReviewsViewSet(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = SeatReviewsSerializer
    pagination_class = Pagination

    def get_queryset(self):
        seat_area_id = self.kwargs['seat_area_id']
        queryset = Review.objects.filter(seat_area_id=seat_area_id)
        return queryset


class DetailReview(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReivewSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.select_related('seat_area')
