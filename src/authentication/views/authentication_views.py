import traceback

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers.authentication_serilizers import LoginSerializer, LoginResponseSerializer
from authentication.services.auth_service import AuthService
from common.serializers import EmptySerializer


@extend_schema(tags=["Authentication"])
class AuthenticationViewSet(viewsets.ViewSet):
    queryset = []
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "login":
            return LoginSerializer
        return EmptySerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def list(self, request):
        return Response([])

    @extend_schema(
        request=LoginSerializer,
        operation_id="login",
        responses=LoginResponseSerializer,
    )
    @action(detail=False, methods=["POST"], url_path="login")
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            auth_service = AuthService()
            auth_data = auth_service.authenticate_user(
                serializer.validated_data["email"]
            )

            serializer = LoginResponseSerializer(
                auth_data, context={"request": request}
            )

            return Response(serializer.data)
        except Exception as e:
            traceback.print_exc()
            raise e
