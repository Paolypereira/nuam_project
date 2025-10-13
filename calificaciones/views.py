from rest_framework import viewsets
from .models import CalificacionTributaria
from .serializers import CalificacionTributariaSerializer

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = CalificacionTributaria.objects.all()
    serializer_class = CalificacionTributariaSerializer
