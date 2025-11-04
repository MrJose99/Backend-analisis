from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RutaViewSet, MetaVendedorViewSet

router = DefaultRouter()
router.register(r'rutas', RutaViewSet, basename='ruta')
router.register(r'metas', MetaVendedorViewSet, basename='meta')

urlpatterns = [
    path('', include(router.urls)),
]