from django.db import models


class TimeStampedModel(models.Model):
    """Modelo abstracto base para timestamps"""
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creado_en')
    actualizado_en = models.DateTimeField(auto_now=True, db_column='actualizado_en')

    class Meta:
        abstract = True


# ============================================
# CATÁLOGOS
# ============================================

class EstatusCredito(models.Model):
    estatus_credito = models.CharField(max_length=2, primary_key=True, db_column='estatus_credito')
    descripcion = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        verbose_name = 'Estatus de Crédito'
        verbose_name_plural = 'Estatus de Crédito'

    def __str__(self):
        return f"{self.estatus_credito} - {self.descripcion}"


class Presentacion(models.Model):
    presentacion = models.CharField(max_length=15, primary_key=True, db_column='presentacion')
    descripcion = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        verbose_name = 'Presentación'
        verbose_name_plural = 'Presentaciones'

    def __str__(self):
        return self.presentacion


class ResultadoVisita(models.Model):
    resultado_visita = models.CharField(max_length=20, primary_key=True, db_column='resultado_visita')
    descripcion = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        verbose_name = 'Resultado de Visita'
        verbose_name_plural = 'Resultados de Visita'

    def __str__(self):
        return self.descripcion or self.resultado_visita


class TiempoCliente(models.Model):
    id_tiempo_cliente = models.SmallIntegerField(primary_key=True, db_column='id_tiempo_cliente')
    minutos = models.IntegerField()
    descripcion = models.CharField(max_length=50)

    class Meta:

        verbose_name = 'Tiempo de Cliente'
        verbose_name_plural = 'Tiempos de Cliente'

    def __str__(self):
        return self.descripcion


class Periodo(models.Model):
    id_periodo = models.SmallIntegerField(primary_key=True, db_column='id_periodo')
    descripcion = models.CharField(max_length=50)

    class Meta:

        verbose_name = 'Período'
        verbose_name_plural = 'Períodos'

    def __str__(self):
        return self.descripcion


class EstadoUsuario(models.Model):
    estado_usuario = models.CharField(max_length=20, primary_key=True, db_column='estado_usuario')
    descripcion = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        verbose_name = 'Estado de Usuario'
        verbose_name_plural = 'Estados de Usuario'

    def __str__(self):
        return self.descripcion or self.estado_usuario


class Rol(models.Model):
    rol = models.CharField(max_length=40, primary_key=True, db_column='rol')
    descripcion = models.CharField(max_length=200, null=True, blank=True)

    class Meta:

        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.descripcion or self.rol
