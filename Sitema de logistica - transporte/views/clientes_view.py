import tkinter as tk
from tkinter import ttk, messagebox # widgtes comm tablas y ventanas de alerta
from controllers.cliente_controller import get_clientes
from controllers.cliente_controller import (
    get_clientes,
    add_cliente,
    update_cliente,
    delete_cliente
)

def vista_clientes(frame):
    tk.Label(frame, text = "Módulo de Clientes", font = ("Arial", 16, "bold")).pack(pady=10)

    #VALIDACIÓN SOLO NÚMEROS
    def solo_numeros(texto):
        return texto.isdigit() or texto == "" #text.isdigit devuelve True si todos los caractres son numeros o vacio si esta vacio

    vcmd = (frame.register(solo_numeros), '%P') # conecta la validacion con los inputs

    # BUSCADOR
    buscar_frame = tk.Frame(frame)
    buscar_frame.pack(pady=5)

    tk.Label(buscar_frame, text="Buscar por nombre:").grid(row=0, column=0, padx=5)
    entry_buscar = tk.Entry(buscar_frame, width=20)
    entry_buscar.grid(row=0, column=1, padx=5)
    
    # boton que ejecuta la busqueda
    tk.Button(buscar_frame, text = "Buscar", command=lambda: buscar(),
            bg="#607D8B", fg="white", width=10).grid(row=0, column=2, padx=5)
    
    # Botón que limpia el buscador y recarga todos los conductores
    tk.Button(buscar_frame, text = "Limpiar", command=lambda: [
        entry_buscar.delete(0, "end"), cargar_tabla()
    ], bg="#9E9E9E", fg="white", width=10).grid(row=0, column=3, padx=5)

    def buscar():
        texto = entry_buscar.get().strip() # toma lo que escribio el usuario
        
        if texto == "":
            cargar_tabla()
            return  # si no escribio nada recarga toda la tabla
        
        for fila in tabla.get_children():
            tabla.delete(fila)  # limpia la tabla antes de mostrar el redultado
        
        for cliente in get_clientes():
            # cliente[1] es el nombre
            if texto.lower() in str(cliente[1]).lower():    # busca coincidencias en el nombre sin importa mayusculas
                tabla.insert("", "end", values=cliente)     # si el texto esta dentro del nombre que lo muestre( an: juan, ana, andres)


    # TABLA
    tabla = ttk.Treeview(frame, columns = ("ID", "Nombre", "NIT", "Teléfono", "Dirección"), show = "headings", height = 10) #donde ves lo cliente
    # las columnas
    tabla.heading("ID", text = "ID")
    tabla.heading("Nombre", text = "Nombre")
    tabla.heading("NIT", text = "NIT")
    tabla.heading("Teléfono", text = "Teléfono")
    tabla.heading("Dirección", text = "Dirección")
    tabla.pack(pady=10)

    # FORMULARIO
    form = tk.Frame(frame)
    form.pack(pady = 10)

    tk.Label(form, text = "Nombre").grid(row = 0, column = 0)
    tk.Label(form, text = "NIT").grid(row = 0, column = 1)
    tk.Label(form, text = "Teléfono").grid(row = 0, column = 2)
    tk.Label(form, text="Dirección").grid(row=0, column=3, padx=5)
    tk.Label(form, text="ID para eliminar").grid(row=0, column=4, padx=(30, 5))

    entry_nombre = tk.Entry(form, width = 15)
    entry_nit = tk.Entry(form, width = 15, validate="key", validatecommand=vcmd) # validacion numerica
    entry_telefono = tk.Entry(form, width = 15, validate="key", validatecommand=vcmd) # validacion numerica
    entry_direccion = tk.Entry(form, width = 15)

    #AQUÍ APLICAMOS VALIDACIÓN
    entry_id = tk.Entry(form, width=10, validate="key", validatecommand=vcmd) # validacion numerica

    entry_nombre.grid(row = 1, column = 0)
    entry_nit.grid(row = 1, column = 1)
    entry_telefono.grid(row = 1, column = 2)
    entry_direccion.grid(row=1, column=3, padx=5)
    entry_id.grid(row=1, column=4, padx=(30, 5))

    id_seleccionado = {"valor": None}   #Guarda el ID del cliente seleccionado en la tabla(saber si se esta editando o creando)

    def cargar_tabla():
        # limpia la tabla
        for fila in tabla.get_children():
            tabla.delete(fila)
        
        # trae lo clientes de la base de datos y los inserta
        for cliente in get_clientes():
            tabla.insert("", "end", values = cliente)

    # cuando hago clic: tomar los datos de esa fila y cargarlos en los campos del formulario 
    # para poder editarlos o verlos.
    def seleccionar(event):
        fila = tabla.focus()         
        if not fila:
            return
        
        valores = tabla.item(fila, "values") # obtiene los datos de la fila (id, nombre, nit, telefono, direccion)
        id_seleccionado["valor"] = valores[0] # guarda el ID del cliente seleccionado
        
        entry_nombre.delete(0, "end");     # primero limpia el campo
        entry_nombre.insert(0, valores[1]) # luego inserta el valor que corresponde
       
        entry_nit.delete(0, "end");       
        entry_nit.insert(0, valores[2])
        
        entry_telefono.delete(0, "end");  
        entry_telefono.insert(0, valores[3])
        
        entry_direccion.delete(0, "end"); 
        entry_direccion.insert(0, valores[4])
        
        entry_id.delete(0, "end");        
        entry_id.insert(0, valores[0])

    def limpiar():
        entry_nombre.delete(0, "end")
        entry_nit.delete(0, "end")
        entry_telefono.delete(0, "end")
        entry_direccion.delete(0, "end")
        entry_id.delete(0, "end")
        id_seleccionado["valor"] = None # resetea el ID

    def guardar():
        #lee los valosres del formulario
        nombre = entry_nombre.get()
        nit = entry_nit.get()
        telefono = entry_telefono.get()
        direccion = entry_direccion.get()

        if nombre == "":
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        # si hay un ID lo estoy editando
        # si no hay un ID lo estoy creando 
        if id_seleccionado["valor"]:
            ok = update_cliente(id_seleccionado["valor"], nombre, nit, telefono, direccion) # si hay ID actualiza ese cliente
        else:
            ok = add_cliente(nombre, nit, telefono, direccion) # si no hay ID crea uno nuevo

        messagebox.showinfo("Info", "Guardado" if ok else "Error al guardar")
        limpiar()
        cargar_tabla()

    def eliminar():
        id = entry_id.get()

        if not id.isdigit():
            messagebox.showerror("Advertencia", "Ingrese un ID válido para eliminar")
            return 

        if messagebox.askyesno("Confirmar", "¿Desea eliminar este cliente?"):
            ok = delete_cliente(id)

            if ok == True:
                messagebox.showinfo("Info", "Cliente eliminado correctamente")

            elif ok == "RELACIONADO":
                messagebox.showwarning(
                    "No permitido",
                    "No se puede eliminar porque el cliente tiene despachos asociados"
                )

            elif ok == False:
                messagebox.showwarning("Advertencia", "El ID no existe")

            else:
                messagebox.showerror("Error", "Error inesperado")

            limpiar()
            cargar_tabla()
    #BINDS 
    entry_buscar.bind("<Return>", lambda e: buscar())
    entry_nombre.bind("<Return>", lambda e: entry_nit.focus())
    entry_nit.bind("<Return>", lambda e: entry_telefono.focus())
    entry_telefono.bind("<Return>", lambda e: entry_direccion.focus())
    entry_direccion.bind("<Return>", lambda e: guardar())
    entry_id.bind("<Return>", lambda e: eliminar())

    entry_nombre.focus()

    # BOTONES
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Guardar",  command=guardar,  bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Eliminar", command=eliminar, bg="#f44336", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Limpiar",  command=limpiar,  bg="#2196F3", fg="white", width=12).grid(row=0, column=2, padx=5)

    cargar_tabla()