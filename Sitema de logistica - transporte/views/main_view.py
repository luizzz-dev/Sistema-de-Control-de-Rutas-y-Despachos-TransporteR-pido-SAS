import tkinter as tk

# Importación de cada vista del sistema (patrón MVC)
from views.usuarios_view import vista_usuarios
from views.vehiculos_view import vista_vehiculos
from views.conductores_view import vista_conductores
from views.clientes_view import vista_clientes
from views.despachos_view import vista_despachos
from views.reportes_view import vista_reportes
from views.destino_view import vista_destinos

def crear_ventana_principal(username):
    # Crea la ventana principal del sistema
    ventana = tk.Tk()
    ventana.title("Sistema de Logística - Menú Principal")
    ventana.geometry("1000x650")

    # Mensaje de bienvenida en la esquina superior derecha
    # anchor="e" lo alinea a la derecha (East)
    tk.Label(ventana, text=f"Bienvenido, {username} 👤",
             font=("Arial", 10), fg="gray").pack(anchor="e", padx=10)

    # SIDEBAR
    frame_sidebar = tk.Frame(ventana, width=150)
    frame_sidebar.pack(side="left", fill="y")
    # pack_propagate(False) evita que el frame se redimensione
    # según su contenido interno
    frame_sidebar.pack_propagate(False)

    tk.Label(frame_sidebar, text="Menú", font=("Arial", 12, "bold")).pack(pady=10)

    # CONTENIDO (del lado derecho)
    frame_contenido = tk.Frame(ventana)
    frame_contenido.pack(side="right", fill="both", expand=True)

    def limpiar_frame():
        # Elimina todos los widgets del panel de contenido
        # antes de cargar una nueva vista
        for widget in frame_contenido.winfo_children():
            widget.destroy()

    def mostrar_bienvenida():
        # Vista inicial al abrir el sistema
        limpiar_frame()
        tk.Label(frame_contenido, text="Bienvenido al Sistema de Logística",
                 font=("Arial", 16, "bold")).pack(expand=True)

    # Funciones de navegación
    # Cada función limpia el contenido actual y carga su vista correspondiente

    def abrir_usuarios():
        limpiar_frame()
        vista_usuarios(frame_contenido)

    def abrir_vehiculos():
        limpiar_frame()
        vista_vehiculos(frame_contenido)

    def abrir_conductores():
        limpiar_frame()
        vista_conductores(frame_contenido)

    def abrir_clientes():
        limpiar_frame()
        vista_clientes(frame_contenido)

    def abrir_destinos():
        limpiar_frame()
        vista_destinos(frame_contenido)

    def abrir_despachos():
        limpiar_frame()
        vista_despachos(frame_contenido)

    def abrir_reportes():
        limpiar_frame()
        vista_reportes(frame_contenido)

    # BOTONES 
    botones = [
        ("Usuarios",    abrir_usuarios),
        ("Vehículos",   abrir_vehiculos),
        ("Conductores", abrir_conductores),
        ("Clientes",    abrir_clientes),
        ("Destinos",    abrir_destinos),
        ("Despachos",   abrir_despachos),
        ("Reportes",    abrir_reportes)
    ]

    for texto, comando in botones:
        if texto == "Reportes":
            # y se ubica al fondo del sidebar con side="bottom"
            tk.Button(frame_sidebar, text=texto, command=comando,
                    width=15, bg="#f44336", fg="white").pack(side="bottom", pady=20)
        else:
            # El resto de botones se apilan normalmente de arriba hacia abajo
            tk.Button(frame_sidebar, text=texto, command=comando,
                  width=15).pack(pady=10)

    # Muestra la pantalla de bienvenida al iniciar
    mostrar_bienvenida()
    
    # Inicia el bucle principal de la interfaz gráfica
    ventana.mainloop()