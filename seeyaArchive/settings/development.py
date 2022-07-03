from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'seeyadb',
        'USER': 'postgres',
        'PASSWORD': 'seeyaarchive',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# Application definition

SECRET_KEY = get_secret("SECRET_KEY")


# 카카오 로그인
SOCIAL_OAUTH_CONFIG = {
    'KAKAO_REST_API_KEY': get_secret('KAKAO_REST_API_KEY'),
    'KAKAO_REDIRECT_URI': get_secret('KAKAO_REDIRECT_URI'),
    'KAKAO_SECRET_KEY': get_secret('KAKAO_SECRET_KEY'),
    'KAKAO_ADMIN_KEY': get_secret('KAKAO_ADMIN_KEY'),
}

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
