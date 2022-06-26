from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .serializers import SeatReviewListSerializer, DetailReviewSerializer, CommentSerializer
from .models import Review, Comment
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 6


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class ReviewListViewSet(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = SeatReviewListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        seat_area_id = self.kwargs['seat_area_id']
        queryset = Review.objects.filter(seat_area_id=seat_area_id).order_by('-create_at')
        return queryset


class DetailReviewViewSet(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = DetailReviewSerializer
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


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs['review_id'])