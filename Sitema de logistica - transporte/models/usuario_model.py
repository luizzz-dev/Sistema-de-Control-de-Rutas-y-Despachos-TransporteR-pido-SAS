from config.db import get_connection # abre la conexion con mysql

def validar_usuario(username, password):
    conn = get_connection() # intenta conectarse
    if not conn:
        return None # si falla devuelve una lista vacia
    cursor = None
    try:
        cursor = conn.cursor() # cursor ejecutar las consultas
        #busca un usuario que coincida con:
        #username sin importar mayus o minus y los mismo con el password
        sql = "SELECT username FROM usuario WHERE LOWER(username) = %s AND password = %s"
        
        #ejecuta la consulta y trae una sola fila
        cursor.execute(sql, (username.lower(), password))
        resultado = cursor.fetchone()
        
        # “Si el usuario y contraseña coinciden, déjalo entrar; si no, recházalo”
        if resultado:
            return resultado[0]  # ← devuelve el username
        return None              # ← None si no existe
    
    except Exception as e:
        print(f"Error al validar usuario: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        conn.close()

def obtener_usuarios():
    conn = get_connection()
    if not conn:
        return []
    cursor = None
    try:
        cursor = conn.cursor()
        # trae todos los usuario y devuelvemos en una lista (dame todos los usuarios registrado)
        cursor.execute("SELECT id_usuario, username FROM usuario")
        return cursor.fetchall()
    
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    
    finally:
        if cursor:
            cursor.close()
        conn.close()

def crear_usuario(username, password):
    conn = get_connection()
    if not conn:
        return False
    cursor = None
    try:
        cursor = conn.cursor()

        # inserta un nuevo usuario en la base de datos
        sql = "INSERT INTO usuario (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (username, password))
        conn.commit() # guarda el cambio
        return True # si sale bien True, si falla False
    
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        conn.close()

def eliminar_usuario(id_usuario): #recibe el ID que quieres eliminar
    conn = get_connection()
    if not conn:
        return False
    cursor = None
    
    try:
        # intenta eliminar el usuario por su ID
        cursor = conn.cursor()
        sql = "DELETE FROM usuario WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        conn.commit()

        # si elimino algo: True
        # si no existia: False
        return cursor.rowcount > 0  # devuelve el número de filas afectadas. Si el ID no existe,
    
    except Exception as e:
        error_str = str(e)

        # ERROR DE CLAVE FORÁNEA
        # No puedes eliminar porque ese usuario está siendo usado en otra tabla
        if "1451" in error_str:
            return "RELACIONADO"

        print(f"Error al eliminar usuario: {e}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        conn.close()