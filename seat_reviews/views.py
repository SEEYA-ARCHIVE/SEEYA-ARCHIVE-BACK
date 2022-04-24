
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .seializers import SeatReviewsSerializer, ReivewSerializer
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
        queryset = Review.objects.filter(seat_area_id=seat_area_id)
        return queryset


class DetailReview(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReivewSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'review_id'

    def get_queryset(self):
        return self.queryset.select_related('seat_area').filter(seat_area_id=self.kwargs['seat_area_id'])

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #
    #     if instance == self.queryset.order_by("id").last():
    #         next_id = None
    #     else:
    #         next_id = self.queryset.filter(id__lt=instance.id).order_by("id").last()
    #
    #     if instance == self.queryset.order_by("id").first():
    #         previous_id = None
    #     else:
    #         previous_id = self.queryset.filter(id__lt=instance.id).order_by("id").first()
    #     serializer.data['next_id'] = next_id
    #     serializer.data['previous_id'] = previous_id
    #
    #     return Response(serializer.data)
