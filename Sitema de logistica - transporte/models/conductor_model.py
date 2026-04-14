from config.db import get_connection # abrea la conexion con mysql

def obtener_conductor(): # traemos todos los clientes de la base de datos
    conn = get_connection() # intenta conectarse

    if not conn:
        return[] # si falla devuelve una lista vacia
    cursor = None

    try: 
        cursor = conn.cursor() # Cursor ejecuta las consultas
        cursor.execute("SELECT * FROM conductor") # trae todos los datos de latabla conductor
        return cursor.fetchall() # lo devuelve en forma de lista

    except Exception as e:
        print(f"Error al obtener conductor: {e}")
        return[]

    finally:
        if cursor:
            cursor.close()
        conn.close()

def crear_conductor(nombre, cedula, telefono, licencia, fecha_vencimiento, estado): # para insertar nuevos conductores
    conn = get_connection()
    if not conn:
        return False
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conductor (nombre, cedula, telefono, licencia, fecha_vencimiento, estado) VALUES (%s, %s, %s, %s, %s, %s)", # inserta un nuevo conductor con esos datos
        (nombre, cedula, telefono, licencia, fecha_vencimiento, estado)) # pasamos los valores que van a llenar en esa casilla
        conn.commit() # es como presionar el boton de guardar, si no los datos no se guardan
        return True # sitodo sale bien devuleve True (El cliente se gurado)

    except Exception as e:
        print(f"Error al crear un conductor: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()

def actualizar_conductor(id_conductor,nombre, cedula, telefono, licencia, fecha_vencimiento, estado): # modifica un conductor existente
    # si no hay conexion falla
    conn = get_connection()
    if not conn:
        return False
    cursor = None

    try:
        cursor = conn.cursor() # ejecuta consultas
        # busca el cliente con ese id y cambiale los datos
        cursor.execute("UPDATE conductor SET nombre = %s, cedula = %s, telefono = %s, licencia = %s, fecha_vencimiento = %s, estado = %s WHERE id_conductor = %s",
        (nombre, cedula, telefono, licencia, fecha_vencimiento, estado, id_conductor))
        conn.commit() # para guardar
        return True

    except Exception as e:
        print(f"Error al actualizar conductor: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()


def eliminar_conductor(id_conductor): # recibe el ID que quieres eliminar
    conn = get_connection() #itenta abrir la conexion
    if not conn:
        return False ## si falla devuelve False
    cursor = None

    try:
        # crea un cursor para ejecutar en ese caso seria DELETE
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conductor WHERE id_conductor = %s", (id_conductor,))
        conn.commit()
       
        #nmero de filas afectadas
        # si es > 0 si elimino algo: True
        # si es = 0 ese  ID no existia: False
        return cursor.rowcount > 0  # devuelve el número de filas afectadas. Si el ID no existe,

    except Exception as e:
        # captura cualquier error y lo convierte en texto
        error_str = str(e)

        #no se puede eliminar si esta relacionado con otra tabla (despacho)
        #vueleve relacionado en vez de False
        if "1451" in str(e):
            return "RELACIONADO"

        print(f"Error al eliminar conductor: {e}")
        return False

    finally:
        if  cursor:
            cursor.close()
        conn.close()