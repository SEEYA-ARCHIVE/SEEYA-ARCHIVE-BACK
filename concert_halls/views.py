from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import *
from .models import ConcertHall, SeatArea


class ConcertHallViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConcertHallSerializer
    queryset = ConcertHall.objects.all()
    lookup_field = "id"


class SeatAreaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SeatAreaSerializer
    lookup_field = "id"

    def get_queryset(self):
        concert_hall_id = self.kwargs['concert_hall_id']
        queryset = SeatArea.objects.filter(concert_hall_id=concert_hall_id).all()
        return queryset

