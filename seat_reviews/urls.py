from django.urls import path, include
from rest_framework import routers
from .views import ReviewListViewSet, DetailReviewViewSet, CommentViewSet

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('seat_areas/<int:seat_area_id>/reviews/', ReviewListViewSet.as_view()),
    path('seat_areas/<int:seat_area_id>/reviews/<int:review_id>', DetailReviewViewSet.as_view()),
    path('seat_areas/<int:seat_area_id>/reviews/<int:review_id>/', include(comment_router.urls)),
]