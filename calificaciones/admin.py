from django.contrib import admin
from .models import InstrumentoNoInscrito, CalificacionTributaria, HistorialCambio, ArchivoCargaMasiva

admin.site.register(InstrumentoNoInscrito)
admin.site.register(CalificacionTributaria)
admin.site.register(HistorialCambio)
admin.site.register(ArchivoCargaMasiva)
