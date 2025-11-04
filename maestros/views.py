from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cliente, Producto, Vendedor
from .serializers import (
    ClienteListSerializer, ClienteDetailSerializer, ClienteCreateUpdateSerializer,
    ProductoListSerializer, ProductoDetailSerializer, ProductoCreateUpdateSerializer,
    VendedorListSerializer, VendedorDetailSerializer, VendedorCreateUpdateSerializer
)


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de clientes
    
    list: Listar todos los clientes
    retrieve: Obtener detalle de un cliente
    create: Crear nuevo cliente
    update: Actualizar cliente completo
    partial_update: Actualizar campos específicos
    destroy: Eliminar cliente
    """
    queryset = Cliente.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estatus_credito']
    search_fields = ['nit', 'nombre', 'correo_electronico']
    ordering_fields = ['nombre', 'estatus_credito', 'creado_en']
    ordering = ['nombre']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ClienteCreateUpdateSerializer
        return ClienteDetailSerializer
    
    @action(detail=False, methods=['get'])
    def por_estatus(self, request):
        """Endpoint personalizado: Agrupar clientes por estatus de crédito"""
        from django.db.models import Count
        resultado = Cliente.objects.values('estatus_credito').annotate(
            total=Count('nit')
        ).order_by('-total')
        return Response(resultado)


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de productos
    """
    queryset = Producto.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['presentacion']
    search_fields = ['codigo', 'descripcion', 'color']
    ordering_fields = ['descripcion', 'precio_unitario', 'creado_en']
    ordering = ['descripcion']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductoCreateUpdateSerializer
        return ProductoDetailSerializer
    
    @action(detail=False, methods=['get'])
    def mas_caros(self, request):
        """Endpoint personalizado: Top 10 productos más caros"""
        productos = Producto.objects.order_by('-precio_unitario')[:10]
        serializer = ProductoListSerializer(productos, many=True)
        return Response(serializer.data)


class VendedorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de vendedores
    """
    queryset = Vendedor.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['dpi', 'nombre', 'correo_electronico', 'telefono']
    ordering_fields = ['nombre', 'sueldo', 'nivel_exito', 'creado_en']
    ordering = ['nombre']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VendedorListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return VendedorCreateUpdateSerializer
        return VendedorDetailSerializer
    
    @action(detail=False, methods=['get'])
    def top_nivel_exito(self, request):
        """Endpoint personalizado: Top vendedores por nivel de éxito"""
        vendedores = Vendedor.objects.filter(
            nivel_exito__isnull=False
        ).order_by('-nivel_exito')[:10]
        serializer = VendedorListSerializer(vendedores, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def rutas(self, request, pk=None):
        """Obtener todas las rutas de un vendedor"""
        vendedor = self.get_object()
        rutas = vendedor.rutas.all()
        from rutas.serializers import RutaListSerializer
        serializer = RutaListSerializer(rutas, many=True)
        return Response(serializer.data)
