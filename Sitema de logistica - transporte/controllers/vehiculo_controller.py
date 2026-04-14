from models.vehiculo_model import (
    obtener_vehiculos, #consulta todos
    crear_vehiculo, # inserta uno nuevo
    actualizar_vehiculo,  #edita uno existente  
    eliminar_vehiculo #elimina
)

def get_vehiculos():
    return obtener_vehiculos() # "Taeme todo los vehiculos"

def add_vehiculo(placa, tipo, capacidad, estado):
    return crear_vehiculo(placa, tipo, capacidad, estado) #crea un vehiculo con estos datos

def update_vehiculo(id_vehiculo, placa, tipo, capacidad, estado):
    return actualizar_vehiculo(id_vehiculo, placa, tipo, capacidad, estado) # Acrualiza es vehiculo por su ID

def delete_vehiculo(id_vehiculo):
    return eliminar_vehiculo(id_vehiculo) # elimina este vehiculo por su ID