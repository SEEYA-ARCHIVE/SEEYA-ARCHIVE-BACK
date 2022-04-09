from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from seeyaArchive.seat_reviews.models import Post


class IndexViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConcertHallNameReviewImageSerializer

    def get_queryset(self):
        queryset = Post.objects.values('images')[:5]
        for q in queryset:
            print(q)
            print(type(q))
        return queryset