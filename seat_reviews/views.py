from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly
from .serializers import SeatReviewListSerializer, DetailReviewSerializer, CommentSerializer # ViewComparisonSerializer
from .models import Review, Comment
from rest_framework.pagination import PageNumberPagination
from concert_halls.models import ConcertHall, SeatArea


class Pagination(PageNumberPagination):
    page_size = 6


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    pagination_class = Pagination
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'create':
            return SeatReviewListSerializer
        else:
            return DetailReviewSerializer

    def get_queryset(self):
        seat_area_id = self.kwargs['seat_area_id']
        return self.queryset.filter(seat_area=seat_area_id).all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        queryset = self.get_queryset()
        pk = self.kwargs['pk']

        next_id, previous_id = None, None
        next_obj = queryset.filter(id__gt=pk).first()
        if next_obj is not None:
            next_id = next_obj.id

        prev_obj = queryset.filter(id__lt=pk).last()
        if prev_obj is not None:
            previous_id = prev_obj.id

        serialized_data = serializer.data
        serialized_data['previous_id'] = previous_id
        serialized_data['next_id'] = next_id

        return Response(serialized_data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs['review_id'])


# class ViewComparisonView(ListAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ViewComparisonSerializer
#
#     def get_queryset(self):
#         concert_hall_id = ConcertHall.objects.all().filter(name=self.request.GET['concert_hall_name']).first().id
#         seat_area_id = SeatArea.objects.all().filter(concert_hall=concert_hall_id).filter(
#             floor=self.request.GET['floor']).filter(area=self.request.GET['seat_area_name']).first().id
#         return self.queryset.select_related('seat_area').filter(seat_area_id=seat_area_id)