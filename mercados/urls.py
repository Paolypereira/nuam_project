from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet, PaisViewSet, TopEmpresasPorPais, demo_empresas

router = DefaultRouter()
router.register(r"empresas", EmpresaViewSet, basename="empresa")
router.register(r"paises", PaisViewSet, basename="pais")

urlpatterns = [
    path("top-empresas/", TopEmpresasPorPais.as_view(), name="top-empresas"),
    path("demo/empresas/", demo_empresas, name="demo-empresas"),  # 👈
]
urlpatterns += router.urls