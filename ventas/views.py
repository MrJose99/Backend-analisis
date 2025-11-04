from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection
import json
from .models import Venta, DetalleVenta, Cobro
from .serializers import (
    VentaListSerializer, VentaDetailSerializer, VentaCreateSerializer,
    CobroListSerializer, CobroDetailSerializer, CobroCreateUpdateSerializer
)


class VentaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de ventas
    """
    queryset = Venta.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nit_cliente', 'id_ruta']
    search_fields = ['nit_cliente__nombre']
    ordering_fields = ['fecha', 'total']
    ordering = ['-fecha']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VentaListSerializer
        elif self.action == 'create':
            return VentaCreateSerializer
        return VentaDetailSerializer
    
    def create(self, request, *args, **kwargs):
        """Crear venta usando stored procedure"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Preparar JSON de detalles
        detalles = serializer.validated_data['detalles']
        detalles_json = json.dumps([
            {
                'codigo': d['codigo_producto'],
                'cantidad': d['cantidad'],
                'precio': str(d['precio_unitario'])
            }
            for d in detalles
        ])
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    DECLARE @id_venta INT;
                    EXEC sistema.sp_registrar_venta 
                        @fecha = %s,
                        @nit_cliente = %s,
                        @id_ruta = %s,
                        @detalles_json = %s,
                        @id_venta = @id_venta OUTPUT;
                    SELECT @id_venta AS id_venta;
                """, [
                    serializer.validated_data['fecha'],
                    serializer.validated_data['nit_cliente'],
                    serializer.validated_data.get('id_ruta'),
                    detalles_json
                ])
                result = cursor.fetchone()
                id_venta = result[0]
            
            # Obtener la venta creada
            venta = Venta.objects.get(pk=id_venta)
            output_serializer = VentaDetailSerializer(venta)
            
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Error al registrar venta: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def por_cliente(self, request):
        """Ventas agrupadas por cliente"""
        from django.db.models import Sum, Count
        resultado = Venta.objects.values(
            'nit_cliente',
            'nit_cliente__nombre'
        ).annotate(
            total_ventas=Count('id_venta'),
            monto_total=Sum('total')
        ).order_by('-monto_total')[:20]
        
        return Response(resultado)
    
    @action(detail=False, methods=['get'])
    def por_vendedor(self, request):
        """Ventas agrupadas por vendedor"""
        from django.db.models import Sum, Count
        resultado = Venta.objects.filter(
            id_ruta__isnull=False
        ).values(
            'id_ruta__dpi_vendedor',
            'id_ruta__dpi_vendedor__nombre'
        ).annotate(
            total_ventas=Count('id_venta'),
            monto_total=Sum('total')
        ).order_by('-monto_total')[:20]
        
        return Response(resultado)
    
    @action(detail=False, methods=['get'])
    def resumen_periodo(self, request):
        """Resumen de ventas por período"""
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return Response(
                {'error': 'Debe proporcionar fecha_inicio y fecha_fin'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.db.models import Sum, Count, Avg
        ventas = Venta.objects.filter(
            fecha__date__gte=fecha_inicio,
            fecha__date__lte=fecha_fin
        )
        
        resumen = ventas.aggregate(
            total_ventas=Count('id_venta'),
            monto_total=Sum('total'),
            monto_promedio=Avg('total')
        )
        
        return Response(resumen)


class CobroViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de cobros
    """
    queryset = Cobro.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nit_cliente', 'id_venta']
    search_fields = ['nit_cliente__nombre']
    ordering_fields = ['fecha', 'monto']
    ordering = ['-fecha']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CobroListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CobroCreateUpdateSerializer
        return CobroDetailSerializer
    
    @action(detail=False, methods=['get'])
    def por_cliente(self, request):
        """Cobros agrupados por cliente"""
        from django.db.models import Sum, Count
        resultado = Cobro.objects.values(
            'nit_cliente',
            'nit_cliente__nombre'
        ).annotate(
            total_cobros=Count('id_cobro'),
            monto_total=Sum('monto')
        ).order_by('-monto_total')[:20]
        
        return Response(resultado)
    
    @action(detail=False, methods=['get'])
    def resumen_periodo(self, request):
        """Resumen de cobros por período"""
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return Response(
                {'error': 'Debe proporcionar fecha_inicio y fecha_fin'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.db.models import Sum, Count, Avg
        cobros = Cobro.objects.filter(
            fecha__date__gte=fecha_inicio,
            fecha__date__lte=fecha_fin
        )
        
        resumen = cobros.aggregate(
            total_cobros=Count('id_cobro'),
            monto_total=Sum('monto'),
            monto_promedio=Avg('monto')
        )
        
        return Response(resumen)
