from django.urls import path, include
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from authentication.views import UsersViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='hello')

urlpatterns = [
    path('rest-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("schema.json", SpectacularJSONAPIView.as_view(), name="schema"),
]
