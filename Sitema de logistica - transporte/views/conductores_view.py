import tkinter as tk
from tkinter import ttk, messagebox  # widgtes comm tablas y ventanas de alerta
from controllers.conductor_controller import (
    get_conductores,
    add_conductor,
    update_conductor,
    delete_conductor
)

def vista_conductores(frame):
    # Título del módulo
    tk.Label(frame, text="Módulo de Conductores", font=("Arial", 16, "bold")).pack(pady=10)

    # VALIDACIÓN — solo permite escribir números en los campos que la usen
    def solo_numeros(texto):
        return texto.isdigit() or texto == ""  # acepta dígitos o campo vacío

    # Registra la validación para poder usarla en los Entry
    vcmd = (frame.register(solo_numeros), '%P')  # conecta la validacion con los inputs

    # BUSCADOR 
    buscar_frame = tk.Frame(frame)
    buscar_frame.pack(pady=5)

    tk.Label(buscar_frame, text="Buscar por nombre:").grid(row=0, column=0, padx=5)
    entry_buscar = tk.Entry(buscar_frame, width=20)
    entry_buscar.grid(row=0, column=1, padx=5)

    # Botón que ejecuta la búsqueda
    tk.Button(buscar_frame, text="Buscar", command=lambda: buscar(),
            bg="#607D8B", fg="white", width=10).grid(row=0, column=2, padx=5)

    # Botón que limpia el buscador y recarga todos los conductores
    tk.Button(buscar_frame, text="Limpiar", command=lambda: [
        entry_buscar.delete(0, "end"), cargar_tabla()
    ], bg="#9E9E9E", fg="white", width=10).grid(row=0, column=3, padx=5)

    def buscar():
        texto = entry_buscar.get().strip()  # lee lo que escribió el usuario
        if texto == "":
            cargar_tabla()  # si está vacío, muestra todos
            return
        
        for fila in tabla.get_children():
            tabla.delete(fila)  # borra la tabla actual
        
        for conductor in get_conductores():
            # conductor[1] es el nombre — filtra los que contienen el texto
            if texto.lower() in str(conductor[1]).lower(): # busca coincidencias en el nombre sin importa mayusculas
                tabla.insert("", "end", values=conductor) # si el texto esta dentro del nombre que lo muestre( an: juan, ana, andres)

    # TABLA 
    # Treeview con 7 columnas — muestra todos los conductores
    tabla = ttk.Treeview(frame, columns=("ID", "Nombre", "Cedula", "Telefono", "Licencia", "Fecha_vencimiento", "Estado"), show="headings", height=8)
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Cedula", text="Cedula")
    tabla.heading("Telefono", text="Telefono")
    tabla.heading("Licencia", text="Licencia")
    tabla.heading("Fecha_vencimiento", text="Fecha vencimiento")
    tabla.heading("Estado", text="Estado")
    tabla.pack(pady=10)

    # FORMULARIO 
    form = tk.Frame(frame)
    form.pack(pady=10)

    # Etiquetas de cada campo
    tk.Label(form, text="Nombre").grid(row=0, column=0)
    tk.Label(form, text="Cedula").grid(row=0, column=1)
    tk.Label(form, text="Telefono").grid(row=0, column=2)
    tk.Label(form, text="Licencia").grid(row=0, column=3)
    tk.Label(form, text="Fecha \n(YYYY-MM-DD)").grid(row=0, column=4)
    tk.Label(form, text="Estado").grid(row=0, column=5)
    tk.Label(form, text="ID para \neliminar").grid(row=0, column=6, padx=(30, 5))

    # Campos de texto — cédula y teléfono solo aceptan números
    entry_nombre = tk.Entry(form, width=15)
    entry_cedula = tk.Entry(form, width=15, validate="key", validatecommand=vcmd)  # solo números
    entry_telefono = tk.Entry(form, width=15, validate="key", validatecommand=vcmd)  # solo números
    entry_licencia = tk.Entry(form, width=15)
    entry_fecha_vencimiento = tk.Entry(form, width=15)
    entry_id = tk.Entry(form, width=10, validate="key", validatecommand=vcmd)  # solo números

    # Combobox para estado — solo permite "activo" o "inactivo"
    combo_estado = ttk.Combobox(form, values=["activo", "inactivo"], width=10, state="readonly")
    combo_estado.current(0)  # selecciona "activo" por defecto

    # Ubica cada campo en su columna
    entry_nombre.grid(row=1, column=0)
    entry_cedula.grid(row=1, column=1)
    entry_telefono.grid(row=1, column=2)
    entry_licencia.grid(row=1, column=3)
    entry_fecha_vencimiento.grid(row=1, column=4)
    combo_estado.grid(row=1, column=5)
    entry_id.grid(row=1, column=6, padx=(30, 5))

    # Guarda el ID del conductor seleccionado en la tabla
    id_seleccionado = {"valor": None}

    # FUNCIONES 

    def cargar_tabla():
        # limpia la tabla
        for fila in tabla.get_children():
            tabla.delete(fila)
        
        # trae lo conductores de la base de datos y los inserta
        for conductor in get_conductores():
            tabla.insert("", "end", values=conductor)

    # cuando hago clic: tomar los datos de esa fila y cargarlos en los campos del formulario 
    # para poder editarlos o verlos
    def seleccionar(event):
        # Cuando el usuario hace clic en una fila, llena el formulario con esos datos
        fila = tabla.focus()
        if not fila:
            return
        
        valores = tabla.item(fila, "values") # obtiene los datos de la fila (id, nombre, nit, telefono, direccion)
        id_seleccionado["valor"] = valores[0]  # guarda el ID

        # Llena cada campo con el valor correspondiente de la fila
        entry_nombre.delete(0, "end");            
        entry_nombre.insert(0, valores[1])
        
        entry_cedula.delete(0, "end");             # primero limpia el campo
        entry_cedula.insert(0, valores[2])         # luego inserta el valor que corresponde
        
        entry_telefono.delete(0, "end");          
        entry_telefono.insert(0, valores[3])
        
        entry_licencia.delete(0, "end");          
        entry_licencia.insert(0, valores[4])
        
        entry_fecha_vencimiento.delete(0, "end"); 
        entry_fecha_vencimiento.insert(0, valores[5])
       
        combo_estado.set(valores[6])              # selecciona el estado en el combobox
        
        entry_id.delete(0, "end");                
        entry_id.insert(0, valores[0])

    def limpiar():
        # Borra todos los campos del formulario y olvida el conductor seleccionado
        entry_nombre.delete(0, "end")
        entry_cedula.delete(0, "end")
        entry_telefono.delete(0, "end")
        entry_licencia.delete(0, "end")
        entry_fecha_vencimiento.delete(0, "end")
        combo_estado.current(0)  # vuelve a "activo"
        entry_id.delete(0, "end")
        
        id_seleccionado["valor"] = None #Guarda el ID del cliente seleccionado en la tabla(saber si se esta editando o creando)

    def guardar():
        # Lee los valores del formulario
        nombre = entry_nombre.get()
        cedula  = entry_cedula.get()
        telefono = entry_telefono.get()
        licencia = entry_licencia.get()
        fecha_vencimiento = entry_fecha_vencimiento.get()
        estado = combo_estado.get()

        # El nombre es obligatorio
        if nombre == "":
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        # Si hay un conductor seleccionado → actualiza, si no → crea uno nuevo
        # si hay un ID lo estoy editando
        # si no hay un ID lo estoy creando 
        if id_seleccionado["valor"]:
            ok = update_conductor(id_seleccionado["valor"], nombre, cedula, telefono, licencia, fecha_vencimiento, estado) # si hay ID actualiza ese cliente
        else:
            ok = add_conductor(nombre, cedula, telefono, licencia, fecha_vencimiento, estado) # si no hay ID crea uno nuevo

        messagebox.showinfo("Info", "Guardado" if ok else "Error al guardar")
        limpiar()
        cargar_tabla()

    def eliminar():
        id = entry_id.get()

        # Verifica que el ID sea un número
        if not id.isdigit():
            messagebox.showerror("Advertencia", "Ingrese un ID válido para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Desea eliminar este conductor?"):
            ok = delete_conductor(int(id))

            if ok:
                messagebox.showinfo("Info", "Conductor eliminado correctamente")
            elif ok == "RELACIONADO":
                # El conductor tiene despachos asociados y no se puede eliminar
                messagebox.showwarning("No permitido",
                    "No se puede eliminar este conductor porque tiene despachos asociados")
            else:
                # El ID no existe en la BD
                messagebox.showwarning("Advertencia", "El ID no existe")

            limpiar()
            cargar_tabla()

    # BINDS 
    # Al presionar Enter en cada campo, el cursor pasa al siguiente
    entry_nombre.bind("<Return>", lambda e: entry_cedula.focus())
    entry_cedula.bind("<Return>", lambda e: entry_telefono.focus())
    entry_telefono.bind("<Return>", lambda e: entry_licencia.focus())
    entry_licencia.bind("<Return>", lambda e: entry_fecha_vencimiento.focus())
    entry_fecha_vencimiento.bind("<Return>", lambda e: guardar())
    entry_id.bind("<Return>", lambda e: eliminar())

    entry_nombre.focus()  # el cursor empieza en el campo nombre

    # Al hacer clic en una fila de la tabla, llama a seleccionar()
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    # BOTONES 
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Guardar",  command=guardar,  bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Eliminar", command=eliminar, bg="#f44336", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Limpiar",  command=limpiar,  bg="#2196F3", fg="white", width=12).grid(row=0, column=2, padx=5)

    # Carga los conductores al abrir el módulo
    cargar_tabla()