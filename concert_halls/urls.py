from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'', views.IndexViewSet, basename='index')

urlpatterns = [
    path('', include(router.urls)),
    path('concert_hall/<int:concert_hall_id>/', views.SeatAreaListViewSet.as_view()),
    path('concert_hall/<int:concert_hall_id>/seat_area/<int:seat_area_id>/', views.SeatAreaViewSet.as_view()),
]