from rest_framework import serializers
from .models import Venta, DetalleVenta, Cobro
from maestros.serializers import ClienteListSerializer, ProductoListSerializer


class DetalleVentaSerializer(serializers.ModelSerializer):
    """Serializer para detalles de venta"""
    producto_info = ProductoListSerializer(source='codigo_producto', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = DetalleVenta
        fields = [
            'linea',
            'codigo_producto',
            'producto_info',
            'cantidad',
            'precio_unitario',
            'subtotal',
        ]
    
    def get_subtotal(self, obj):
        return obj.cantidad * obj.precio_unitario


class DetalleVentaCreateSerializer(serializers.Serializer):
    """Serializer para crear detalles (sin ID de venta)"""
    codigo_producto = serializers.CharField(max_length=30)
    cantidad = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)


class VentaListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""
    cliente_nombre = serializers.CharField(source='nit_cliente.nombre', read_only=True)
    
    class Meta:
        model = Venta
        fields = [
            'id_venta',
            'fecha',
            'nit_cliente',
            'cliente_nombre',
            'total',
        ]


class VentaDetailSerializer(serializers.ModelSerializer):
    """Serializer completo con detalles"""
    cliente_info = ClienteListSerializer(source='nit_cliente', read_only=True)
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venta
        fields = [
            'id_venta',
            'fecha',
            'nit_cliente',
            'cliente_info',
            'id_ruta',
            'total',
            'detalles',
            'creado_en',
            'actualizado_en',
        ]
        read_only_fields = ['total', 'creado_en', 'actualizado_en']


class VentaCreateSerializer(serializers.Serializer):
    """Serializer para crear venta con stored procedure"""
    fecha = serializers.DateTimeField()
    nit_cliente = serializers.CharField(max_length=9)
    id_ruta = serializers.IntegerField(required=False, allow_null=True)
    detalles = DetalleVentaCreateSerializer(many=True)
    
    def validate_detalles(self, value):
        if not value:
            raise serializers.ValidationError("Debe incluir al menos un detalle de venta")
        return value


class CobroListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""
    cliente_nombre = serializers.CharField(source='nit_cliente.nombre', read_only=True)
    
    class Meta:
        model = Cobro
        fields = [
            'id_cobro',
            'fecha',
            'nit_cliente',
            'cliente_nombre',
            'monto',
        ]


class CobroDetailSerializer(serializers.ModelSerializer):
    """Serializer completo"""
    cliente_info = ClienteListSerializer(source='nit_cliente', read_only=True)
    
    class Meta:
        model = Cobro
        fields = [
            'id_cobro',
            'fecha',
            'nit_cliente',
            'cliente_info',
            'id_venta',
            'monto',
            'creado_en',
            'actualizado_en',
        ]
        read_only_fields = ['creado_en', 'actualizado_en']


class CobroCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar"""
    
    class Meta:
        model = Cobro
        fields = [
            'fecha',
            'nit_cliente',
            'id_venta',
            'monto',
        ]
    
    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a 0")
        return value