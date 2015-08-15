from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from studioservices.models import AndroidDevice, BlendFile

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, style={'input_type': 'password'})
    password2 = serializers.CharField(max_length=128, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "The passwords don't match"})
        return attrs

    def validate_username(self, value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError("This user already exists")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk','username',)


class AuthTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token

    def to_representation(self, instance):
        return {
            'token': instance.key,
            'user': instance.user.username,
            'created': instance.created
        }

class AndroidDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AndroidDevice
        fields = ('android_id', 'name')

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'android_id': instance.android_id,
            'name': instance.name,
            'user': instance.user.username,
            'last_connection': instance.last_connection,
            'is_connected': instance.is_connected
        }


class BlendFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlendFile
        fields = ('file', )

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'filename': instance.filename,
            'upload_date': instance.upload_date,
            'user': instance.user.username
        }