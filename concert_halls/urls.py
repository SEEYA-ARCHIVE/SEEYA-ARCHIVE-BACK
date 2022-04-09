from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'concert_halls'

router = routers.SimpleRouter()
# naming....... 뭐라해...... 지끈~
router.register(r'index', views.IndexViewSet, basename='index')

urlpatterns = [
    path('', include(router.urls)),
]