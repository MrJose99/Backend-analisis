from django.contrib import admin
from .models import Cliente, Producto, Vendedor


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nit', 'nombre', 'estatus_credito', 'correo_electronico', 'creado_en']
    list_filter = ['estatus_credito', 'creado_en']
    search_fields = ['nit', 'nombre', 'correo_electronico']
    ordering = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'precio_unitario', 'presentacion', 'creado_en']
    list_filter = ['presentacion', 'creado_en']
    search_fields = ['codigo', 'descripcion', 'color']
    ordering = ['descripcion']


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ['dpi', 'nombre', 'sueldo', 'nivel_exito', 'creado_en']
    list_filter = ['creado_en']
    search_fields = ['dpi', 'nombre', 'correo_electronico', 'telefono']
    ordering = ['nombre']
    readonly_fields = ['nivel_exito', 'creado_en', 'actualizado_en']