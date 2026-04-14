from models.usuario_model import (
    obtener_usuarios,
    crear_usuario,
    eliminar_usuario
)

def get_usuarios():
    return obtener_usuarios() # "dame todos los usuario"

def add_usuario(username, password):
    return crear_usuario(username, password) # Crea un usuario con estos datos

def delete_usuario(id_usuario):
    return eliminar_usuario(id_usuario) # elimina un usuario por su ID