from django.db import models
from core.models import TimeStampedModel, EstadoUsuario, Rol


class Usuario(TimeStampedModel):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    usuario = models.CharField(max_length=80, unique=True)
    contrasena_hash = models.BinaryField(db_column='contrasena_hash')
    contrasena_salt = models.BinaryField(db_column='contrasena_salt')
    ultimo_ingreso = models.DateTimeField(null=True, blank=True, db_column='ultimo_ingreso')

    class Meta:

        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.usuario


class Administrador(TimeStampedModel):
    dpi = models.CharField(max_length=13, primary_key=True, db_column='dpi')
    nombre = models.CharField(max_length=150)
    correo_electronico = models.EmailField(max_length=150, null=True, blank=True, db_column='correo_electronico')
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='administrador'
    )

    class Meta:

        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

    def __str__(self):
        return self.nombre


class UsuarioEstado(models.Model):
    id_usuario_estado = models.AutoField(primary_key=True, db_column='id_usuario_estado')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    estado_usuario = models.ForeignKey(EstadoUsuario, on_delete=models.PROTECT, db_column='estado_usuario')
    fecha_inicio = models.DateTimeField(auto_now_add=True, db_column='fecha_inicio')
    fecha_fin = models.DateTimeField(null=True, blank=True, db_column='fecha_fin')
    observaciones = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Estado de Usuario'
        verbose_name_plural = 'Estados de Usuario'


class UsuarioRol(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column='rol')
    asignado_en = models.DateTimeField(auto_now_add=True, db_column='asignado_en')

    class Meta:
        unique_together = ('id_usuario', 'rol')
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuario'
