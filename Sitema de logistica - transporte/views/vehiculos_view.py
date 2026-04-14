import tkinter as tk
from tkinter import ttk, messagebox
from controllers.vehiculo_controller import (
    get_vehiculos,
    add_vehiculo,
    update_vehiculo,
    delete_vehiculo
)

def vista_vehiculos(frame):
    tk.Label(frame, text="Módulo de Vehículos", font=("Arial", 16, "bold")).pack(pady=10)

    #buscar
    buscar_frame = tk.Frame(frame)
    buscar_frame.pack(pady=5)

    tk.Label(buscar_frame, text="Buscar por placa:").grid(row=0, column=0, padx=5)
    entry_buscar = tk.Entry(buscar_frame, width=20)
    entry_buscar.grid(row=0, column=1, padx=5)
    tk.Button(buscar_frame, text = "Buscar", command=lambda: buscar(),
            bg="#607D8B", fg="white", width=10).grid(row=0, column=2, padx=5)
    tk.Button(buscar_frame, text = "Limpiar", command=lambda: [
        entry_buscar.delete(0, "end"), cargar_tabla()
    ], bg="#9E9E9E", fg="white", width=10).grid(row=0, column=3, padx=5)

    def buscar():
        texto = entry_buscar.get().strip()
        if texto == "":
            cargar_tabla()
            return
        for fila in tabla.get_children():
            tabla.delete(fila)
        for vehiculo in get_vehiculos():
            if texto.lower() in str(vehiculo[1]).lower(): #vehiculo[1] es la placa
                tabla.insert("", "end", values=vehiculo)
    
    #validacion (solo numeros)
    def solo_numeros(texto):
        return texto.isdigit() or texto == ""

    vcmd = (frame.register(solo_numeros), "%P")

    # TABLA
    tabla = ttk.Treeview(frame, columns=("ID", "Placa", "Tipo", "Capacidad", "Estado"), show="headings", height=10)
    tabla.heading("ID", text="ID")
    tabla.heading("Placa", text="Placa")
    tabla.heading("Tipo", text="Tipo")
    tabla.heading("Capacidad", text="Capacidad")
    tabla.heading("Estado", text="Estado")
    tabla.pack(pady=10)

    # FORMULARIO
    form = tk.Frame(frame)
    form.pack(pady=10)

    tk.Label(form, text="Placa").grid(row=0, column=0)
    tk.Label(form, text="Tipo").grid(row=0, column=1)
    tk.Label(form, text="Capacidad").grid(row=0, column=2)
    tk.Label(form, text="Estado").grid(row=0, column=3)
    tk.Label(form, text="ID para eliminar").grid(row=0, column=4, padx=(30, 5))

    entry_placa = tk.Entry(form, width=15)
    entry_tipo = tk.Entry(form, width=15)
    entry_capacidad = tk.Entry(form, width=15, validate="key", validatecommand=vcmd)
    entry_id = tk.Entry(form, width=10, validate="key", validatecommand=vcmd)

    # Combobox para estado ("propio" o "subcontratado")
    combo_estado = ttk.Combobox(form, values=["propio", "subcontratado"], width=13, state="readonly")
    combo_estado.current(0) # Selecciona "propio" por defecto

    entry_placa.grid(row=1, column=0)
    entry_tipo.grid(row=1, column=1)
    entry_capacidad.grid(row=1, column=2)
    combo_estado.grid(row=1, column=3)
    entry_id.grid(row=1, column=4, padx=(30, 5))

    id_seleccionado = {"valor": None}

    def cargar_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for vehiculo in get_vehiculos():
            tabla.insert("", "end", values=vehiculo)

    def seleccionar(event):
        fila = tabla.focus()
        if not fila:
            return
        valores = tabla.item(fila, "values")
        id_seleccionado["valor"] = valores[0]
       
        entry_placa.delete(0, "end");     
        entry_placa.insert(0, valores[1])
       
        entry_tipo.delete(0, "end");      
        entry_tipo.insert(0, valores[2])
       
        entry_capacidad.delete(0, "end"); 
        entry_capacidad.insert(0, valores[3])
        combo_estado.set(valores[4])
       
        entry_id.delete(0, "end");        
        entry_id.insert(0, valores[0])

    def limpiar():
        entry_placa.delete(0, "end")
        entry_tipo.delete(0, "end")
        entry_capacidad.delete(0, "end")
        combo_estado.current(0) # vuleve a "propio"
        entry_id.delete(0, "end")
        id_seleccionado["valor"] = None

    def guardar():
        placa     = entry_placa.get()
        tipo      = entry_tipo.get()
        capacidad = entry_capacidad.get()
        estado    = combo_estado.get()

        if placa == "":
            messagebox.showerror("Error", "La placa es obligatoria")
            return

        if id_seleccionado["valor"]:
            ok = update_vehiculo(id_seleccionado["valor"], placa, tipo, capacidad, estado)
        else:
            ok = add_vehiculo(placa, tipo, capacidad, estado)

        messagebox.showinfo("Info", "Guardado" if ok else "Error al guardar")
        limpiar()
        cargar_tabla()

    def eliminar():
        id = entry_id.get()

        if not id.isdigit():
            messagebox.showerror("Advertencia", "Ingrese un ID válido para eliminar")
            return 

        if messagebox.askyesno("Confirmar", "¿Desea eliminar este vehículo?"):
            ok = delete_cliente(int(id))

            if ok:
                messagebox.showinfo("Info", "Vehículo eliminado correctamente")

            elif ok == "RELACIONADO":
                messagebox.showwarning(
                    "No permitido",
                    "No se puede eliminar este vehículo porque tiene despachos asociados"
                )

            else:
                messagebox.showwarning("Advertencia", "El ID no existe")

            limpiar()
            cargar_tabla()

    entry_placa.bind("<Return>", lambda e: entry_tipo.focus())
    entry_tipo.bind("<Return>", lambda e: entry_capacidad.focus())
    entry_capacidad.bind("<Return>", lambda e: combo_estado.focus())
    combo_estado.bind("<Return>", lambda e: guardar())
    entry_id.bind("<Return>", lambda e: eliminar())
    entry_placa.focus()

    # BOTONES
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Guardar",  command=guardar,  bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Eliminar", command=eliminar, bg="#f44336", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Limpiar",  command=limpiar,  bg="#2196F3", fg="white", width=12).grid(row=0, column=2, padx=5)

    cargar_tabla()

