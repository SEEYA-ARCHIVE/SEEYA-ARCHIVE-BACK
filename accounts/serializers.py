from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from .models import User


class MyPageSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'kakao_id', 'nickname', 'email', 'login_method']

    def validate(self, obj):
        nickname = obj.get('nickname')
        record = User.objects.filter(nickname=nickname)
        if record:
            raise ValidationError(nickname + " is Already in Use")
        return super().validate(obj)