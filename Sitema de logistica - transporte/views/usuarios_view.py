import tkinter as tk
from tkinter import ttk, messagebox
# Importa las funciones del controlador que manejan la lógica de base de datos
from controllers.usuario_controller import (
    get_usuarios,
    add_usuario,
    delete_usuario
)

def vista_usuarios(frame):
    tk.Label(frame, text="Módulo de Usuarios", font=("Arial", 16, "bold")).pack(pady=10)

    # TABLA DE USUARIOS 
    # Muestra ID y Username de todos los usuarios registrados
    tabla = ttk.Treeview(frame, columns=("ID", "Username"), show="headings", height=10)
    tabla.heading("ID", text="ID")
    tabla.heading("Username", text="Username")
    tabla.column("ID", width=100)
    tabla.column("Username", width=200)
    tabla.pack(pady=10)

    # FORMULARIO
    form = tk.Frame(frame)
    form.pack(pady=10)

    # Etiquetas de los campos del formulario
    tk.Label(form, text="Username").grid(row=0, column=0, padx=5)
    tk.Label(form, text="Password").grid(row=0, column=1, padx=5)
    tk.Label(form, text="ID para eliminar").grid(row=0, column=2, padx=(30, 5))

    entry_user = tk.Entry(form, width=15)
    entry_pass = tk.Entry(form, width=15, show="*")  # show="*" oculta la contraseña

    # VALIDACIÓN: solo permite números en el campo ID 
    # La función retorna True si el valor es dígito o está vacío
    def solo_numeros(valor):
        return valor.isdigit() or valor == ""

    # vcmd registra la función de validación en tkinter
    # '%P' representa el valor que tendría el campo si se acepta el carácter
    vcmd = (frame.register(solo_numeros), '%P')

    # El campo ID usa validate="key" para validar en cada pulsación de tecla
    entry_id = tk.Entry(form, width=10, validate="key", validatecommand=vcmd)

    entry_user.grid(row=1, column=0, padx=5)
    entry_pass.grid(row=1, column=1, padx=5)
    entry_id.grid(row=1, column=2, padx=(30, 5))

    id_seleccionado = {"valor": None} #Guarda el ID del usuario seleccionado en la tabla(saber si se esta editando o creando)


    def cargar_tabla():
        # Limpia todas las filas actuales de la tabla
        for fila in tabla.get_children():
            tabla.delete(fila)
       
        # trae lo clientes de la base de datos y los inserta
        for usuario in get_usuarios():
            tabla.insert("", "end", values=usuario)


    # cuando hago clic: tomar los datos de esa fila y cargarlos en los campos del formulario 
    # para poder editarlos o verlos.
    def seleccionar(event):
        # Obtiene la fila actualmente seleccionada en la tabla
        fila = tabla.focus()
        if not fila:
            return
        
        valores = tabla.item(fila, "values") # obtiene los datos de la fila (usuario y contraseña)

        # Guarda el ID de la fila seleccionada
        id_seleccionado["valor"] = valores[0]

        # Autocompleta los campos del formulario con los datos de la fila
        entry_user.delete(0, "end")
        entry_user.insert(0, valores[1])

        entry_id.delete(0, "end")  # primero limpia el campo
        entry_id.insert(0, valores[0]) # luego debe inserta el valor que corresponde

    def limpiar():
        # Vacía todos los campos del formulario y resetea el ID seleccionado
        entry_user.delete(0, "end")
        entry_pass.delete(0, "end")
        entry_id.delete(0, "end")
        id_seleccionado["valor"] = None

    def guardar():
        #lee los valores del formulario
        username = entry_user.get().strip()
        password = entry_pass.get().strip()

        # Valida que ningún campo esté vacío
        if username == "" or password == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Llama al controlador para insertar el nuevo usuario
        ok = add_usuario(username, password)
        # Muestra mensaje según si la operación fue exitosa o falló (ej: username duplicado)
        messagebox.showinfo("Info", "Usuario creado" if ok else "Error (¿username duplicado?)")
        limpiar()
        cargar_tabla()

    def eliminar():
        id = entry_id.get()

        # Verifica que el campo ID tenga un número válido
        if not id.isdigit():
            messagebox.showerror("Error", "Ingrese un ID válido para eliminar")
            return

        # Pide confirmación antes de eliminar
        if messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            ok = delete_usuario(int(id))
            
            if ok:
                # Eliminación exitosa
                messagebox.showinfo("Info", "Usuario eliminado correctamente")

            elif ok == "RELACIONADO":
                # El usuario tiene registros asociados en otras tablas (integridad referencial)
                messagebox.showwarning(
                    "No permitido",
                    "No se puede eliminar este usuario porque tiene registros asociados"
                )

            else:
                # El ID no existe en la base de datos
                messagebox.showwarning("Advertencia", "El ID no existe")

            limpiar()
            cargar_tabla()

    # ATAJOS DE TECLADO
    tabla.bind("<<TreeviewSelect>>", seleccionar)       # Clic en tabla → autocompleta formulario
    entry_user.bind("<Return>", lambda e: entry_pass.focus())  # Enter en usuario → salta a contraseña
    entry_pass.bind("<Return>", lambda e: guardar())           # Enter en contraseña → guarda
    entry_id.bind("<Return>", lambda e: eliminar())            # Enter en ID → elimina
    entry_user.focus()  # El cursor inicia en el campo username

    # BOTONES DE ACCIÓN 
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Guardar",  command=guardar,  bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Eliminar", command=eliminar, bg="#f44336", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Limpiar",  command=limpiar,  bg="#2196F3", fg="white", width=12).grid(row=0, column=2, padx=5)

    # Carga los datos iniciales al abrir el módulo
    cargar_tabla()