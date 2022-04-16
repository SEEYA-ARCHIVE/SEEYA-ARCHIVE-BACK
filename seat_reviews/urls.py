from django.urls import path
from .views import SeatReviewsViewSet, DetailReview

urlpatterns = [
    path('seat_area/<int:seat_area_id>/reviews/', SeatReviewsViewSet.as_view()),
    path('reviews/<int:id>', DetailReview.as_view())
]