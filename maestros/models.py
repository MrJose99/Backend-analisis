from django.db import models
from core.models import TimeStampedModel, EstatusCredito, Presentacion


class Cliente(TimeStampedModel):
    nit = models.CharField(max_length=9, primary_key=True, db_column='nit')
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250, null=True, blank=True)
    correo_electronico = models.EmailField(max_length=150, null=True, blank=True, db_column='correo_electronico')
    estatus_credito = models.ForeignKey(
        EstatusCredito,
        on_delete=models.PROTECT,
        db_column='estatus_credito',
        default='B'
    )

    class Meta:
        db_table = 'sistema\".\"clientes'
        managed = False
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nit} - {self.nombre}"


class Producto(TimeStampedModel):
    codigo = models.CharField(max_length=30, primary_key=True, db_column='codigo')
    descripcion = models.CharField(max_length=200)
    color = models.CharField(max_length=50, null=True, blank=True)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, db_column='precio_unitario')
    presentacion = models.ForeignKey(
        Presentacion,
        on_delete=models.PROTECT,
        db_column='presentacion'
    )

    class Meta:
        db_table = 'sistema\".\"productos'
        managed = False
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['descripcion']

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class Vendedor(TimeStampedModel):
    dpi = models.CharField(max_length=13, primary_key=True, db_column='dpi')
    nombre = models.CharField(max_length=150)
    correo_electronico = models.EmailField(max_length=150, null=True, blank=True, db_column='correo_electronico')
    telefono = models.CharField(max_length=30, null=True, blank=True)
    sueldo = models.DecimalField(max_digits=12, decimal_places=2)
    nivel_exito = models.SmallIntegerField(null=True, blank=True, db_column='nivel_exito')

    class Meta:
        db_table = 'sistema\".\"vendedores'
        managed = False
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.dpi} - {self.nombre}"