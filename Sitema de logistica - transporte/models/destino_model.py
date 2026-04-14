from config.db import get_connection # abre la conexion con mysql

def obtener_destinos(): #vamos a trare todos los destinos de la base de datos
    conn = get_connection() # inetnta conectarse
    if not conn:
        return []   # si falla devuelve una lista vacia
    cursor = None
    
    try:
        cursor = conn.cursor() # cursor ejecutas las consultas
        cursor.execute("SELECT * FROM destino") # trae todo los datos de la tabla destino
        return cursor.fetchall() #fetchall lo devuelve en forma de lista

    except Exception as e:
        print(f"Error al obtener destinos: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        conn.close()

def crear_destino(ciudad, direccion, departamento): # para insertar nuevos destinos
    conn = get_connection()
    if not conn:
        return False
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO destino (ciudad, direccion, departamento) VALUES (%s, %s, %s)", # inserta un nuevi cliente con esos datos 
        (ciudad, direccion, departamento)) # pasamos los valores que van a llenar en esa casilla
        conn.commit()  # es como presionar el boton de guardar, si no los datos no se guradan
        return True # si todo sale bien devuleve True (El destino se gurado)

    except Exception as e:
        print(f"Error al crear destino: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()

def actualizar_destino(id_destino, ciudad, direccion, departamento): # modifaca un destino existente
    # si no hay conexion falla
    conn = get_connection()
    if not conn:
        return False
    cursor = None

    try:
        cursor = conn.cursor() # ejecuta consultas

         # busca el cliente con ese id y cambiale los datos
        cursor.execute("UPDATE destino SET ciudad = %s, direccion = %s, departamento = %s WHERE id_destino = %s", 
        (ciudad, direccion, departamento, id_destino))
        conn.commit()  # para guardar
        return True

    except Exception as e:
        print(f"Error al actualizar destino: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()

def eliminar_destino(id_destino):   # recibe el ID que quieres eliminar
    conn = get_connection()  #itenta abrir la conexion
    if not conn:
        return False    # si falla devuelve False
    cursor = None

    try:
        # crea un cursor para ejecutar en ese caso seria DELETE
        cursor = conn.cursor()
        cursor.execute("DELETE FROM destino WHERE id_destino = %s", (id_destino,))
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

        print(f"Error al eliminar destino: {e}")
        return False

    finally:
        # cierra cursor y conexion
        if cursor:
            cursor.close()
        conn.close()