from django.urls import include, path
from rest_framework import routers
from .views import CalificacionViewSet

router = routers.DefaultRouter()
router.register(r'calificaciones', CalificacionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
