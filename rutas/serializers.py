from rest_framework import serializers
from .models import Ruta, RutaCliente, MetaVendedor
from maestros.serializers import VendedorListSerializer, ClienteListSerializer
from core.models import TiempoCliente, ResultadoVisita, Periodo


class TiempoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiempoCliente
        fields = ['id_tiempo_cliente', 'minutos', 'descripcion']


class ResultadoVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoVisita
        fields = ['resultado_visita', 'descripcion']


class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id_periodo', 'descripcion']


class RutaClienteSerializer(serializers.ModelSerializer):
    """Serializer para clientes dentro de una ruta"""
    cliente_info = ClienteListSerializer(source='nit_cliente', read_only=True)
    tiempo_cliente_info = TiempoClienteSerializer(source='id_tiempo_cliente', read_only=True)
    resultado_visita_info = ResultadoVisitaSerializer(source='resultado_visita', read_only=True)
    
    class Meta:
        model = RutaCliente
        fields = [
            'nit_cliente',
            'cliente_info',
            'orden_visita',
            'id_tiempo_cliente',
            'tiempo_cliente_info',
            'hora_inicio',
            'hora_fin',
            'resultado_visita',
            'resultado_visita_info',
            'observaciones',
        ]


class RutaClienteCreateSerializer(serializers.ModelSerializer):
    """Serializer para asignar cliente a ruta"""
    
    class Meta:
        model = RutaCliente
        fields = [
            'nit_cliente',
            'orden_visita',
            'id_tiempo_cliente',
        ]


class RutaListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""
    vendedor_nombre = serializers.CharField(source='dpi_vendedor.nombre', read_only=True)
    total_clientes = serializers.SerializerMethodField()
    
    class Meta:
        model = Ruta
        fields = [
            'id_ruta',
            'dpi_vendedor',
            'vendedor_nombre',
            'fecha',
            'kilometros_estimados',
            'tiempo_planificado_min',
            'tiempo_real_min',
            'total_clientes',
        ]
    
    def get_total_clientes(self, obj):
        return obj.clientes.count()


class RutaDetailSerializer(serializers.ModelSerializer):
    """Serializer completo con clientes"""
    vendedor_info = VendedorListSerializer(source='dpi_vendedor', read_only=True)
    clientes = RutaClienteSerializer(many=True, read_only=True)
    
    class Meta:
        model = Ruta
        fields = [
            'id_ruta',
            'dpi_vendedor',
            'vendedor_info',
            'fecha',
            'kilometros_estimados',
            'tiempo_planificado_min',
            'tiempo_real_min',
            'resultado_global',
            'clientes',
            'creado_en',
            'actualizado_en',
        ]
        read_only_fields = ['tiempo_planificado_min', 'creado_en', 'actualizado_en']


class RutaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear ruta"""
    
    class Meta:
        model = Ruta
        fields = [
            'dpi_vendedor',
            'fecha',
            'kilometros_estimados',
        ]
    
    def validate_kilometros_estimados(self, value):
        if value and value < 0:
            raise serializers.ValidationError("Los kilómetros deben ser mayor o igual a 0")
        return value


class MetaVendedorListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""
    vendedor_nombre = serializers.CharField(source='dpi_vendedor.nombre', read_only=True)
    periodo_descripcion = serializers.CharField(source='id_periodo.descripcion', read_only=True)
    porcentaje_cumplimiento = serializers.SerializerMethodField()
    
    class Meta:
        model = MetaVendedor
        fields = [
            'id_meta',
            'dpi_vendedor',
            'vendedor_nombre',
            'id_periodo',
            'periodo_descripcion',
            'fecha_inicio',
            'fecha_fin',
            'monto_meta',
            'monto_logrado',
            'porcentaje_cumplimiento',
            'estado',
        ]
    
    def get_porcentaje_cumplimiento(self, obj):
        if obj.monto_meta == 0:
            return 0
        return round((obj.monto_logrado * 100) / obj.monto_meta, 2)


class MetaVendedorDetailSerializer(serializers.ModelSerializer):
    """Serializer completo"""
    vendedor_info = VendedorListSerializer(source='dpi_vendedor', read_only=True)
    periodo_info = PeriodoSerializer(source='id_periodo', read_only=True)
    porcentaje_cumplimiento = serializers.SerializerMethodField()
    diferencia = serializers.SerializerMethodField()
    
    class Meta:
        model = MetaVendedor
        fields = [
            'id_meta',
            'dpi_vendedor',
            'vendedor_info',
            'id_periodo',
            'periodo_info',
            'fecha_inicio',
            'fecha_fin',
            'monto_meta',
            'monto_logrado',
            'porcentaje_cumplimiento',
            'diferencia',
            'peso_conversion',
            'peso_monto',
            'estado',
            'observaciones',
            'creado_en',
            'actualizado_en',
        ]
        read_only_fields = ['monto_logrado', 'creado_en', 'actualizado_en']
    
    def get_porcentaje_cumplimiento(self, obj):
        if obj.monto_meta == 0:
            return 0
        return round((obj.monto_logrado * 100) / obj.monto_meta, 2)
    
    def get_diferencia(self, obj):
        return obj.monto_meta - obj.monto_logrado


class MetaVendedorCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar"""
    
    class Meta:
        model = MetaVendedor
        fields = [
            'dpi_vendedor',
            'id_periodo',
            'fecha_inicio',
            'fecha_fin',
            'monto_meta',
            'peso_conversion',
            'peso_monto',
            'observaciones',
        ]
    
    def validate(self, data):
        """Validar pesos y fechas"""
        peso_conversion = data.get('peso_conversion', 60)
        peso_monto = data.get('peso_monto', 40)
        
        if peso_conversion + peso_monto != 100:
            raise serializers.ValidationError(
                "La suma de peso_conversion y peso_monto debe ser 100"
            )
        
        if data['fecha_inicio'] > data['fecha_fin']:
            raise serializers.ValidationError(
                "La fecha de inicio debe ser menor o igual a la fecha fin"
            )
        
        return data