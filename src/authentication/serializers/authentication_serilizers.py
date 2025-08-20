from django.contrib.auth import get_user_model
from rest_framework import serializers

from authentication.serializers.user_serilizer import UserSerializer

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email__iexact=attrs["email"])
            if not user.check_password(attrs["password"]):
                raise serializers.ValidationError("Wrong password!")

        except Exception:
            raise serializers.ValidationError(
                {"password": "Email or password is incorrect"}
            )
        return attrs


class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserSerializer()
