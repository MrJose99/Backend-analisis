from django.contrib import admin
from .models import Venta, DetalleVenta, Cobro


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id_venta', 'fecha', 'nit_cliente', 'total', 'id_ruta']
    list_filter = ['fecha', 'nit_cliente']
    search_fields = ['nit_cliente__nombre']
    ordering = ['-fecha']
    readonly_fields = ['total', 'creado_en', 'actualizado_en']
    inlines = [DetalleVentaInline]


@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    list_display = ['id_cobro', 'fecha', 'nit_cliente', 'monto', 'id_venta']
    list_filter = ['fecha', 'nit_cliente']
    search_fields = ['nit_cliente__nombre']
    ordering = ['-fecha']
    readonly_fields = ['creado_en', 'actualizado_en']