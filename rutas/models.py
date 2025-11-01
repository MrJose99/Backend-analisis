from django.db import models
from core.models import TimeStampedModel, TiempoCliente, ResultadoVisita, Periodo
from maestros.models import Vendedor, Cliente


class Ruta(TimeStampedModel):
    id_ruta = models.AutoField(primary_key=True, db_column='id_ruta')
    dpi_vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.PROTECT,
        db_column='dpi_vendedor',
        related_name='rutas'
    )
    fecha = models.DateField()
    kilometros_estimados = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        db_column='kilometros_estimados'
    )
    tiempo_planificado_min = models.IntegerField(
        null=True,
        blank=True,
        db_column='tiempo_planificado_min'
    )
    tiempo_real_min = models.IntegerField(null=True, blank=True, db_column='tiempo_real_min')
    resultado_global = models.CharField(max_length=50, null=True, blank=True, db_column='resultado_global')

    class Meta:
        db_table = 'sistema\".\"rutas'
        managed = False
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        ordering = ['-fecha']

    def __str__(self):
        return f"Ruta {self.id_ruta} - {self.dpi_vendedor.nombre} ({self.fecha})"


class RutaCliente(models.Model):
    id_ruta = models.ForeignKey(
        Ruta,
        on_delete=models.CASCADE,
        db_column='id_ruta',
        related_name='clientes'
    )
    nit_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        db_column='nit_cliente'
    )
    orden_visita = models.IntegerField(db_column='orden_visita')
    id_tiempo_cliente = models.ForeignKey(
        TiempoCliente,
        on_delete=models.PROTECT,
        db_column='id_tiempo_cliente',
        default=1
    )
    hora_inicio = models.DateTimeField(null=True, blank=True, db_column='hora_inicio')
    hora_fin = models.DateTimeField(null=True, blank=True, db_column='hora_fin')
    resultado_visita = models.ForeignKey(
        ResultadoVisita,
        on_delete=models.PROTECT,
        db_column='resultado_visita',
        default='PENDIENTE'
    )
    observaciones = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'sistema\".\"ruta_clientes'
        managed = False
        unique_together = ('id_ruta', 'nit_cliente')
        verbose_name = 'Cliente en Ruta'
        verbose_name_plural = 'Clientes en Ruta'
        ordering = ['id_ruta', 'orden_visita']

    def __str__(self):
        return f"Ruta {self.id_ruta_id} - Cliente {self.nit_cliente_id}"


class MetaVendedor(TimeStampedModel):
    id_meta = models.AutoField(primary_key=True, db_column='id_meta')
    dpi_vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.PROTECT,
        db_column='dpi_vendedor',
        related_name='metas'
    )
    id_periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT, db_column='id_periodo')
    fecha_inicio = models.DateField(db_column='fecha_inicio')
    fecha_fin = models.DateField(db_column='fecha_fin')
    monto_meta = models.DecimalField(max_digits=14, decimal_places=2, db_column='monto_meta')
    monto_logrado = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        db_column='monto_logrado'
    )
    peso_conversion = models.SmallIntegerField(default=60, db_column='peso_conversion')
    peso_monto = models.SmallIntegerField(default=40, db_column='peso_monto')
    estado = models.CharField(max_length=20, default='ACTIVA')
    observaciones = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'sistema\".\"metas_vendedor'
        managed = False
        verbose_name = 'Meta de Vendedor'
        verbose_name_plural = 'Metas de Vendedor'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"Meta {self.id_meta} - {self.dpi_vendedor.nombre}"