from django.contrib import admin
from django.urls import path, include
from mercados.views import home   # <-- importar
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mercados.urls')),
    path('', home, name='home'),  # <-- ya funciona
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("mercados.urls")),

    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Docs
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]