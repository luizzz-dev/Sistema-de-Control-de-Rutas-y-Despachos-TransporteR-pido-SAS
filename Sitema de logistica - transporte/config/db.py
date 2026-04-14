import mysql.connector #permite a py hablar con mysql
from mysql.connector import Error # acptura erroe si algo flla al conectarse 

def get_connection():
    try: #intentar hacer esto
        return mysql.connector.connect( #intenta crear ela conexion
            host = 'localhost', # la bse de datos esta en el mismo computador
            user = "root", # usuario de mysql
            password = "Sena2025*", #contraseña de ella
            database = "transporte_rapido" # la base de datos que voy a usar
        ) #si todo sale bien devuelve la conexion
    except Error as e:                                # si algo falla (usuario o contraseña)
        print(f"Error al conectar a MySQL: {e}")      # captura el error e imprime el mensaje
        return None                                   # devuleve "None" (no hay conexion)