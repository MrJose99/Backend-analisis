from core.models import *
from maestros.models import *
from rutas.models import *
from ventas.models import *
from usuarios.models import *

# ===================== CORE =====================
print('Cargando datos de core...')
estatus_credito = EstatusCredito.objects.create(estatus_credito='B', descripcion='Bueno')
estatus_credito2 = EstatusCredito.objects.create(estatus_credito='M', descripcion='Malo')
presentacion = Presentacion.objects.create(presentacion='CAJA', descripcion='Caja de 12')
presentacion2 = Presentacion.objects.create(presentacion='UNIDAD', descripcion='Unidad')
resultado_visita = ResultadoVisita.objects.create(resultado_visita='PENDIENTE', descripcion='Pendiente')
resultado_visita2 = ResultadoVisita.objects.create(resultado_visita='EXITOSA', descripcion='Exitosa')
tiempo_cliente = TiempoCliente.objects.create(id_tiempo_cliente=1, minutos=15, descripcion='Visita corta')
tiempo_cliente2 = TiempoCliente.objects.create(id_tiempo_cliente=2, minutos=30, descripcion='Visita larga')
periodo = Periodo.objects.create(id_periodo=1, descripcion='Enero 2025')
periodo2 = Periodo.objects.create(id_periodo=2, descripcion='Febrero 2025')
estado_usuario = EstadoUsuario.objects.create(estado_usuario='ACTIVO', descripcion='Usuario activo')
estado_usuario2 = EstadoUsuario.objects.create(estado_usuario='INACTIVO', descripcion='Usuario inactivo')
rol = Rol.objects.create(rol='ADMIN', descripcion='Administrador')
rol2 = Rol.objects.create(rol='VENDEDOR', descripcion='Vendedor')

# ===================== MAESTROS =====================
print('Cargando datos de maestros...')
cliente = Cliente.objects.create(nit='123456789', nombre='Cliente Demo', direccion='Zona 1', correo_electronico='cliente@demo.com', estatus_credito=estatus_credito)
cliente2 = Cliente.objects.create(nit='987654321', nombre='Cliente 2', direccion='Zona 2', correo_electronico='cliente2@demo.com', estatus_credito=estatus_credito2)
producto = Producto.objects.create(codigo='P001', descripcion='Producto 1', color='Rojo', precio_unitario=10.5, presentacion=presentacion)
producto2 = Producto.objects.create(codigo='P002', descripcion='Producto 2', color='Azul', precio_unitario=20.0, presentacion=presentacion2)
vendedor = Vendedor.objects.create(dpi='1234567890123', nombre='Juan Pérez', correo_electronico='juan@demo.com', telefono='5555-1111', sueldo=3500, nivel_exito=90)
vendedor2 = Vendedor.objects.create(dpi='3210987654321', nombre='Ana López', correo_electronico='ana@demo.com', telefono='5555-2222', sueldo=4000, nivel_exito=80)

# ===================== RUTAS =====================
print('Cargando datos de rutas...')
ruta = Ruta.objects.create(dpi_vendedor=vendedor, fecha='2025-11-01', kilometros_estimados=12.5)
ruta2 = Ruta.objects.create(dpi_vendedor=vendedor2, fecha='2025-11-02', kilometros_estimados=15.0)
ruta_cliente = RutaCliente.objects.create(id_ruta=ruta, nit_cliente=cliente, orden_visita=1, id_tiempo_cliente=tiempo_cliente, resultado_visita=resultado_visita)
ruta_cliente2 = RutaCliente.objects.create(id_ruta=ruta2, nit_cliente=cliente2, orden_visita=1, id_tiempo_cliente=tiempo_cliente2, resultado_visita=resultado_visita2)
meta = MetaVendedor.objects.create(dpi_vendedor=vendedor, id_periodo=periodo, fecha_inicio='2025-11-01', fecha_fin='2025-11-30', monto_meta=10000, monto_logrado=5000, observaciones='Meta parcial')
meta2 = MetaVendedor.objects.create(dpi_vendedor=vendedor2, id_periodo=periodo2, fecha_inicio='2025-11-01', fecha_fin='2025-11-28', monto_meta=8000, monto_logrado=8000, observaciones='Meta cumplida')

# ===================== VENTAS =====================
print('Cargando datos de ventas...')
venta = Venta.objects.create(fecha='2025-11-01T10:00:00Z', nit_cliente=cliente, id_ruta=ruta, total=100)
venta2 = Venta.objects.create(fecha='2025-11-02T11:00:00Z', nit_cliente=cliente2, id_ruta=ruta2, total=200)
detalle = DetalleVenta.objects.create(id_venta=venta, linea=1, codigo_producto=producto, cantidad=2, precio_unitario=10.5)
detalle2 = DetalleVenta.objects.create(id_venta=venta2, linea=1, codigo_producto=producto2, cantidad=5, precio_unitario=20.0)
cobro = Cobro.objects.create(nit_cliente=cliente, id_venta=venta, fecha='2025-11-02T10:00:00Z', monto=100)
cobro2 = Cobro.objects.create(nit_cliente=cliente2, id_venta=venta2, fecha='2025-11-03T10:00:00Z', monto=200)

# ===================== USUARIOS =====================
print('Cargando datos de usuarios...')
usuario = Usuario.objects.create(usuario='admin', contrasena_hash=b'hash', contrasena_salt=b'salt', ultimo_ingreso=None)
usuario2 = Usuario.objects.create(usuario='vendedor', contrasena_hash=b'hash2', contrasena_salt=b'salt2', ultimo_ingreso=None)
admin = Administrador.objects.create(dpi='1234567890123', nombre='Admin', correo_electronico='admin@demo.com', id_usuario=usuario)
usuario_estado = UsuarioEstado.objects.create(id_usuario=usuario, estado_usuario=estado_usuario, observaciones='Activo')
usuario_estado2 = UsuarioEstado.objects.create(id_usuario=usuario2, estado_usuario=estado_usuario2, observaciones='Inactivo')
usuario_rol = UsuarioRol.objects.create(id_usuario=usuario, rol=rol)
usuario_rol2 = UsuarioRol.objects.create(id_usuario=usuario2, rol=rol2)

print('Carga inicial completada.')
