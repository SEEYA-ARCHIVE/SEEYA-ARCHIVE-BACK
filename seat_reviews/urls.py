from django.urls import path
from .views import SeatReviewsUpload,ReviewList



urlpatterns = [

    path("seat_area/<int:seat_area_id>/reviews/",SeatReviewsUpload.as_view()),
    path("reviews/<int:id>", ReviewList.as_view())

]