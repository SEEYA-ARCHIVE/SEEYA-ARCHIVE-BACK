from django.urls import include, path
from rest_framework import routers
from . import views


urlpatterns = [
    path('kakao_login/', views.kakao_login),
    path('kakao_logout/', views.kakao_logout),
    path('kakao_secession/', views.kakao_secession),
    path('accounts/kakao/login/callback/', views.kakao_login_callback),
    path('me/', views.SetNicknameView.as_view()),
]