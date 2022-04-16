from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'concert_halls', views.ConcertHallViewSet, basename='concert_hall')

seat_area_router = routers.SimpleRouter(trailing_slash=False)
seat_area_router.register(r'seat_areas', views.SeatAreaViewSet, basename='seat_area')

urlpatterns = [
    path('', include(router.urls)),
    path('', views.SeatAreaViewSet.as_view({'get': 'retrieve'})),
    path('concert_halls/<int:concert_hall_id>/', include(seat_area_router.urls)),
]