# intermediario entre la interfaz (lo que le usuario ve) y la base de datos
#El cliente (la interfaz) hace el pedido
#El mesero (este archivo) lo recibe
#La cocina (el cliente_model) lo prepara
#El mesero devuelve el resultado


from models.conductor_model import (
    obtener_conductor,
    crear_conductor,
    actualizar_conductor,    
    eliminar_conductor
)

def get_conductores():
    return obtener_conductor() #pasa todos los conductores

def add_conductor(nombre, cedula, telefono, licencia, fecha_vencimiento, estado):
    return crear_conductor(nombre, cedula, telefono, licencia, fecha_vencimiento, estado) # crea un conductor con estos datos

def update_conductor(id_conductor,nombre, cedula, telefono, licencia, fecha_vencimiento, estado):
    return actualizar_conductor(id_conductor,nombre, cedula, telefono, licencia, fecha_vencimiento, estado) # modifica este cliente con este ID usando nuevos datos

def delete_conductor(id_conductor):
    return eliminar_conductor(id_conductor) # eliminamos un cliente por su ID

    