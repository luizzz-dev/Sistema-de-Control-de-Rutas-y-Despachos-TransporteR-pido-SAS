from config.db import get_connection  # Función que abre la conexión con MySQL


# 📋 OBTENER TODOS LOS VEHÍCULOS
def obtener_vehiculos():
    conn = get_connection()  # Intenta conectarse a la BD
    
    if not conn:
        return []  # Si falla la conexión, devuelve lista vacía
    
    cursor = None  # Inicializa el cursor
    
    try:
        cursor = conn.cursor()  # Crea el cursor para ejecutar SQL
        cursor.execute("SELECT * FROM vehiculo")  # Consulta todos los registros
        return cursor.fetchall()  # Devuelve todos los resultados

    except Exception as e:
        print(f"Error al obtener vehículos: {e}")  # Muestra el error en consola
        return []  # Devuelve lista vacía si falla

    finally:
        if cursor:
            cursor.close()  # Cierra el cursor
        conn.close()  # Cierra la conexión


# ➕ CREAR VEHÍCULO
def crear_vehiculo(placa, tipo, capacidad, estado):
    conn = get_connection()
    
    if not conn:
        return False  # Si no hay conexión, falla
    
    cursor = None

    try:
        cursor = conn.cursor()
        
        # Inserta un nuevo vehículo en la tabla
        cursor.execute(
            "INSERT INTO vehiculo (placa, tipo, capacidad, estado) VALUES (%s, %s, %s, %s)", 
            (placa, tipo, capacidad, estado)
        )
        
        conn.commit()  # Guarda los cambios en la BD
        return True  # Indica que se creó correctamente

    except Exception as e:
        print(f"Error al crear vehículo: {e}")
        return False  # Indica que falló

    finally:
        if cursor:
            cursor.close()
        conn.close()


# ✏️ ACTUALIZAR VEHÍCULO
def actualizar_vehiculo(id_vehiculo, placa, tipo, capacidad, estado):
    conn = get_connection()
    
    if not conn:
        return False
    
    cursor = None

    try:
        cursor = conn.cursor()
        
        # Actualiza los datos del vehículo según su ID
        cursor.execute(
            "UPDATE vehiculo SET placa = %s, tipo = %s, capacidad = %s, estado = %s WHERE id_vehiculo = %s", 
            (placa, tipo, capacidad, estado, id_vehiculo)
        )
        
        conn.commit()  # Guarda cambios
        return True  # Indica éxito

    except Exception as e:
        print(f"Error al actualizar vehículo: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()



def eliminar_vehiculo(id_vehiculo): #recibe le ID que quieres eliminar
    conn = get_connection()
    
    if not conn:
        return False
    cursor = None

    try:
        cursor = conn.cursor()
        # Elimina el vehículo por ID
        cursor.execute("DELETE FROM vehiculo WHERE id_vehiculo = %s", (id_vehiculo,))
        conn.commit()  # Guarda cambios
        
        # rowcount indica cuántas filas se afectaron
        return cursor.rowcount > 0  # True si eliminó, False si no existía

    except Exception as e:
        error_str = str(e)
        
        #restricción de clave foránea (está siendo usado en otra tabla)
        if "1451" in str(e):
            return "RELACIONADO"

        print(f"Error al eliminar vehículo: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()