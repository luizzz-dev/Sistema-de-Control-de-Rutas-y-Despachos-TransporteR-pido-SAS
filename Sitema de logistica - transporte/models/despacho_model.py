from config.db import get_connection # abre la conexion con mysql

def obtener_despachos(): #vamos a trare todos los depachos de la base de datos
    conn = get_connection() # intenta conectarse
    if not conn:
        return []   # si flla devuelve una lista vacia
    cursor = None
    try:
        cursor = conn.cursor()  # cursor ejecutas las consultas 
        cursor.execute("""
            SELECT d.id_despacho, d.fecha, d.estado,
                   c.nombre, co.nombre, v.placa, de.ciudad
            FROM despacho d
            LEFT JOIN cliente   c  ON d.id_cliente   = c.id_cliente
            LEFT JOIN conductor co ON d.id_conductor = co.id_conductor
            LEFT JOIN vehiculo  v  ON d.id_vehiculo  = v.id_vehiculo
            LEFT JOIN destino   de ON d.id_destino   = de.id_destino
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener despachos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conn.close()

def crear_despacho(id_cliente, id_conductor, id_vehiculo, id_destino, fecha, estado): # para insertar nuevos despachos
    conn = get_connection()
    if not conn:
        return False
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO despacho (id_cliente, id_conductor, id_vehiculo, id_destino, fecha, estado)
            VALUES (%s, %s, %s, %s, %s, %s) """, # inserta un nuevo despacho con esos datos
        (id_cliente, id_conductor, id_vehiculo, id_destino, fecha, estado))  # pasamos los valores que van a llenar en esa casilla
        conn.commit() # es como presionar el boton de guardar, si no los datos no se guradan
        return True # sitodo sale bien devuleve True (El despacho se gurado)
    
    except Exception as e:
        print(f"Error al crear un despacho: {e}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        conn.close()

def actualizar_despacho(id_despacho, id_cliente, id_conductor, id_vehiculo, id_destino, fecha, estado): # modificar un despacho existente
    # si no hay conexion falla
    conn = get_connection()
    if not conn:
        return False
    cursor = None
    try:
        cursor = conn.cursor() # ejecutar consultaa
        
        # busca el cliente con ese id y cambiale los datos
        cursor.execute("""
            UPDATE despacho
            SET id_cliente = %s, id_conductor = %s, id_vehiculo = %s, id_destino = %s, fecha = %s, estado = %s
            WHERE id_despacho = %s
        """, (id_cliente, id_conductor, id_vehiculo, id_destino, fecha, estado, id_despacho))
        conn.commit() # para guardar
        return True
    
    except Exception as e:
        print(f"Error al actualizar despacho: {e}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        conn.close()    

def eliminar_despacho(id_despacho): # recibe el ID que quieres eliminar
    conn = get_connection()  #itenta abrir la conexion
    if not conn:
        return False    # si falla devuelve False
    cursor = None
    
    try:
        # crea un cursor para ejecutar en ese caso seria DELETE
        cursor = conn.cursor()
        cursor.execute("DELETE FROM despacho WHERE id_despacho = %s", (id_despacho,))
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

        print(f"Error al eliminar despacho: {e}")
        return False
    
    finally:
        # cierra cursor y conexion
        if cursor:
            cursor.close()
        conn.close()