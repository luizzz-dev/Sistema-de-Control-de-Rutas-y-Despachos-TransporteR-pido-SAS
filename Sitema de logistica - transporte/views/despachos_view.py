import tkinter as tk
from tkinter import ttk, messagebox
from config.db import get_connection
from datetime import date
from controllers.despacho_controller import (
    get_despachos,
    add_despacho,
    update_despacho,
    delete_despacho
)
from config.db import get_connection

def vista_despachos(frame):
    tk.Label(frame, text="Módulo de Despachos", font=("Arial", 16, "bold")).pack(pady=10)

    # TABLA
    tabla = ttk.Treeview(frame, columns=("ID", "Fecha", "Estado", "Cliente", "Conductor", "Vehículo", "Destino"), show="headings", height=7)
    
    #evitar repetir tabla.heading
    for col in ("ID", "Fecha", "Estado", "Cliente", "Conductor", "Vehículo", "Destino"):
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(pady=5)

    # FORMULARIO
    form = tk.Frame(frame)
    form.pack(pady=5)

    tk.Label(form, text="Fecha\n(YYYY-MM-DD)").grid(row=0, column=0, padx=5)
    tk.Label(form, text="Estado").grid(row=0, column=1, padx=5)
    tk.Label(form, text="Cliente").grid(row=0, column=2, padx=5)
    tk.Label(form, text="Conductor").grid(row=0, column=3, padx=5)
    tk.Label(form, text="Vehículo").grid(row=0, column=4, padx=5)
    tk.Label(form, text="Destino").grid(row=0, column=5, padx=5)
    tk.Label(form, text="ID para\neliminar").grid(row=0, column=6, padx=(30,5))


    # una lista despegable
    # state = "redondly" evita que lo escribamos
    combo_estado = ttk.Combobox(form, values=[ "","Pendiente", "En_ruta", "Entregado", "Devuelto"], width=10, state="readonly")
    combo_estado.current(0) # selecciona el primer valor por defecto
    combo_estado.grid(row=1, column=1, padx=5)

    #VALIDACIÓN SOLO NÚMEROS
    def solo_numeros(texto):
        return texto.isdigit() or texto == "" #text.isdigit devuelve True si todos los caractres son numeros o vacio si esta vacio

    vcmd = (frame.register(solo_numeros), '%P')  # conecta la validacion con los inputs

    entry_fecha = tk.Entry(form, width=12)
    entry_fecha.grid(row=1, column=0, padx=5)

    #Cargar opciones desde la BD (clientes, conductores, vehiculos y destinos en los combobox)
    def cargar_opciones(sql):
        conn = get_connection()
        if not conn: return []
        cursor = conn.cursor()
        cursor.execute(sql)
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return filas

    #traer los datos reales de cliente, conductores vehiculos y destinos
    clientes = cargar_opciones("SELECT id_cliente, nombre FROM cliente")
    conductores = cargar_opciones("SELECT id_conductor, nombre FROM conductor WHERE estado = 'activo'") #solomuestra los activos
    vehiculos = cargar_opciones("SELECT id_vehiculo, placa FROM vehiculo")
    destinos = cargar_opciones("SELECT id_destino, ciudad FROM destino")

    # Crea un diccionario donde la clave es el texto que ve el usuario "Empresa ABC (ID:1)" 
    # el valor es el ID 1. Así el Combobox muestra nombres pero internamente guardamos IDs.
    # r: representa cada registro
    # r[0]: es el ID
    # r[1]: es el nombre
    map_cli = {f"{r[1]} (ID:{r[0]})": r[0] for r in clientes}
    map_con = {f"{r[1]} (ID:{r[0]})": r[0] for r in conductores}
    map_veh = {f"{r[1]} (ID:{r[0]})": r[0] for r in vehiculos}
    map_des = {f"{r[1]} (ID:{r[0]})": r[0] for r in destinos}

    # lista despegable mostrando los datos
    # values: opciones que vera el usuario
    # state="readonly": no se puede escribir, solo seleccionar
    # values=list(map_cli.keys()): Muéstrame todas las claves del diccionario map_cli como opciones
    combo_cli = ttk.Combobox(form, values=list(map_cli.keys()), width=15, state="readonly")
    combo_con = ttk.Combobox(form, values=list(map_con.keys()), width=15, state="readonly")
    combo_veh = ttk.Combobox(form, values=list(map_veh.keys()), width=15, state="readonly")
    combo_des = ttk.Combobox(form, values=list(map_des.keys()), width=15, state="readonly")

    combo_cli.grid(row=1, column=2, padx=5)
    combo_con.grid(row=1, column=3, padx=5)
    combo_veh.grid(row=1, column=4, padx=5)
    combo_des.grid(row=1, column=5, padx=5)

    # ENTRY CON VALIDACIÓN
    entry_id = tk.Entry(form, width=10)
    entry_id.grid(row=1, column=6, padx=(30,5))

    id_seleccionado = {"valor": None}  #Guarda el ID del despacho seleccionado en la tabla(saber si se esta editando o creando)

    def cargar_tabla():
        # limpia la tabla
        for fila in tabla.get_children():
            tabla.delete(fila)
        
        #trae lso despachos de la BD y los inserta
        for despacho in get_despachos():
            tabla.insert("", "end", values=despacho)


    # cuando hago clic: tomar los datos de esa fila y cargarlos en los campos del formulario 
    # para poder editarlos o verlos.
    def seleccionar(event):
        fila = tabla.focus()  # fila que el usuario seleccionó
        if not fila:
            return
        
        valores = tabla.item(fila, "values")# obtiene los datos de la fila (fecha, estado, cliente, ect)
        id_seleccionado["valor"] = valores[0] # guarda el ID
        
        entry_fecha.delete(0, "end") # primero limpia el campo
        entry_fecha.insert(0, valores[1]) # luego inserta el valor que corresponde
        
        combo_estado.set(valores[2]) # selecciona el estado
        
        entry_id.delete(0, "end")
        entry_id.insert(0, valores[0])  # llena el ID para eliminar

    def limpiar():
        entry_fecha.delete(0, "end")   # borra la fecha
        combo_estado.current(0)          # vuelve al primer estado
        combo_cli.set("")                # limpia el combobox de cliente
        combo_con.set("")                # limpia el de conductor
        combo_veh.set("")                # limpia el de vehículo
        combo_des.set("")                # limpia el de destino
        entry_id.delete(0, tk.END)       # borra el ID
        id_seleccionado["valor"] = None  # olvida el despacho seleccionado

    def guardar():
        fecha = entry_fecha.get().strip()
        estado = combo_estado.get()
        cli_k = combo_cli.get()
        con_k = combo_con.get()
        veh_k = combo_veh.get()
        des_k = combo_des.get()

        # Verifica que todos los campos estén llenos antes de continuar.
        if not fecha or not cli_k or not con_k or not veh_k or not des_k:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        id_cli = map_cli[cli_k]  # obtiene el ID del cliente seleccionado
        id_con = map_con[con_k]  # obtiene el ID del conductor
        id_veh = map_veh[veh_k]  # obtiene el ID del vehículo
        id_des = map_des[des_k]  # obtiene el ID del destino

        # Despacho entregado no se puede modificar 
        if id_seleccionado["valor"]:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT estado FROM despacho WHERE id_despacho = %s", (id_seleccionado["valor"],))
            fila = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if fila and fila[0] == "entregado":
                messagebox.showerror("No permitido", " Este despacho ya fue entregado y no puede modificarse.")
                return

        # Vehículo no puede estar en dos despachos en_ruta
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT id_despacho FROM despacho WHERE id_vehiculo = %s AND estado = 'en_ruta'"
        params = [id_veh]
        
        if id_seleccionado["valor"]:
            sql += " AND id_despacho != %s"
            params.append(id_seleccionado["valor"])
        cursor.execute(sql, params)
        
        if cursor.fetchone():
            cursor.close(); conn.close()
            messagebox.showerror("Error", "El vehículo ya tiene un despacho activo en ruta.")
            return
        cursor.close(); conn.close()

        # Conductor no puede tener dos despachos en_ruta 
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT id_despacho FROM despacho WHERE id_conductor = %s AND estado = 'en_ruta'"
        params = [id_con]
        
        if id_seleccionado["valor"]:
            sql += " AND id_despacho != %s"
            params.append(id_seleccionado["valor"])
        cursor.execute(sql, params)
        
        if cursor.fetchone():
            cursor.close()
            conn.close()
            messagebox.showerror("Error", "El conductor ya tiene un despacho activo en ruta.")
            return
        cursor.close()
        conn.close()

        # Conductor no puede tener licencia vencida 
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT fecha_vencimiento FROM conductor WHERE id_conductor = %s", (id_con,))
        conductor = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if conductor and conductor[0] < date.today(): # conductor[0]: es la fecha de vencimiento y date.today es la fecha de hoy
            messagebox.showerror("Error", f"La licencia del conductor venció el {conductor[0]}.")
            return

        # Guardar en BD
        if id_seleccionado["valor"]:
            ok = update_despacho(id_seleccionado["valor"], id_cli, id_con, id_veh, id_des, fecha, estado) # si hay ID actualiza ese cliente
        else:
            ok = add_despacho(id_cli, id_con, id_veh, id_des, fecha, estado) # si no hay ID crea uno nuevo

        messagebox.showinfo("Info", "Guardado" if ok else "Error al guardar")
        limpiar()
        cargar_tabla()
       
    def eliminar():
        id = entry_id.get()

        if not id.isdigit(): # el ID debe ser numero
            messagebox.showerror("Advertencia", "Ingrese un ID válido para eliminar")
            return 

        if messagebox.askyesno("Confirmar", "¿Desea eliminar este despacho?"):
            ok = delete_despacho(int(id))

            if ok:
                messagebox.showinfo("Info", "Despacho eliminado correctamente")

            elif ok == "RELACIONADO":
                messagebox.showwarning(
                    "No permitido",
                    "No se puede eliminar este despacho porque tiene registros asociados"
                )

            else:
                messagebox.showwarning("Advertencia", "El ID no existe")

            limpiar()
            cargar_tabla()

    tabla.bind("<<TreeviewSelect>>", seleccionar)
    entry_id.bind("<Return>", lambda e: eliminar())

    # BOTONES
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Guardar",  command=guardar,  bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Eliminar", command=eliminar, bg="#f44336", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Limpiar",  command=limpiar,  bg="#2196F3", fg="white", width=12).grid(row=0, column=2, padx=5)

    cargar_tabla()