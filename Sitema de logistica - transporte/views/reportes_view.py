import tkinter as tk
from tkinter import ttk, messagebox
from config.db import get_connection

def vista_reportes(frame):
    tk.Label(frame, text="Módulo de Reportes", font=("Arial", 16, "bold")).pack(pady=10)

    def mostrar_reporte(titulo, consulta_sql):
        # Limpia el frame excepto el primer widget (el título principal)
        for widget in frame.winfo_children()[1:]:
            widget.destroy()

        # Botón para volver al menú de reportes
        # Destruye todo el contenido y recarga vista_reportes desde cero
        tk.Button(frame, text="← Volver", command=lambda: [
        [w.destroy() for w in frame.winfo_children()],
        vista_reportes(frame)
        ], bg="#607D8B", fg="white", width=10).pack(anchor="w", padx=10) # anchor="w" alinea el botón a la izquierda
        
        tk.Label(frame, text=titulo, font=("Arial", 12, "bold")).pack(pady=5)

        # Intenta conectarse a la base de datos
        conexion = get_connection()
        if not conexion:
            tk.Label(frame, text="Error: no se pudo conectar a la BD", fg="red").pack()
            return

        # Ejecuta la consulta SQL recibida como parámetro
        cursor = conexion.cursor()
        cursor.execute(consulta_sql)
        filas = cursor.fetchall()
        
        # Extrae los nombres de las columnas desde el cursor
        columnas = [dato[0] for dato in cursor.description]
        cursor.close()
        conexion.close()

        # Si la consulta no devuelve datos, muestra un mensaje informativo
        if not filas:
            tk.Label(frame, text="No hay datos para mostrar.", fg="gray").pack()
            return

        # Crea la tabla visual con columnas dinámicas según la consulta ejecutada
        tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
        
        for columna in columnas:
            tabla.heading(columna, text=columna)   # Nombre de encabezado
            tabla.column(columna, width=150)        # Ancho de cada columna
        
        # Inserta cada fila de resultados en la tabla
        for fila in filas:
            tabla.insert("", "end", values=fila)
        tabla.pack(fill="both", expand=True, padx=10, pady=5)

    # BOTONES DE REPORTES 
    # Cada botón ejecuta una consulta SQL predefinida
    contenedor_botones = tk.Frame(frame)
    contenedor_botones.pack(pady=10)

    # Reporte: cantidad de despachos agrupados por su estado
    tk.Button(contenedor_botones, text="Despachos por estado", width=22, bg="#2196F3", fg="white",
        command=lambda: mostrar_reporte("Despachos por estado",
            "SELECT estado, COUNT(*) AS total FROM despacho GROUP BY estado")
    ).grid(row=0, column=0, padx=5)

    # Reporte: conductores con su total de despachos realizados, ordenados de mayor a menor
    tk.Button(contenedor_botones, text="Conductores activos", width=22, bg="#4CAF50", fg="white",
        command=lambda: mostrar_reporte("Conductores con despachos",
            """SELECT co.nombre AS conductor, COUNT(d.id_despacho) AS total_despachos
               FROM conductor co
               LEFT JOIN despacho d ON co.id_conductor = d.id_conductor
               GROUP BY co.nombre ORDER BY total_despachos DESC""")
    ).grid(row=0, column=1, padx=5)

    # Reporte: vehículos con la cantidad de viajes realizados, ordenados de mayor a menor
    tk.Button(contenedor_botones, text="Vehículos utilizados", width=22, bg="#FF9800", fg="white",
        command=lambda: mostrar_reporte("Uso de vehículos",
            """SELECT v.placa, v.tipo, COUNT(d.id_despacho) AS viajes
               FROM vehiculo v
               LEFT JOIN despacho d ON v.id_vehiculo = d.id_vehiculo
               GROUP BY v.placa, v.tipo ORDER BY viajes DESC""")
    ).grid(row=0, column=2, padx=5)

    # Reporte: conductores cuya fecha de vencimiento de licencia ya pasó
    tk.Button(contenedor_botones, text="Licencias vencidas", width=22, bg="#f44336", fg="white",
        command=lambda: mostrar_reporte("Conductores con licencia vencida",
            """SELECT nombre, cedula, licencia, fecha_vencimiento
               FROM conductor WHERE fecha_vencimiento < CURDATE()
               ORDER BY fecha_vencimiento ASC""")
    ).grid(row=0, column=3, padx=5)

    # FILTROs
    filtros_frame = tk.Frame(frame)
    filtros_frame.pack(pady=5)

    # Filtro 1: Combobox con estados predefinidos
    tk.Label(filtros_frame, text="Filtrar por estado:").grid(row=0, column=0, padx=5, pady=15)
    combo_filtro_estado = ttk.Combobox(filtros_frame, values=["" , "todos", "pendiente", "en ruta", "entregado", "devuelto"], width=12, state="readonly")
    combo_filtro_estado.current(0)  # Selecciona el primer valor por defecto
    combo_filtro_estado.grid(row=0, column=1, padx=5)

    # Filtro 2: Campo de texto para buscar por nombre de conductor
    tk.Label(filtros_frame, text="Filtrar por conductor:").grid(row=0, column=2, padx=5, pady=15)
    entry_filtro_conductor = tk.Entry(filtros_frame, width=15)
    entry_filtro_conductor.grid(row=0, column=3, padx=5)

    # Filtro 3: Rango de fechas (inicio y fin) en formato YYYY-MM-DD
    tk.Label(filtros_frame, text="Fecha inicio:").grid(row=0, column=4, padx=3, pady=15)
    entry_fecha_inicio = tk.Entry(filtros_frame, width=12)
    entry_fecha_inicio.grid(row=0, column=5, padx=5)

    tk.Label(filtros_frame, text="Fecha fin:").grid(row=0, column=6, padx=5, pady=15)
    entry_fecha_fin = tk.Entry(filtros_frame, width=12)
    entry_fecha_fin.grid(row=0, column=7, padx=5)

    def filtrar_por_estado():
        estado = combo_filtro_estado.get().strip()
        # Si selecciona "todos", consulta sin filtro WHERE
        # Si selecciona un estado específico, filtra por ese valor
        if estado == "todos":
            sql = """SELECT d.id_despacho, d.fecha, d.estado,
                            c.nombre, co.nombre, v.placa, de.ciudad
                    FROM despacho d
                    LEFT JOIN cliente c  ON d.id_cliente = c.id_cliente
                    LEFT JOIN conductor co ON d.id_conductor = co.id_conductor
                    LEFT JOIN vehiculo v  ON d.id_vehiculo  = v.id_vehiculo
                    LEFT JOIN destino de ON d.id_destino = de.id_destino"""
        else:
            sql = f"""SELECT d.id_despacho, d.fecha, d.estado,
                            c.nombre, co.nombre, v.placa, de.ciudad
                    FROM despacho d
                    LEFT JOIN cliente c  ON d.id_cliente = c.id_cliente
                    LEFT JOIN conductor co ON d.id_conductor = co.id_conductor
                    LEFT JOIN vehiculo v  ON d.id_vehiculo  = v.id_vehiculo
                    LEFT JOIN destino de ON d.id_destino = de.id_destino
                    WHERE d.estado = '{estado}'"""
        mostrar_reporte("Despachos filtrados por estado", sql)

    def filtrar_por_conductor():
        nombre = entry_filtro_conductor.get()
        # Valida que el campo no esté vacío antes de consultar
        if nombre == "":
            messagebox.showerror("Error", "Escribe el nombre del conductor")
            return
        # LIKE '%nombre%' permite búsqueda parcial (no necesita el nombre exacto)
        sql = f"""SELECT d.id_despacho, d.fecha, d.estado,
                        c.nombre, co.nombre, v.placa, de.ciudad
                FROM despacho d
                LEFT JOIN cliente   c  ON d.id_cliente   = c.id_cliente
                LEFT JOIN conductor co ON d.id_conductor = co.id_conductor
                LEFT JOIN vehiculo  v  ON d.id_vehiculo  = v.id_vehiculo
                LEFT JOIN destino   de ON d.id_destino   = de.id_destino
                WHERE co.nombre LIKE '%{nombre}%'"""
        mostrar_reporte(f"Despachos del conductor: {nombre}", sql)

    def filtrar_por_fechas():
        fecha_inicio = entry_fecha_inicio.get().strip()
        fecha_fin = entry_fecha_fin.get().strip()
        
        # Valida que ambas fechas estén ingresadas
        if fecha_inicio == "" or fecha_fin == "":
            messagebox.showerror("Error", "Debes ingresar ambas fechas en formato YYYY-MM-DD")
            return
        sql = f"""SELECT d.id_despacho, d.fecha, d.estado,
                        c.nombre, co.nombre, v.placa, de.ciudad
                FROM despacho d
                LEFT JOIN cliente   c  ON d.id_cliente   = c.id_cliente
                LEFT JOIN conductor co ON d.id_conductor = co.id_conductor
                LEFT JOIN vehiculo  v  ON d.id_vehiculo  = v.id_vehiculo
                LEFT JOIN destino   de ON d.id_destino   = de.id_destino
                WHERE d.fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"""
        mostrar_reporte(f"Despachos entre {fecha_inicio} y {fecha_fin}", sql)

    entry_filtro_conductor.bind("<Return>", lambda e: filtrar_por_conductor())
    entry_fecha_inicio.bind("<Return>", lambda e: entry_fecha_fin.focus())   # Enter salta al campo fecha fin
    entry_fecha_fin.bind("<Return>", lambda e: filtrar_por_fechas())         # Enter en fecha fin ejecuta el filtro

    # Botones que ejecutan cada función de filtrado
    tk.Button(filtros_frame, text="Filtrar por estado", width=22, bg="#9C27B0", fg="white", command=filtrar_por_estado).grid(row=1, column=1, padx=5, pady=5)

    tk.Button(filtros_frame, text="Filtrar por conductor", width=22, bg="#009688", fg="white", command=filtrar_por_conductor).grid(row=1, column=3, padx=5, pady=5)

    tk.Button(filtros_frame, text="Filtrar por fechas", width=22, bg="#795548", fg="white",command=filtrar_por_fechas).grid(row=1, column=5, padx=5, pady=5)