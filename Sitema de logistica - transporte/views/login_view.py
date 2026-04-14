import tkinter as tk
from tkinter import messagebox
from controllers.login_controller import validar_usuario

def crear_login():
    # Crea la ventana principal
    ventana = tk.Tk()
    ventana.title("Login - Sistema de Logística")
    ventana.geometry("500x300")

    # Campos de entrada para usuario y contraseña
    # show="*" oculta los caracteres de la contraseña
    entry_user = tk.Entry(ventana)
    entry_pass = tk.Entry(ventana, show="*")

    def iniciar_sesion():
        # Obtiene y limpia los valores ingresados
        # .strip() elimina espacios en blanco al inicio y al final
        # .lower() convierte el usuario a minúsculas
        username = entry_user.get().strip().lower()
        password = entry_pass.get().strip()

        # Valida que ningún campo esté vacío
        if username == "" or password == "":
            messagebox.showerror("Error", "Por favor ingrese ambos campos")
            return

        # Llama al controlador para validar las credenciales
        resultado = validar_usuario(username, password)

        if resultado:
            # Si las credenciales son correctas, muestra bienvenida,
            # cierra el login y abre la ventana principal
            messagebox.showinfo("Éxito", f"Bienvenido, {username}")
            ventana.destroy()
            abrir_ventana_principal(resultado)
        else:
            # Si las credenciales son incorrectas, muestra un error
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def abrir_ventana_principal(username):
        # Importación local para evitar importaciones circulares
        from views.main_view import crear_ventana_principal
        crear_ventana_principal(username) 

    # Etiqueta y campo de entrada para el usuario
    tk.Label(ventana, text="Usuario:").pack(pady=20)
    entry_user.pack()

    # Etiqueta y campo de entrada para la contraseña
    tk.Label(ventana, text="Contraseña:").pack(pady=10)
    entry_pass.pack()

    # Al presionar Enter en usuario, el foco salta al campo de contraseña
    entry_user.bind("<Return>", lambda e: entry_pass.focus())
    
    # Al presionar Enter en contraseña, se ejecuta el login directamente
    entry_pass.bind("<Return>", lambda e: iniciar_sesion())

    # El cursor inicia en el campo de usuario al abrir la ventana
    entry_user.focus()

    # Botón que ejecuta la función de login al hacer clic
    tk.Button(ventana, text="Iniciar sesión", command=iniciar_sesion).pack(pady=15)

    # La ventana permanece abierta hasta que el usuario la cierre
    ventana.mainloop()