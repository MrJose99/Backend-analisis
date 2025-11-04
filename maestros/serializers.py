from rest_framework import serializers
from .models import Cliente, Producto, Vendedor
from core.models import EstatusCredito, Presentacion


class EstatusCreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstatusCredito
        fields = ['estatus_credito', 'descripcion']


class PresentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentacion
        fields = ['presentacion', 'descripcion']


class ClienteListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""
    estatus_credito_display = serializers.CharField(
        source='estatus_credito.descripcion',
        read_only=True
    )
    
    class Meta:
        model = Cliente
        fields = [
            'nit',
            'nombre',
            'estatus_credito',
            'estatus_credito_display',
            'correo_electronico',
        ]


class ClienteDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalle"""
    estatus_credito_info = EstatusCreditoSerializer(
        source='estatus_credito',
        read_only=True
    )
    
    class Meta:
        model = Cliente
        fields = [
            'nit',
            'nombre',
            'direccion',
            'correo_electronico',
            'estatus_credito',
            'estatus_credito_info',
            'creado_en',
            'actualizado_en',
        ]
        read_only_fields = ['creado_en', 'actualizado_en']


class ClienteCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar"""
    
    class Meta:
        model = Cliente
        fields = [
            'nit',
            'nombre',
            'direccion',
            'correo_electronico',
            'estatus_credito',
        ]
    
    def validate_nit(self, value):
        """Validar que el NIT solo contenga dígitos"""
        if not value.isdigit():
            raise serializers.ValidationError("El NIT debe contener solo dígitos")
        if len(value) != 9:
            raise serializers.ValidationError("El NIT debe tener exactamente 9 dígitos")
        return value


class ProductoListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""
    presentacion_display = serializers.CharField(
        source='presentacion.descripcion',
        read_only=True
    )
    
    class Meta:
        model = Producto
        fields = [
            'codigo',
            'descripcion',
            'precio_unitario',
            'presentacion',
            'presentacion_display',
        ]


class ProductoDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalle"""
    presentacion_info = PresentacionSerializer(
        source='presentacion',
        read_only=True
    )
    
    class Meta:
        model = Producto
        fields = [
            'codigo',
            'descripcion',
            'color',
            'precio_unitario',
            'presentacion',
            'presentacion_info',
            'creado_en',
            'actualizado_en',
        ]
        read_only_fields = ['creado_en', 'actualizado_en']


class ProductoCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar"""
    
    class Meta:
        model = Producto
        fields = [
            'codigo',
            'descripcion',
            'color',
            'precio_unitario',
            'presentacion',
        ]
    
    def validate_precio_unitario(self, value):
        """Validar que el precio sea positivo"""
        if value < 0:
            raise serializers.ValidationError("El precio debe ser mayor o igual a 0")
        return value


class VendedorListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""
    
    class Meta:
        model = Vendedor
        fields = [
            'dpi',
            'nombre',
            'telefono',
            'nivel_exito',
        ]


class VendedorDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalle"""
    
    class Meta:
        model = Vendedor
        fields = [
            'dpi',
            'nombre',
            'correo_electronico',
            'telefono',
            'sueldo',
            'nivel_exito',
            'creado_en',
            'actualizado_en',
        ]
        read_only_fields = ['creado_en', 'actualizado_en', 'nivel_exito']


class VendedorCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar"""
    
    class Meta:
        model = Vendedor
        fields = [
            'dpi',
            'nombre',
            'correo_electronico',
            'telefono',
            'sueldo',
        ]
    
    def validate_dpi(self, value):
        """Validar que el DPI solo contenga dígitos"""
        if not value.isdigit():
            raise serializers.ValidationError("El DPI debe contener solo dígitos")
        if len(value) != 13:
            raise serializers.ValidationError("El DPI debe tener exactamente 13 dígitos")
        return value
    
    def validate_sueldo(self, value):
        """Validar que el sueldo sea positivo"""
        if value < 0:
            raise serializers.ValidationError("El sueldo debe ser mayor o igual a 0")
        return value