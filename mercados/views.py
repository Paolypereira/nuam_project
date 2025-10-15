# mercados/views.py
from django.http import JsonResponse
from django.db.models import F

from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .models import Pais, Empresa
from .serializers import PaisSerializer, EmpresaSerializer

from django.shortcuts import render

def home(request):
    return JsonResponse({
        "message": "API NUAM – integración bursátil Chile, Colombia, Perú",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/",
            "top-empresas": "/api/top-empresas/?pais=CHL&n=5"
        }
    })


# -------------------------------
# Empresas (CRUD + filtros)
# -------------------------------
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    # búsqueda, orden y filtros exactos
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["ticker", "nombre", "pais__codigo", "sector", "moneda", "mercado"]
    ordering_fields = ["ticker", "nombre", "capitalizacion"]
    ordering = ["ticker"]
    lookup_field = "ticker"  # /api/empresas/{TICKER}/

    # filtros por querystring:
    # ?pais__codigo=CHL
    # ?pais__codigo__in=CHL,COL
    # ?moneda=CLP
    filterset_fields = {
        "pais__codigo": ["exact", "in"],
        "moneda": ["exact", "in"],
        "sector": ["exact"],
    }


# -------------------------------
# Países (solo lectura)
# -------------------------------
class PaisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    lookup_field = "codigo"


# -------------------------------
# Resumen: Top empresas por país
# GET /api/top-empresas/?pais=CHL&n=5
# -------------------------------
class TopEmpresasPorPais(APIView):
    def get(self, request):
        pais = request.GET.get("pais")
        try:
            n = int(request.GET.get("n", 5))
        except ValueError:
            n = 5

        qs = Empresa.objects.all()
        if pais:
            qs = qs.filter(pais__codigo__iexact=pais)

        qs = qs.order_by(F("capitalizacion").desc(nulls_last=True))[:n]

        data = [
            {
                "ticker": e.ticker,
                "nombre": e.nombre,
                "pais": e.pais.codigo if e.pais else None,
                "capitalizacion": float(e.capitalizacion) if e.capitalizacion is not None else None,
                "moneda": e.moneda,
            }
            for e in qs
        ]
        return Response({"pais": pais, "n": n, "resultados": data})


def demo_empresas(request):
    return render(request, "mercados/empresas.html")
