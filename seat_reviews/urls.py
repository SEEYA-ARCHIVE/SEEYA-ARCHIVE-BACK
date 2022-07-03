from django.urls import path, include
from rest_framework import routers

from .views import SeatReviewsViewSet, DetailReview, ReviewUploadView, \
    ViewComparisonView, ReviewLikesView, ConcertHallViewSet, ConsertSeatAreaView,  CommentViewSet


comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('seat_areas/<int:seat_area_id>/reviews', SeatReviewsViewSet.as_view()),
    path('seat_areas/<int:seat_area_id>/reviews/<int:review_id>', DetailReview.as_view()),
    path('reviews/concert_halls', ConcertHallViewSet.as_view()),
    path('reviews/concert_halls/<int:concert_hall_id>/seat_areas', ConsertSeatAreaView.as_view()),

    path('reviews', ReviewUploadView.as_view({'post': 'create'})),
    path('reviews/<int:review_id>', ReviewUploadView.as_view({'put': 'update',
                                                              'delete': 'destroy'})),

# http://127.0.0.1:8000/compare_view?concert_hall_name=%EC%98%AC%EB%A6%BC%ED%94%BD%ED%99%80&floor=1&seat_area_name=C1
# http://127.0.0.1:8000/compare_view?seat_area_id=1
    path('compare_view', ViewComparisonView.as_view()),
    path('reviews/<int:review_id>/likes', ReviewLikesView.as_view()),
    path('seat_areas/<int:seat_area_id>/reviews/<int:review_id>/', include(comment_router.urls)),

]