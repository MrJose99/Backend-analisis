# Endpoints principales de la API Ruteros

## Maestros
- **Clientes**
  - `GET    /api/maestros/clientes/`           → Listar clientes
  - `POST   /api/maestros/clientes/`           → Crear cliente
  - `GET    /api/maestros/clientes/{nit}/`     → Detalle cliente
  - `PUT    /api/maestros/clientes/{nit}/`     → Actualizar cliente
  - `PATCH  /api/maestros/clientes/{nit}/`     → Actualizar parcial
  - `DELETE /api/maestros/clientes/{nit}/`     → Eliminar cliente
  - `GET    /api/maestros/clientes/por_estatus/` → Agrupados por estatus

- **Productos**
  - `GET    /api/maestros/productos/`           → Listar productos
  - `POST   /api/maestros/productos/`           → Crear producto
  - `GET    /api/maestros/productos/{codigo}/`  → Detalle producto
  - `PUT    /api/maestros/productos/{codigo}/`  → Actualizar producto
  - `PATCH  /api/maestros/productos/{codigo}/`  → Actualizar parcial
  - `DELETE /api/maestros/productos/{codigo}/`  → Eliminar producto
  - `GET    /api/maestros/productos/mas_caros/` → Top 10 más caros

- **Vendedores**
  - `GET    /api/maestros/vendedores/`           → Listar vendedores
  - `POST   /api/maestros/vendedores/`           → Crear vendedor
  - `GET    /api/maestros/vendedores/{dpi}/`     → Detalle vendedor
  - `PUT    /api/maestros/vendedores/{dpi}/`     → Actualizar vendedor
  - `PATCH  /api/maestros/vendedores/{dpi}/`     → Actualizar parcial
  - `DELETE /api/maestros/vendedores/{dpi}/`     → Eliminar vendedor
  - `GET    /api/maestros/vendedores/{dpi}/rutas/` → Rutas del vendedor
  - `GET    /api/maestros/vendedores/top_nivel_exito/` → Top por nivel de éxito

## Rutas
- **Rutas**
  - `GET    /api/rutas/rutas/`                   → Listar rutas
  - `POST   /api/rutas/rutas/`                   → Crear ruta
  - `GET    /api/rutas/rutas/{id_ruta}/`         → Detalle ruta
  - `PUT    /api/rutas/rutas/{id_ruta}/`         → Actualizar ruta
  - `PATCH  /api/rutas/rutas/{id_ruta}/`         → Actualizar parcial
  - `DELETE /api/rutas/rutas/{id_ruta}/`         → Eliminar ruta
  - `POST   /api/rutas/rutas/{id_ruta}/asignar_cliente/` → Asignar cliente a ruta
  - `GET    /api/rutas/rutas/{id_ruta}/clientes/`        → Listar clientes de ruta

- **Metas de Vendedor**
  - `GET    /api/rutas/metas/`                   → Listar metas
  - `POST   /api/rutas/metas/`                   → Crear meta
  - `GET    /api/rutas/metas/{id_meta}/`         → Detalle meta
  - `PUT    /api/rutas/metas/{id_meta}/`         → Actualizar meta
  - `PATCH  /api/rutas/metas/{id_meta}/`         → Actualizar parcial
  - `DELETE /api/rutas/metas/{id_meta}/`         → Eliminar meta
  - `GET    /api/rutas/metas/activas/`           → Listar solo metas activas

## Ventas
- **Ventas**
  - `GET    /api/ventas/ventas/`                 → Listar ventas
  - `POST   /api/ventas/ventas/`                 → Crear venta
  - `GET    /api/ventas/ventas/{id_venta}/`      → Detalle venta
  - `PUT    /api/ventas/ventas/{id_venta}/`      → Actualizar venta
  - `PATCH  /api/ventas/ventas/{id_venta}/`      → Actualizar parcial
  - `DELETE /api/ventas/ventas/{id_venta}/`      → Eliminar venta
  - `GET    /api/ventas/ventas/por_cliente/`     → Ventas agrupadas por cliente
  - `GET    /api/ventas/ventas/por_vendedor/`    → Ventas agrupadas por vendedor
  - `GET    /api/ventas/ventas/resumen_periodo/?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD` → Resumen por periodo

- **Cobros**
  - `GET    /api/ventas/cobros/`                 → Listar cobros
  - `POST   /api/ventas/cobros/`                 → Crear cobro
  - `GET    /api/ventas/cobros/{id_cobro}/`      → Detalle cobro
  - `PUT    /api/ventas/cobros/{id_cobro}/`      → Actualizar cobro
  - `PATCH  /api/ventas/cobros/{id_cobro}/`      → Actualizar parcial
  - `DELETE /api/ventas/cobros/{id_cobro}/`      → Eliminar cobro
  - `GET    /api/ventas/cobros/por_cliente/`     → Cobros agrupados por cliente
  - `GET    /api/ventas/cobros/resumen_periodo/?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD` → Resumen por periodo

## Usuarios
- **No hay endpoints REST para usuarios personalizados en este proyecto (solo admin y modelos).**

## Documentación interactiva
- Swagger:   `/api/docs/`
- Redoc:     `/api/redoc/`
- Esquema:   `/api/schema/`

---

**Notas:**
- Todos los endpoints aceptan y devuelven JSON.
- Para crear registros, usa los endpoints `POST` con los campos requeridos según el modelo.
- Para autenticación y pruebas, puedes usar `/api-auth/login/` (si tienes usuarios Django activos).
