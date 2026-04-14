# Sistema de Control de Rutas y Despachos — TransporteRápido S.A.S.

## Descripción
Sistema de escritorio desarrollado en Python con Tkinter y MySQL para gestionar vehículos, conductores, clientes, destinos y despachos de la empresa TransporteRápido S.A.S. Permite registrar y hacer seguimiento de cada envío, asignar conductores y vehículos, y generar reportes de operación.

## Módulos del sistema
- **Acceso al sistema** — Login con validación de usuario y contraseña
- **Gestión de Usuarios** — Crear y eliminar usuarios del sistema
- **Gestión de Vehículos** — CRUD completo con placa, tipo, capacidad y estado
- **Gestión de Conductores** — CRUD completo con licencia, estado activo/inactivo
- **Gestión de Clientes** — CRUD completo con razón social y datos de contacto
- **Gestión de Destinos** — CRUD completo de ciudades y zonas de entrega
- **Despachos** — Registro y seguimiento de despachos con validaciones de negocio
- **Consultas y Reportes** — Reportes con JOIN y filtros por estado, conductor y fechas

## Herramientas usadas
- Python 3.13
- Tkinter (interfaz gráfica)
- MySQL (base de datos)
- mysql-connector-python (conector)

## Arquitectura
MVC (Modelo - Vista - Controlador) implementado con funciones.

```
proyecto/
├── main.py
├── config/
│   └── db.py
├── models/
│   ├── usuario_model.py
│   ├── cliente_model.py
│   ├── vehiculo_model.py
│   ├── conductor_model.py
│   ├── destino_model.py
│   └── despacho_model.py
├── controllers/
│   ├── login_controller.py
│   ├── usuario_controller.py
│   ├── cliente_controller.py
│   ├── vehiculo_controller.py
│   ├── conductor_controller.py
│   ├── destino_controller.py
│   └── despacho_controller.py
└── views/
    ├── login_view.py
    ├── main_view.py
    ├── usuarios_view.py
    ├── clientes_view.py
    ├── vehiculos_view.py
    ├── conductores_view.py
    ├── destinos_view.py
    ├── despachos_view.py
    └── reportes_view.py
```

## Instalación y uso
1. Instalar dependencias:
```
pip install mysql-connector-python
```
2. Crear la base de datos ejecutando el archivo `database.sql` en MySQL
3. Configurar credenciales en `config/db.py`
4. Ejecutar el sistema:
```
python main.py
```

## Autor
**Luis Cortes**
SENA — Análisis y Desarrollo de Software
