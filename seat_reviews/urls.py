from django.urls import path, re_path

from .views import SeatReviewsViewSet, DetailReview, ReviewUploadView, ViewComparisonView

urlpatterns = [
    path('seat_areas/<int:seat_area_id>/reviews', SeatReviewsViewSet.as_view()),
    path('seat_areas/<int:seat_area_id>/reviews/<int:review_id>', DetailReview.as_view()),
    path('reviews', ReviewUploadView.as_view({'post': 'create'})),
    path('reviews/<int:review_id>', ReviewUploadView.as_view({'put': 'update',
                                                              'delete': 'destroy'})),
#http://127.0.0.1:8000/compareView?concert_hall_name=%EC%98%AC%EB%A6%BC%ED%94%BD%ED%99%80&floor=1&seat_area_name=C1
    path('compareView', ViewComparisonView.as_view()),

]