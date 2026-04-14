# Manual de Uso — Sistema de Logística TransporteRápido S.A.S.

**Autor:** Luis Cortes  
**Institución:** SENA — Análisis y Desarrollo de Software

---

## 1. Módulo de Acceso al Sistema (Login)

Al ejecutar el sistema aparece una ventana de login.

- Ingrese su **usuario** y **contraseña**
- Presione el botón **Iniciar sesión** o la tecla **Enter**
- Si los datos son correctos, el sistema abre el menú principal
- Si son incorrectos, aparece un mensaje de error

> Usuario por defecto: `admin` | Contraseña: `1234`

---

## 2. Módulo de Gestión de Usuarios

Permite crear y eliminar usuarios del sistema.

- **Crear:** Ingrese username y password, presione **Crear**
- **Eliminar:** Ingrese el ID del usuario o haga clic en la tabla, presione **Eliminar**
- **Limpiar:** Limpia el formulario

> ⚠️ No se puede editar un usuario, solo crear o eliminar.

---

## 3. Módulo de Gestión de Vehículos

Permite registrar y administrar los vehículos de la empresa.

- **Campos:** Placa, Tipo, Capacidad (kg), Estado (propio/subcontratado)
- **Crear:** Complete los campos y presione **Guardar**
- **Editar:** Haga clic en un vehículo de la tabla, modifique los campos y presione **Guardar**
- **Eliminar:** Ingrese el ID o haga clic en la tabla, presione **Eliminar**

---

## 4. Módulo de Gestión de Conductores

Permite registrar y administrar los conductores.

- **Campos:** Nombre, Cédula, Teléfono, Licencia, Fecha vencimiento (YYYY-MM-DD), Estado (activo/inactivo)
- **Crear:** Complete los campos y presione **Guardar**
- **Editar:** Haga clic en un conductor de la tabla, modifique los campos y presione **Guardar**
- **Eliminar:** Ingrese el ID o haga clic en la tabla, presione **Eliminar**

> ⚠️ No se puede asignar un conductor con licencia vencida a un despacho.

---

## 5. Módulo de Gestión de Clientes

Permite registrar y administrar los clientes corporativos.

- **Campos:** Nombre (razón social), NIT, Teléfono, Dirección
- **Crear:** Complete los campos y presione **Guardar**
- **Editar:** Haga clic en un cliente de la tabla, modifique los campos y presione **Guardar**
- **Eliminar:** Ingrese el ID o haga clic en la tabla, presione **Eliminar**

---

## 6. Módulo de Gestión de Destinos

Permite registrar las ciudades y zonas de entrega.

- **Campos:** Ciudad, Dirección, Departamento
- **Crear:** Complete los campos y presione **Guardar**
- **Editar:** Haga clic en un destino de la tabla, modifique y presione **Guardar**
- **Eliminar:** Ingrese el ID o haga clic en la tabla, presione **Eliminar**

---

## 7. Módulo de Despachos

Permite registrar y gestionar los despachos de mercancía.

- **Campos:** Fecha (YYYY-MM-DD), Estado, Cliente, Conductor, Vehículo, Destino
- **Crear:** Seleccione todos los campos usando los Combobox y presione **Guardar**
- **Editar:** Haga clic en un despacho de la tabla, modifique y presione **Guardar**
- **Eliminar:** Ingrese el ID o haga clic en la tabla, presione **Eliminar**

### Reglas de negocio aplicadas:
| Regla | Mensaje |
|---|---|
| Vehículo ya en ruta | ❌ El vehículo ya tiene un despacho activo |
| Conductor ya en ruta | ❌ El conductor ya tiene un despacho activo |
| Licencia vencida | ❌ La licencia del conductor venció el... |
| Despacho entregado | ⚠️ Este despacho ya fue entregado y no puede modificarse |

---

## 8. Módulo de Consultas y Reportes

Permite visualizar reportes y filtrar despachos.

### Reportes disponibles:
- **Despachos por estado** — Muestra cuántos despachos hay en cada estado
- **Conductores activos** — Muestra cuántos despachos tiene cada conductor
- **Vehículos utilizados** — Muestra cuántos viajes ha hecho cada vehículo
- **Licencias vencidas** — Muestra conductores con licencia vencida

### Filtros disponibles:
- **Por estado** — Seleccione un estado del Combobox y presione **Filtrar por estado**
- **Por conductor** — Escriba el nombre y presione **Filtrar por conductor**
- **Por fechas** — Ingrese fecha inicio y fin (YYYY-MM-DD) y presione **Filtrar por fechas**

> Presione **← Volver** para regresar al menú de reportes.
