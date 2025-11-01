from django.db import models
from core.models import TimeStampedModel
from maestros.models import Cliente, Producto
from rutas.models import Ruta


class Venta(TimeStampedModel):
    id_venta = models.AutoField(primary_key=True, db_column='id_venta')
    fecha = models.DateTimeField()
    nit_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        db_column='nit_cliente',
        related_name='ventas'
    )
    id_ruta = models.ForeignKey(
        Ruta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_ruta',
        related_name='ventas'
    )
    total = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = 'sistema\".\"ventas'
        managed = False
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha']

    def __str__(self):
        return f"Venta {self.id_venta} - Q{self.total}"


class DetalleVenta(models.Model):
    id_venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        db_column='id_venta',
        related_name='detalles'
    )
    linea = models.IntegerField()
    codigo_producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        db_column='codigo_producto'
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, db_column='precio_unitario')

    class Meta:
        db_table = 'sistema\".\"detalle_venta'
        managed = False
        unique_together = ('id_venta', 'linea')
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'

    def __str__(self):
        return f"Detalle {self.linea} - Venta {self.id_venta_id}"


class Cobro(TimeStampedModel):
    id_cobro = models.AutoField(primary_key=True, db_column='id_cobro')
    nit_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        db_column='nit_cliente',
        related_name='cobros'
    )
    id_venta = models.ForeignKey(
        Venta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_venta',
        related_name='cobros'
    )
    fecha = models.DateTimeField()
    monto = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = 'sistema\".\"cobros'
        managed = False
        verbose_name = 'Cobro'
        verbose_name_plural = 'Cobros'
        ordering = ['-fecha']

    def __str__(self):
        return f"Cobro {self.id_cobro} - Q{self.monto}"