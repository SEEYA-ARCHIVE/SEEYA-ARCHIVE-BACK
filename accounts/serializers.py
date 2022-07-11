from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from .models import User


class CheckNicknameDuplicateSerializer(ModelSerializer):
    def validate(self, obj):
        nickname = obj.get('nickname')
        record = User.objects.filter(nickname=nickname)
        if len(record) > 1:
            raise ValidationError(nickname + " is Already in Use")
        return super().validate(obj)

    class Meta:
        model = User
        fields = ['nickname']


class MyPageSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'login_method']