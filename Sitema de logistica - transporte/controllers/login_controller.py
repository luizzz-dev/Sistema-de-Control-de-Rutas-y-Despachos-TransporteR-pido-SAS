from models.usuario_model import validar_usuario as validar_usuario_model # para evitar confucion con la que creamos abajo

#
def validar_usuario(username, password):
    return validar_usuario_model(username, password)
            
        #Recibe usuario y contraseña desde la interfaz (login)
        #Llama al modelo
        #Devuelve el resultado

        #Traducción directa:
        #“Valida este usuario en la base de datos”