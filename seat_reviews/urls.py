from django.urls import path

from .views import SeatReviewsViewSet, DetailReview, ReviewUploadView

urlpatterns = [
    path('seat_areas/<int:seat_area_id>/reviews', SeatReviewsViewSet.as_view()),
    path('seat_areas/<int:seat_area_id>/reviews/<int:review_id>', DetailReview.as_view()),
    path('reviews', ReviewUploadView.as_view({'post': 'create'})),
    path('reviews/<int:review_id>', ReviewUploadView.as_view({'put': 'update',
                                                              'delete': 'destroy'})),

]