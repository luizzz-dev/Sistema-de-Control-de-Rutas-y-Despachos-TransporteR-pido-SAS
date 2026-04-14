# intermediario entre la interfaz (lo que le usuario ve) y la base de datos
#El cliente (la interfaz) hace el pedido
#El mesero (este archivo) lo recibe
#La cocina (el cliente_model) lo prepara
#El mesero devuelve el resultado


from models.destino_model import (
    obtener_destinos,
    crear_destino,
    actualizar_destino,    
    eliminar_destino
)

def get_destinos():
    return obtener_destinos() # "dame todos los destinos"

def add_destino(ciudad, direccion, departamento):
    return crear_destino(ciudad, direccion, departamento) # crea este destino con estos datos

def update_destino(id_destino, ciudad, direccion, departamento):
    return actualizar_destino(id_destino, ciudad, direccion, departamento) # actualiza este vehiculo con base a su ID

def delete_destino(id_destino):
    return eliminar_destino(id_destino) #elimina un destino por su ID