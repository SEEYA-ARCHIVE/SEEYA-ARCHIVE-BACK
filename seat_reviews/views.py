
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .seializers import SeatReviewsUploadSerializer, ReivewSerializer
from .models import Review
from rest_framework.pagination import LimitOffsetPagination

class MyOffsetPagination(LimitOffsetPagination):
    default_limit = 5

class SeatReviewsUpload(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = SeatReviewsUploadSerializer
    permission_classes = []
    pagination_class = MyOffsetPagination

    def get_queryset(self):
        seat_area_id = self.kwargs['seat_area_id']
        post_reviews = Review.objects.filter(seat_area_id=seat_area_id)
        return post_reviews

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, args, kwargs)
    #     response.data += [{"count": self.get_queryset().count()}]
    #     return response

class ReviewList(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReivewSerializer
    permission_classes = []
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.select_related('seat_area')

