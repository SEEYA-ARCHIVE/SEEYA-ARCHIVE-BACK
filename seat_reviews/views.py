from django.contrib.auth import get_user
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from rest_framework.pagination import PageNumberPagination

from rest_framework import permissions

from concert_halls.models import SeatArea, ConcertHall
from .serializers import ReviewUploadSerializer, ViewComparisonSerializer, \
    ReviewLikesSerializer, ConcertHallSerializer, SeatAreaSerializer, SeatReviewListSerializer, CommentSerializer, \
    SeatAreaUploadSerializer, DetailReviewSerializer
from .models import Review, Likes, Comment

class IsAuthorOrReadonly(permissions.BasePermission):
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS', 'POST')

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in self.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class Pagination(PageNumberPagination):
    page_size = 6


class SeatReviewsViewSet(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = SeatReviewListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        seat_area_id = self.kwargs['seat_area_id']
        queryset = Review.objects.filter(seat_area_id=seat_area_id).order_by('-create_at')
        return queryset


class ConcertHallViewSet(ListAPIView):
    serializer_class = ConcertHallSerializer
    queryset = ConcertHall.objects.all()

class ConsertSeatAreaView(ListAPIView):
    serializer_class = SeatAreaUploadSerializer

    def get_queryset(self):
        concert_hall_id = self.kwargs['concert_hall_id']
        queryset = SeatArea.objects.filter(concert_hall_id=concert_hall_id)
        return queryset




class DetailReview(RetrieveAPIView):
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


class ConcertHallViewSet(ListAPIView):
    serializer_class = ConcertHallSerializer
    queryset = ConcertHall.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "concert_hall_id"


class ReviewUploadView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewUploadSerializer
    permission_classes = [IsAuthorOrReadonly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance_id = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer_data = {}
        serializer_data['seat_area_id'] = request.data['seat_area']
        serializer_data['review_id'] = instance_id
        return Response(serializer_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance_id = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer_data = {}
        serializer_data['seat_area_id'] = request.data['seat_area']
        serializer_data['review_id'] = instance_id
        return Response(serializer_data)

    def perform_create(self, serializer):
        concert_hall = self.request.data['concert_hall']
        concert_hall_floor = self.request.data['floor']
        concert_hall_area = self.request.data['area']
        concerthall_id = ConcertHall.objects.all().filter(name=concert_hall).first().id
        seatarea_id = SeatArea.objects.all().filter(concert_hall=concerthall_id).filter(
            floor=concert_hall_floor).filter(area=concert_hall_area).first().id
        request_data = self.request.data
        request_data['seat_area'] = seatarea_id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(user=self.request.user)

        return obj.id

    def perform_update(self, serializer):
        concert_hall = self.request.data['concert_hall']
        concert_hall_floor = self.request.data['floor']
        concert_hall_area = self.request.data['area']
        concerthall_id = ConcertHall.objects.all().filter(name=concert_hall).first().id
        seatarea_id = SeatArea.objects.all().filter(concert_hall=concerthall_id).filter(
            floor=concert_hall_floor).filter(area=concert_hall_area).first().id
        request_data = self.request.data
        request_data['seat_area'] = seatarea_id

        partial = self.kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(user=self.request.user)

        return obj.id

    # def perform_create(self, serializer):
    #     concert_hall = self.request.data['concert_hall']
    #     concert_hall_floor = self.request.data['floor']
    #     concert_hall_area = self.request.data['area']
    #     concerthall_id = ConcertHall.objects.all().filter(name=concert_hall).first().id
    #     seatarea_id = SeatArea.objects.all().filter(concert_hall=concerthall_id).filter(
    #         floor=concert_hall_floor).filter(area=concert_hall_area).first().id
    #     request_data = self.request.data
    #     request_data['seat_area'] = seatarea_id
    #
    #     serializer = self.get_serializer(data=request_data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     image_files = self.request.data.getlist('images')
    #     for image_file in image_files:
    #         image_full_url = os.path.join('review-images', image_file.name)
    #         default_storage.save(image_full_url, image_file)


class ViewComparisonView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ViewComparisonSerializer

    def get_queryset(self):
        # concerthall_id = ConcertHall.objects.all().filter(name=self.request.GET['concert_hall_name']).first().id
        # seat_area_id = SeatArea.objects.all().filter(concert_hall=concerthall_id).filter(
        #     floor=self.request.GET['floor']).filter(area=self.request.GET['seat_area_name']).first().id
        # return self.queryset.select_related('seat_area').filter(seat_area_id=seat_area_id)
        return self.queryset.select_related('seat_area').filter(seat_area_id=self.request.GET['seat_area_id'])




class ReviewLikesView(APIView):
    permission_classes = [IsAuthorOrReadonly]

    def get(self, request, review_id):
        review = Likes.objects.filter(review_id = review_id)
        like_count = review.count()
        return Response({'like_counts' : like_count} )

    def post(self,request,review_id):
        likeusers = request.user
        likepost = Review.objects.filter(id=review_id)
        # new_like = Likes(user=likeusers, review=likepost.last())
        # new_like.save()


        if Likes.objects.filter(user_id=likeusers.id, review=likepost.last()).exists():
            Likes.objects.filter(user_id=likeusers.id, review=likepost.last()).delete()
        else:
            new_like = Likes(user=likeusers, review=likepost.last())
            new_like.save()
        new_like = Likes(user=likeusers, review=likepost.last())
        serializer = ReviewLikesSerializer(data=new_like)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs['review_id'])