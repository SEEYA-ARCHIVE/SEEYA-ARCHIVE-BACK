from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import login, logout

from seeyaArchive.settings.base import SOCIAL_OAUTH_CONFIG

import random
import requests
from http import HTTPStatus
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import GenericAPIView
from .models import User
from .serializers import MyPageSerializer

KAKAO_REST_API_KEY = SOCIAL_OAUTH_CONFIG['KAKAO_REST_API_KEY']
KAKAO_REDIRECT_URI = SOCIAL_OAUTH_CONFIG['KAKAO_REDIRECT_URI']
KAKAO_SECRET_KEY = SOCIAL_OAUTH_CONFIG['KAKAO_SECRET_KEY']
KAKAO_ADMIN_KEY = SOCIAL_OAUTH_CONFIG['KAKAO_ADMIN_KEY']


class SetNicknameView(RetrieveModelMixin,
                      UpdateModelMixin,
                      GenericAPIView):
    queryset = User.objects.all()
    serializer_class = MyPageSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        return self.queryset.get(pk=self.request.user.pk)


@api_view(['GET'])
def kakao_login(request):
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
    )


@api_view(['GET'])
def kakao_login_callback(request):
    code = request.GET.get("code", None)
    request_access_token = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&code={code}&client_secret={KAKAO_SECRET_KEY}",
        headers={"Accept": "application/json"},
    )
    access_token_json = request_access_token.json()
    access_token = access_token_json.get("access_token")
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Authorization": f"Bearer {access_token}"},
    )
    token_info = requests.get(
        "https://kapi.kakao.com/v1/user/access_token_info",
        headers={"Authorization": f"Bearer {access_token}", },
    )
    json_response = profile_request.json()
    kakao_account = json_response.get("kakao_account")
    kakao_id = json_response.get('id')
    email = kakao_account.get("email", None)
    gender = kakao_account.get("gender", None)
    birth_year = kakao_account.get("birthyear", None)
    birthday_type = kakao_account.get("birthday_type", None)
    birthday = kakao_account.get("birthday", None)
    age_range = kakao_account.get("age_range", None)
    name = kakao_account.get("name", None)
    profile = kakao_account.get("profile", None)

    profile_image_url = None
    if profile is not None:
        profile_image_url = profile.get("profile_image_url")
    user = User.objects.filter(kakao_id=kakao_id).first()
    if user is not None:
        login(request, user)
        return Response(status=HTTPStatus.OK)
    else:
        user = User.objects.create_user(
            kakao_id=kakao_id,
            email=email,
            username=kakao_id,
            nickname=make_random_nickname(kakao_id),
            profile_image_url=profile_image_url,
            gender=gender,
            age_range=age_range,
            birth_year=birth_year,
            birthday_type=birthday_type,
            birthday=birthday,
            account_name=name,
            login_method=User.LOGIN_KAKAO,
            password=None,
        )
        user.set_unusable_password()
        user.save()
        login(request, user)
        return Response(status=HTTPStatus.CREATED)


@csrf_exempt
def kakao_logout(request):
    requests.post(
        f"https://kapi.kakao.com/v1/user/logout?target_id_type=user_id&target_id={request.user.kakao_id}",
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Authorization": f"KakaoAK {KAKAO_ADMIN_KEY}"},
    )
    logout(request)
    return redirect("/")


def kakao_withdrawal(request):
    user = User.objects.get(pk=request.user.pk)
    requests.post(
        f"https://kapi.kakao.com/v1/user/unlink?target_id_type=user_id&target_id={request.user.kakao_id}",
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Authorization": f"KakaoAK {KAKAO_ADMIN_KEY}"},
    )
    logout(request)
    user.delete()
    return redirect("/")


def make_random_nickname(kakao_id):
    random_nickname = str(kakao_id)
    with open('accounts/words.txt', encoding='utf-8') as f:
        nicknames = f.read().splitlines()
    for i in range(2):
        random_nickname += random.choice(nicknames)
    return random_nickname