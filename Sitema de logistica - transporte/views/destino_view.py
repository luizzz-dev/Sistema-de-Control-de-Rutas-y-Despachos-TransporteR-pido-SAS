import tkinter as tk
from tkinter import ttk, messagebox  # widgets como tablas y ventanas de alerta
from controllers.destino_controller import (
    get_destinos,
    add_destino,
    update_destino,
    delete_destino
)

def vista_destinos(frame):
    # Título del módulo
    tk.Label(frame, text="Módulo de Destinos", font=("Arial", 16, "bold")).pack(pady=10)

    # BUSCADOr
    buscar_frame = tk.Frame(frame)
    buscar_frame.pack(pady=5)

    tk.Label(buscar_frame, text="Buscar por ciudad:").grid(row=0, column=0, padx=5)
    entry_buscar = tk.Entry(buscar_frame, width=20)  # campo donde el usuario escribe lo que busca
    entry_buscar.grid(row=0, column=1, padx=5)

    # Botón que ejecuta la búsqueda
    tk.Button(buscar_frame, text="Buscar", command=lambda: buscar(),
            bg="#607D8B", fg="white", width=10).grid(row=0, column=2, padx=5)

    # Botón que limpia el buscador y muestra todos los destinos de nuevo
    tk.Button(buscar_frame, text="Limpiar", command=lambda: [
        entry_buscar.delete(0, "end"), cargar_tabla()
    ], bg="#9E9E9E", fg="white", width=10).grid(row=0, column=3, padx=5)

    def buscar():
        texto = entry_buscar.get().strip()  # lee lo que escribió el usuario
        
        if texto == "":
            cargar_tabla()  # si está vacío muestra todos
            return
        
        for fila in tabla.get_children():
            tabla.delete(fila)  # borra la tabla actual
        
        for destino in get_destinos():
            if texto.lower() in str(destino[1]).lower():  # destino[1] es la ciudad
                tabla.insert("", "end", values=destino)   # agrega los que coincidan

    # TABLA
    # Muestra todos los destinos registrados en la BD
    tabla = ttk.Treeview(frame, columns=("ID", "Ciudad", "Dirección", "Departamento"), show="headings", height=10)
    tabla.heading("ID", text="ID")
    tabla.heading("Ciudad", text="Ciudad")
    tabla.heading("Dirección", text="Dirección")
    tabla.heading("Departamento", text="Departamento")
    tabla.pack(pady=10)

    # FORMULARIo
    form = tk.Frame(frame)
    form.pack(pady=10)

    # Etiquetas de cada campo
    tk.Label(form, text="Ciudad").grid(row=0, column=0)
    tk.Label(form, text="Dirección").grid(row=0, column=1)
    tk.Label(form, text="Departamento").grid(row=0, column=2)
    tk.Label(form, text="ID para eliminar").grid(row=0, column=4, padx=(30, 5))

    # Campos de texto para ingresar datos del destino
    entry_ciudad  = tk.Entry(form, width=15)
    entry_direccion  = tk.Entry(form, width=15)
    entry_departamento = tk.Entry(form, width=15)

    # VALIDACIÓN — solo permite escribir números en el campo ID
    def solo_numeros(valor):
        return valor.isdigit() or valor == ""  # acepta dígitos o campo vacío

    # Registra la validación para usarla en el entry_id
    vcmd = (frame.register(solo_numeros), "%P")  # conecta la validacion con los inputs

    entry_id = tk.Entry(form, width=10, validate="key", validatecommand=vcmd)  # solo números

    # Ubica cada campo en su columna
    entry_ciudad.grid(row=1, column=0)
    entry_direccion.grid(row=1, column=1)
    entry_departamento.grid(row=1, column=2)
    entry_id.grid(row=1, column=4, padx=(30, 5))

    # Guarda el ID del destino seleccionado en la tabla
    id_seleccionado = {"valor": None}

    # FUNCIONEs

    def cargar_tabla():
        # limpia la tabla
        for fila in tabla.get_children():
            tabla.delete(fila)
       
        # trae lo clientes de la base de datos y los inserta
        for destino in get_destinos():
            tabla.insert("", "end", values=destino)

    # cuando hago clic: tomar los datos de esa fila y cargarlos en los campos del formulario 
    # para poder editarlos o verlos.
    def seleccionar(event):
        # Cuando el usuario hace clic en una fila, llena el formulario con esos datos
        fila = tabla.focus()
        if not fila:
            return
        valores = tabla.item(fila, "values") # obtiene los datos de la fila (ciudad, direccion, etc)
        id_seleccionado["valor"] = valores[0]  # guarda el ID del destino seleccionado

        # Llena cada campo con el valor de la fila seleccionada
        entry_ciudad.delete(0, "end");       
        entry_ciudad.insert(0, valores[1])
        
        entry_direccion.delete(0, "end");    # primero limpia el camp
        entry_direccion.insert(0, valores[2]) # luego inserta el valor que corresponde
        
        entry_departamento.delete(0, "end"); 
        entry_departamento.insert(0, valores[3])
        
        entry_id.delete(0, "end");           
        entry_id.insert(0, valores[0])

    def limpiar():
        # Borra todos los campos y olvida el destino seleccionado
        entry_ciudad.delete(0, "end")
        entry_direccion.delete(0, "end")
        entry_departamento.delete(0, "end")
        entry_id.delete(0, "end")
        id_seleccionado["valor"] = None  # resetea el ID

    def guardar():
        # Lee los valores del formulario
        ciudad = entry_ciudad.get()
        direccion = entry_direccion.get()
        departamento = entry_departamento.get()

        # La ciudad es obligatoria
        if ciudad == "":
            messagebox.showerror("Error", "La ciudad es obligatoria")
            return

        # Si hay un destino seleccionado → actualiza, si no → crea uno nuevo
        if id_seleccionado["valor"]:
            ok = update_destino(id_seleccionado["valor"], ciudad, direccion, departamento)
        else:
            ok = add_destino(ciudad, direccion, departamento)

        messagebox.showinfo("Info", "Guardado" if ok else "Error al guardar")
        limpiar()
        cargar_tabla()

    def eliminar():
        id = entry_id.get()

        # Verifica que el ID sea un número
        if not id.isdigit():
            messagebox.showerror("Advertencia", "Ingrese un ID válido para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Desea eliminar este destino?"):
            ok = delete_destino(int(id))

            if ok:
                # Eliminado correctamente
                messagebox.showinfo("Info", "Destino eliminado correctamente")
            elif ok == "RELACIONADO":
                # Tiene despachos asociados, no se puede eliminar
                messagebox.showwarning("No permitido",
                    "No se puede eliminar este destino porque tiene despachos asociados")
            else:
                # El ID no existe en la BD
                messagebox.showwarning("Advertencia", "El ID no existe")

            limpiar()
            cargar_tabla()

    # BINDS
    # Al presionar Enter en cada campo, el cursor pasa al siguiente
    entry_ciudad.bind("<Return>", lambda e: entry_direccion.focus())
    entry_direccion.bind("<Return>", lambda e: entry_departamento.focus())
    entry_departamento.bind("<Return>", lambda e: guardar())
    entry_id.bind("<Return>", lambda e: eliminar())
    entry_ciudad.focus()  # el cursor empieza en el campo ciudad

    # Al hacer clic en una fila de la tabla, llama a seleccionar()
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    # BOTONES 
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Guardar",  command=guardar,  bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Eliminar", command=eliminar, bg="#f44336", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Limpiar",  command=limpiar,  bg="#2196F3", fg="white", width=12).grid(row=0, column=2, padx=5)

    # Carga los destinos al abrir el módulo
    cargar_tabla()