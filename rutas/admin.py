from django.contrib import admin
from .models import Ruta, RutaCliente, MetaVendedor


class RutaClienteInline(admin.TabularInline):
    model = RutaCliente
    extra = 0


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ['id_ruta', 'dpi_vendedor', 'fecha', 'kilometros_estimados', 
                    'tiempo_planificado_min', 'tiempo_real_min']
    list_filter = ['fecha', 'dpi_vendedor']
    search_fields = ['dpi_vendedor__nombre']
    ordering = ['-fecha']
    readonly_fields = ['tiempo_planificado_min', 'creado_en', 'actualizado_en']
    inlines = [RutaClienteInline]


@admin.register(MetaVendedor)
class MetaVendedorAdmin(admin.ModelAdmin):
    list_display = ['id_meta', 'dpi_vendedor', 'fecha_inicio', 'fecha_fin', 
                    'monto_meta', 'monto_logrado', 'estado']
    list_filter = ['estado', 'id_periodo', 'fecha_inicio']
    search_fields = ['dpi_vendedor__nombre']
    ordering = ['-fecha_inicio']
    readonly_fields = ['monto_logrado', 'creado_en', 'actualizado_en']