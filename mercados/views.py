from django.shortcuts import render
from django.db.models import F
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend

from .models import Pais, Empresa
from .serializers import PaisSerializer, EmpresaSerializer


# HOME (landing con tarjetas)
def home(request):
    return render(request, "home.html", {
        "title": "NUAM – Mantenedor & API",
        "links": {
            "catalogo": "/catalogo/",
            "admin": "/admin/",
            "mer": "/mer/",
        }
    })


# CATÁLOGO EMPRESAS (frontend que lista empresas)
def demo_empresas(request):
    return render(request, "empresas.html", {
        "title": "Catálogo de Empresas"
    })


# DIAGRAMA NUAM (M.E.R.)
def mer_view(request):
    return render(request, "mer.html", {
        "title": "Diagrama NUAM (M.E.R.)"
    })


# -------- API REST principal (DRF con paginación) --------
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["ticker", "nombre", "pais__codigo", "sector", "moneda", "mercado"]
    ordering_fields = ["ticker", "nombre", "capitalizacion"]
    ordering = ["ticker"]
    lookup_field = "ticker"

    filterset_fields = {
        "pais__codigo": ["exact", "in"],
        "moneda": ["exact", "in"],
        "sector": ["exact"],
    }


class PaisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    lookup_field = "codigo"


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


# -------- Endpoint SIN paginación para el front /catalogo-data/ --------
@api_view(["GET"])
def empresas_sin_paginacion(request):
    """
    Devuelve TODAS las empresas en una sola lista simple, sin paginación,
    ordenadas por ticker. Esta es la que consume /catalogo/.
    """
    qs = (
        Empresa.objects
        .all()
        .order_by("ticker")
        .values(
            "ticker",
            "nombre",
            "moneda",
            "capitalizacion",
            "pais__codigo",
        )
    )

    data = [
        {
            "ticker": row["ticker"],
            "nombre": row["nombre"],
            "pais": row["pais__codigo"],
            "moneda": row["moneda"],
            "capitalizacion": float(row["capitalizacion"]) if row["capitalizacion"] is not None else None,
        }
        for row in qs
    ]

    return Response(data)
