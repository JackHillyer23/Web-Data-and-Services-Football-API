# football_api/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, PlayerViewSet, MatchViewSet, StatsViewSet

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'stats', StatsViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Football API",
      default_version='v1',
      description="API documentation for Football API project",
      contact=openapi.Contact(email="your-email@example.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),

    # Swagger/OpenAPI endpoints
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]