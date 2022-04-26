from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'seeyadb',
        'USER': 'seeyadb',
        'PASSWORD': 'seeyaarchive123!',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# S3 설정을 위한 변수
# access key와 secret key는 본인이 생성한 iam의 정보를 사용할 것
# AWS_ACCESS_KEY_ID = get_secret('MY_AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = get_secret('MY_AWS_SECRET_ACCESS_KEY')

AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = '7th-team2-seeya-archive'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (
    AWS_STORAGE_BUCKET_NAME, AWS_REGION)
STATIC_URL = 'https://%s/' % (AWS_S3_CUSTOM_DOMAIN)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = 'https://%s/' % (AWS_S3_CUSTOM_DOMAIN)

MEDIA_URL = 'https://%s/' % (AWS_S3_CUSTOM_DOMAIN)
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
