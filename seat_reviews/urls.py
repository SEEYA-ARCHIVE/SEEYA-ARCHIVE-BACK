from django.urls import path, include
from rest_framework import routers
from .views import CommentViewSet, ReviewViewSet

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comment')

review_router = routers.SimpleRouter(trailing_slash=False)
review_router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('seat_areas/<int:seat_area_id>/reviews/<int:review_id>/', include(comment_router.urls)),
    path('seat_areas/<int:seat_area_id>/', include(review_router.urls)),
]