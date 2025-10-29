from django.contrib import admin, messages
from django.http import HttpResponse
import csv

from .models import (
    Pais, Normativa, Empresa,
    InstrumentoNoInscrito, CalificacionTributaria,
    HistorialCambio, ArchivoCargaMasiva, ValorInstrumento
)
from .utils_import import import_empresas_from_excel  # 👈 nuevo

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def exportar_empresas_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="empresas.csv"'
    writer = csv.writer(response)
    writer.writerow([
        "ticker", "nombre", "pais_codigo", "pais_nombre",
        "sector", "moneda", "capitalizacion", "mercado", "fuente", "fecha_reporte",
    ])
    for e in queryset.select_related("pais"):
        writer.writerow([
            e.ticker,
            e.nombre,
            e.pais.codigo if e.pais else "",
            e.pais.nombre if e.pais else "",
            e.sector or "",
            e.moneda or "",
            (f"{e.capitalizacion:.2f}" if e.capitalizacion is not None else ""),
            e.mercado or "",
            e.fuente or "",
            e.fecha_reporte.isoformat() if e.fecha_reporte else "",
        ])
    return response
exportar_empresas_csv.short_description = "Exportar selección a CSV"


# -------------------------------------------------------------------
# ADMIN PERSONALIZADO PARA EL PANEL DE NUAM
# -------------------------------------------------------------------

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "moneda", "bolsa_nombre")
    search_fields = ("codigo", "nombre", "moneda", "bolsa_nombre")
    list_filter = ("moneda",)
    ordering = ("codigo",)
    list_per_page = 50
    save_on_top = True


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("ticker", "nombre", "pais", "sector", "moneda", "capitalizacion_fmt")
    search_fields = ("ticker", "nombre", "pais__codigo", "pais__nombre", "sector", "moneda")
    list_filter = ("pais", "sector", "moneda")
    ordering = ("ticker",)
    list_per_page = 50
    save_on_top = True
    actions = [exportar_empresas_csv]
    autocomplete_fields = ("pais",)

    @admin.display(description="Capitalización", ordering="capitalizacion")
    def capitalizacion_fmt(self, obj):
        if obj.capitalizacion is None:
            return "—"
        return f"{obj.capitalizacion:,.2f}"


@admin.register(Normativa)
class NormativaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "pais", "numero", "fecha_promulgacion", "tema")
    search_fields = ("titulo", "numero", "tema", "pais__codigo", "pais__nombre")
    list_filter = ("pais", "tema")
    date_hierarchy = "fecha_promulgacion"
    list_per_page = 50
    save_on_top = True


@admin.register(InstrumentoNoInscrito)
class InstrumentoNoInscritoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "emisor", "pais_origen", "tipo", "fecha_solicitud", "estado")
    list_filter = ("pais_origen", "tipo", "estado")
    search_fields = ("nombre", "emisor")
    date_hierarchy = "fecha_solicitud"
    list_per_page = 50
    save_on_top = True


# ========= AQUI ESTÁ LA CLASE MODIFICADA =========
@admin.register(ArchivoCargaMasiva)
class ArchivoCargaMasivaAdmin(admin.ModelAdmin):
    list_display = ("archivo", "fecha_subida", "procesado", "resultado")
    readonly_fields = ("fecha_subida",)
    list_filter = ("procesado",)
    list_per_page = 50
    save_on_top = True
    actions = ["procesar_empresas_desde_excel"]  # 👈 acción nueva

    def procesar_empresas_desde_excel(self, request, queryset):
        """
        Toma el/los archivos seleccionados, los procesa y carga/actualiza Empresas.
        Guarda el resultado en el propio registro.
        """
        for obj in queryset:
            try:
                path = obj.archivo.path  # ruta completa en disco
            except Exception:
                messages.error(request, f"No se pudo resolver la ruta del archivo: {obj.archivo}")
                continue

            res = import_empresas_from_excel(path)
            obj.procesado = bool(res.get("ok"))
            obj.resultado = res.get("msg", "")
            obj.save(update_fields=["procesado", "resultado"])

            if res.get("ok"):
                messages.success(request, f"{obj.archivo.name}: {res['msg']}")
            else:
                messages.error(request, f"{obj.archivo.name}: {res['msg']}")
    procesar_empresas_desde_excel.short_description = "Procesar Excel y cargar/actualizar empresas"
# =================================================


@admin.register(HistorialCambio)
class HistorialCambioAdmin(admin.ModelAdmin):
    list_display = ("fecha", "tipo", "pais_afectado", "usuario")
    list_filter = ("tipo", "pais_afectado")
    date_hierarchy = "fecha"
    list_per_page = 50
    save_on_top = True


@admin.register(ValorInstrumento)
class ValorInstrumentoAdmin(admin.ModelAdmin):
    list_display = ("instrumento", "fecha", "valor", "moneda")
    list_filter = ("moneda", "fecha")
    date_hierarchy = "fecha"
    list_per_page = 50
    save_on_top = True


# -------------------------------------------------------------------
# PERSONALIZACIÓN VISUAL DEL PANEL
# -------------------------------------------------------------------
admin.site.site_header = "Administración NUAM"
admin.site.site_title = "NUAM Admin"
admin.site.index_title = "Panel de control NUAM"
admin.site.site_url = "http://127.0.0.1:8000/"
