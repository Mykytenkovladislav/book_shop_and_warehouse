from django.conf import settings
from django.conf.urls import url
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from storehouse import views

router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="WAREHOUSE API",
        default_version="v1",
        description="API for WAREHOUSE application",
    ),
    url=settings.SWAGGER_SETTINGS["DEFAULT_API_URL"],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

swagger_patterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

router.register(r'orders', views.OrderViewSet)
router.register(r'order_items', views.OrderItemViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'book_instances', views.BookInstanceViewSet)
router.register(r'genre', views.GenreViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]

if settings.DEBUG:
    urlpatterns += swagger_patterns
