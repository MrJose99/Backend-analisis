from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VentaViewSet, CobroViewSet

router = DefaultRouter()
router.register(r'ventas', VentaViewSet, basename='venta')
router.register(r'cobros', CobroViewSet, basename='cobro')

urlpatterns = [
    path('', include(router.urls)),
]