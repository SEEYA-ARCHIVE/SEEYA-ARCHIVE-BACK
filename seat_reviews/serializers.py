import uuid
import boto3
from datetime import datetime
from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from rest_framework.exceptions import APIException
from .models import Review, Comment
from accounts.models import User
from seeyaArchive.settings.base import SOCIAL_OAUTH_CONFIG

AWS_ACCESS_KEY_ID = SOCIAL_OAUTH_CONFIG['MY_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = SOCIAL_OAUTH_CONFIG['MY_AWS_SECRET_ACCESS_KEY']
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = '7th-team2-seeya-archive'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)


class ImageRequiredException(APIException):
    status_code = 204
    default_detail = 'Image is Required'
    default_code = 'NoContent'


class TooManyImagesException(APIException):
    status_code = 413
    default_detail = 'Too Many Images. Max Size is 5'
    default_code = 'RequestEntityTooLarge'


class LikeUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'kakao_id', 'nickname']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'comment', 'create_at', 'update_at']


class SeatReviewImageUploadS3Serializer(Serializer):
    def to_representation(self, image_url_list):
        imag_dict = {'image_urls': image_url_list}
        return imag_dict

    def create(self, validate_data):
        images_data = self.context['request'].FILES

        if len(images_data.getlist('image')) > 5:
            raise TooManyImagesException
        if len(images_data.getlist('image')) == 0:
            raise ImageRequiredException

        s3r = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        bucket_name = 'review-images'
        current_date = datetime.now().strftime('%Y_%m_%d-%H:%M:%S')

        image_url_list = []
        for image_data in images_data.getlist('image'):
            image_data._set_name(str(uuid.uuid4()))
            s3r.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key='%s/%s-%s' % (bucket_name, current_date, image_data),
                                                           Body=image_data, ContentType='jpg')
            image_url_list.append(AWS_S3_CUSTOM_DOMAIN + "/%s/%s-%s" % (bucket_name, current_date, image_data))
        return self.to_representation(image_url_list)


class SeatReviewListSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'image_url_array', 'seat_area', 'artist', 'reviews']


class DetailReviewSerializer(ModelSerializer):
    seat_area = SerializerMethodField()
    concert_hall_name = SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    like_users = LikeUserSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'concert_hall_name', 'image_url_array', 'create_at',
                  'update_at', 'seat_area', 'artist', 'reviews', 'comments', 'like_users']

    def get_seat_area(self, obj):
        return obj.seat_area.area

    def get_concert_hall_name(self, obj):
        return obj.seat_area.concert_hall.name


class ViewComparisonSerializer(ModelSerializer):
    count_like_users = SerializerMethodField(source='like_users')
    thumbnail_image = SerializerMethodField(source='image_url_array')
    user_nickname = SerializerMethodField()
    count_comments = SerializerMethodField()
    seat_area_name = SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user_nickname', 'thumbnail_image', 'seat_area_name', 'reviews',
                  'create_at', 'count_like_users', 'count_comments']

    def get_count_like_users(self, obj):
        return obj.like_users.count()

    def get_thumbnail_image(self, obj):
        if len(obj.image_url_array) > 0:
            return obj.image_url_array[0]

    def get_user_nickname(self, obj):
        return obj.user.nickname

    def get_count_comments(self, obj):
        return obj.comments.count()

    def get_seat_area_name(self, obj):
        return obj.seat_area.area