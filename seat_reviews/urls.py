from django.urls import path, include
from rest_framework import routers
from .views import CommentViewSet, ReviewViewSet, ReviewImageUploadViewSet, CompareViewSet, ReviewLikeViewSet

comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comment')

compare_router = routers.SimpleRouter(trailing_slash=False)
compare_router.register('compare', CompareViewSet, basename='comparison')

review_image_router = routers.SimpleRouter(trailing_slash=False)
review_image_router.register('review_images', ReviewImageUploadViewSet, basename='review_image')

review_router = routers.SimpleRouter(trailing_slash=False)
review_router.register('reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('reviews/<int:review_id>/', include(comment_router.urls)),
    path('', include(compare_router.urls)),
    path('s3/upload/', include(review_image_router.urls)),
    path('seat_areas/<int:seat_area_id>/', include(review_router.urls)),
    path('reviews/<int:review_id>/likes', ReviewLikeViewSet.as_view()),
]