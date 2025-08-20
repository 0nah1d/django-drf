from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:
    model = User

    def __init__(self, user=None):
        self._user = user

    def authenticate_user(self, email: str):
        user = self.model.objects.get(email__iexact=email)

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "username": user.username,
            },
        }
