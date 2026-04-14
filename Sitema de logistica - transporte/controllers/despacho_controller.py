# intermediario entre la interfaz (lo que le usuario ve) y la base de datos
#El cliente (la interfaz) hace el pedido
#El mesero (este archivo) lo recibe
#La cocina (el cliente_model) lo prepara
#El mesero devuelve el resultado


from models.despacho_model import (
    obtener_despachos,
    crear_despacho,
    actualizar_despacho,
    eliminar_despacho
)

def get_despachos():
    return obtener_despachos()  #pasa todos los despachos

def add_despacho(id_cliente, id_conductor, id_vehiculo, id_destino, fecha, estado):
    return crear_despacho(id_cliente, id_conductor, id_vehiculo, id_destino, fecha, estado) #crea un nuevo depacho con estos datos

def update_despacho(id_despacho, id_cliente, id_conductor, id_vehiculo, id_destino, fecha, estado):
    return actualizar_despacho(id_despacho, id_cliente, id_conductor, id_vehiculo, id_destino, fecha, estado) # modifica este despacho con este ID usando estos nuevos datos

def delete_despacho(id_despacho):
    return eliminar_despacho(id_despacho) # elimina este despacho por su ID