from rest_framework import viewsets, mixins, generics
from .serializers import *
from .models import ConcertHall, SeatArea
from django.db.models import Prefetch