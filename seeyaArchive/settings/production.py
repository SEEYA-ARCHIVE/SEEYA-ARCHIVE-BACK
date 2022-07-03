from .base import *



DEBUG = False

def get_secret(secret_name):
    file = open('/run/secrets/' + secret_name)
    secret = file.read()
    secret = secret.rstrip().lstrip()
    file.close()

    return secret


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


ALLOWED_HOSTS = ['localhost'
                , get_secret('HOST'),
                 '*.seeya-archive.com',
                 'api.seeya-archive.com',
                 ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'HOST': get_secret('DB_HOST'),
        'PORT': get_secret('DB_PORT'),
    }
}

# S3 설정을 위한 변수
# access key와 secret key는 본인이 생성한 iam의 정보를 사용할 것
AWS_ACCESS_KEY_ID = get_secret("MY_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_secret("MY_AWS_SECRET_ACCESS_KEY")

AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = '7th-team2-seeya-archive'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (
    AWS_STORAGE_BUCKET_NAME, AWS_REGION)
STATIC_URL = 'https://%s/' % (AWS_S3_CUSTOM_DOMAIN)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = 'https://%s/' % (AWS_S3_CUSTOM_DOMAIN)
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
