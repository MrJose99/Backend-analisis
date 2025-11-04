from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection
from .models import Ruta, RutaCliente, MetaVendedor
from .serializers import (
    RutaListSerializer, RutaDetailSerializer, RutaCreateSerializer,
    RutaClienteSerializer, RutaClienteCreateSerializer,
    MetaVendedorListSerializer, MetaVendedorDetailSerializer, 
    MetaVendedorCreateUpdateSerializer
)


class RutaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de rutas
    """
    queryset = Ruta.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dpi_vendedor', 'fecha']
    search_fields = ['dpi_vendedor__nombre']
    ordering_fields = ['fecha', 'tiempo_planificado_min', 'tiempo_real_min']
    ordering = ['-fecha']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RutaListSerializer
        elif self.action == 'create':
            return RutaCreateSerializer
        return RutaDetailSerializer
    
    def create(self, request, *args, **kwargs):
        """Crear ruta usando stored procedure"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Llamar al stored procedure
        with connection.cursor() as cursor:
            cursor.execute("""
                DECLARE @id_ruta INT;
                EXEC sistema.sp_crear_ruta 
                    @dpi_vendedor = %s,
                    @fecha = %s,
                    @kilometros_estimados = %s,
                    @id_ruta = @id_ruta OUTPUT;
                SELECT @id_ruta AS id_ruta;
            """, [
                serializer.validated_data['dpi_vendedor'].dpi,
                serializer.validated_data['fecha'],
                serializer.validated_data.get('kilometros_estimados')
            ])
            result = cursor.fetchone()
            id_ruta = result[0]
        
        # Obtener la ruta creada
        ruta = Ruta.objects.get(pk=id_ruta)
        output_serializer = RutaDetailSerializer(ruta)
        
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def asignar_cliente(self, request, pk=None):
        """Asignar un cliente a la ruta usando stored procedure"""
        ruta = self.get_object()
        serializer = RutaClienteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    EXEC sistema.sp_asignar_cliente_ruta 
                        @id_ruta = %s,
                        @nit_cliente = %s,
                        @orden_visita = %s,
                        @id_tiempo_cliente = %s;
                """, [
                    ruta.id_ruta,
                    serializer.validated_data['nit_cliente'].nit,
                    serializer.validated_data['orden_visita'],
                    serializer.validated_data['id_tiempo_cliente'].id_tiempo_cliente
                ])
            
            # Refrescar la ruta
            ruta.refresh_from_db()
            output_serializer = RutaDetailSerializer(ruta)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def clientes(self, request, pk=None):
        """Listar clientes de una ruta"""
        ruta = self.get_object()
        clientes = ruta.clientes.all()
        serializer = RutaClienteSerializer(clientes, many=True)
        return Response(serializer.data)


class MetaVendedorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de metas de vendedor
    """
    queryset = MetaVendedor.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dpi_vendedor', 'estado', 'id_periodo']
    search_fields = ['dpi_vendedor__nombre']
    ordering_fields = ['fecha_inicio', 'monto_meta', 'monto_logrado']
    ordering = ['-fecha_inicio']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MetaVendedorListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MetaVendedorCreateUpdateSerializer
        return MetaVendedorDetailSerializer
    
    def create(self, request, *args, **kwargs):
        """Crear meta usando stored procedure"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                DECLARE @id_meta INT;
                EXEC sistema.sp_crear_meta_vendedor 
                    @dpi_vendedor = %s,
                    @id_periodo = %s,
                    @fecha_inicio = %s,
                    @fecha_fin = %s,
                    @monto_meta = %s,
                    @peso_conversion = %s,
                    @peso_monto = %s,
                    @observaciones = %s,
                    @id_meta = @id_meta OUTPUT;
                SELECT @id_meta AS id_meta;
            """, [
                serializer.validated_data['dpi_vendedor'].dpi,
                serializer.validated_data['id_periodo'].id_periodo,
                serializer.validated_data['fecha_inicio'],
                serializer.validated_data['fecha_fin'],
                serializer.validated_data['monto_meta'],
                serializer.validated_data.get('peso_conversion', 60),
                serializer.validated_data.get('peso_monto', 40),
                serializer.validated_data.get('observaciones')
            ])
            result = cursor.fetchone()
            id_meta = result[0]
        
        meta = MetaVendedor.objects.get(pk=id_meta)
        output_serializer = MetaVendedorDetailSerializer(meta)
        
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Listar solo metas activas"""
        metas = self.queryset.filter(estado='ACTIVA')
        serializer = MetaVendedorListSerializer(metas, many=True)
        return Response(serializer.data)