from django.contrib import admin
from django.urls import path, include
from mercados.views import (
    home,
    mer_view,
    demo_empresas,
    empresas_sin_paginacion,
)
from django.http import HttpResponseRedirect
from django.conf import settings


# Redirección para el botón "Ver sitio"
def redirect_to_site(request):
    return HttpResponseRedirect(settings.ADMIN_SITE_URL)


urlpatterns = [
    path("ver-sitio/", redirect_to_site, name="ver-sitio"),  # 👈 Nueva ruta
    path("", home, name="home"),
    path("catalogo/", demo_empresas, name="catalogo"),
    path("catalogo-data/", empresas_sin_paginacion, name="catalogo-data"),
    path("mer/", mer_view, name="mer"),
    path("api/", include("mercados.urls")),
    path("admin/", admin.site.urls),
]
