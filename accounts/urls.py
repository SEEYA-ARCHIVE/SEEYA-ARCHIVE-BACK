from django.urls import include, path
from rest_framework import routers
from . import views

# account_router = routers.SimpleRouter(trailing_slash=False)
# account_router.register('accounts', views.getUserInfo, basename='account')

urlpatterns = [
    path('kakao_login/', views.kakao_login),
    path('kakao_logout/', views.kakao_logout),
    # path('logout/', views.logout),
    path('accounts/kakao/login/callback/', views.kakao_login_callback),
]