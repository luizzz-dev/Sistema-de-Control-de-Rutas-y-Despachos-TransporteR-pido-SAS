from config.db import get_connection # abre la conexion con mysql

def obtener_clientes(): #vamos a trare todos lo clientes de la base de datos
    conn = get_connection() # intenta conectarse 
    if not conn:
        return []           # si flla devuelve una lista vacia
    cursor = None
    
    try:
        cursor = conn.cursor() # cursor ejecutas las consultas 
        cursor.execute("SELECT * FROM cliente") # trae todo los datos de la tabla cliente
        return cursor.fetchall() #fetchall lo devuelve en forma de lista

    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        conn.close()


def crear_cliente(nombre, nit, telefono, direccion): #para insertar nuevos cliente
    conn = get_connection()
    if not conn:
        return False
    cursor = None

    try:
        cursor = conn.cursor()  
        cursor.execute("INSERT INTO cliente (nombre, nit, telefono, direccion) VALUES (%s, %s, %s, %s)", # inserta un nuevi cliente con esos datos 
        (nombre, nit, telefono, direccion))     # pasamos los valores que van a llenar en esa casilla
        conn.commit() # es como presionar el boton de guardar, si no los datos no se guradan
        return True # si todo sale bien devuleve True (El cliente se gurado)

    except Exception as e:
        print(f"Error al crear cliente: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()

def actualizar_cliente(id_cliente, nombre, nit, telefono, direccion): # modificar un cliente existente
    # si no hay conexion falla
    conn = get_connection()
    if not conn:
        return False
    cursor = None

    try:
        cursor = conn.cursor() # ejecutar consultas
        
        # busca el cliente con ese id y cambiale los datos
        cursor.execute("UPDATE cliente SET nombre = %s, nit = %s, telefono = %s, direccion = %s WHERE id_cliente = %s", 
        (nombre, nit, telefono, direccion, id_cliente))
        conn.commit() # para guardar
        return True

    except Exception as e:
        print(f"Error al actualizar cliente: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        conn.close()

def eliminar_cliente(id_cliente): # recibe el ID que quieres eliminar
    conn = get_connection() #itenta abrir la conexion
    if not conn:
        return False # si falla devuelve False
    cursor = None   

    try:
        # crea un cursor para ejecutar en ese caso seria DELETE
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        
        #nmero de filas afectadas
        # si es > 0 si elimino algo: True
        # si es = 0 ese  ID no existia: False
        return cursor.rowcount > 0  #

    except Exception as e:
        # captura cualquier error y lo convierte en texto
        error_str = str(e)

        # ERROR DE CLAVE FORÁNEA
        #no se puede eliminar si esta relacionado con otra tabla (despacho)
        #vueleve relacionado en vez de False
        if "1451" in error_str:
            return "RELACIONADO"

        print(f"Error al eliminar cliente: {e}")
        return False

    finally:
        #cierra curso y conexion
        if cursor:
            cursor.close()
        conn.close()
