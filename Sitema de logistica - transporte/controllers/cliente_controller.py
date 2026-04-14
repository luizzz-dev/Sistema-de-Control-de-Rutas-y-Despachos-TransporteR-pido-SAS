# intermediario entre la interfaz (lo que le usuario ve) y la base de datos
#El cliente (la interfaz) hace el pedido
#El mesero (este archivo) lo recibe
#La cocina (el cliente_model) lo prepara
#El mesero devuelve el resultado


from models.cliente_model import (
    obtener_clientes,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente
)

def get_clientes():
    return obtener_clientes() # "dame todos los clientes"

def add_cliente(nombre, nit, telefono, direccion):
    return crear_cliente(nombre, nit, telefono, direccion) # crea este cliente con estos datos

def update_cliente(id_cliente, nombre, nit, telefono, direccion):
    return actualizar_cliente(id_cliente, nombre, nit, telefono, direccion) #modifica este cliente con este ID usando estos nuevos datos

def delete_cliente(id_cliente):
    return eliminar_cliente(id_cliente) #elimina un clinete por su ID