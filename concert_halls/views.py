from rest_framework import viewsets, mixins, generics
from .serializers import *
from .models import ConcertHall, SeatArea
from django.db.models import Prefetch


class IndexViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConcertHallNameReviewImageSerializer
    queryset = ConcertHall.objects.all().prefetch_related(
        Prefetch("seat_areas",
                 queryset=SeatArea.objects.prefetch_related("reviews").filter(reviews__images__len__gt=0).all())).all()


class SeatLayoutViewSet(generics.ListAPIView,
                        mixins.RetrieveModelMixin):
    serializer_class = ConcertHallSeatLayoutSerializer

    def get_queryset(self):
        concert_hall_id = self.kwargs['concert_hall_id']
        queryset = ConcertHall.objects.filter(id=concert_hall_id).prefetch_related(
            Prefetch("seat_areas", queryset=SeatArea.objects.prefetch_related("reviews").all())).all()
        return queryset