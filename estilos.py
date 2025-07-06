import tkinter.ttk as ttk

# Colores principales
COLOR_PRINCIPAL = "#2c3e50"  # Azul oscuro
COLOR_SECUNDARIO = "#3498db"  # Azul claro
COLOR_EXITOSO = "#2ecc71"    # Verde
COLOR_ALERTA = "#e74c3c"     # Rojo
COLOR_FONDO = "#ecf0f1"      # Gris claro
COLOR_TEXTO = "#2c3e50"      # Azul oscuro

# Configuración de estilos para ttk
def configurar_estilos(root):
    estilo = ttk.Style()
    
    # Configurar tema clásico
    estilo.theme_use("clam")
    
    # Estilo para el frame principal
    estilo.configure("Principal.TFrame",
                    background=COLOR_FONDO)
    
    # Estilo para los labels
    estilo.configure("TLabel",
                    background=COLOR_FONDO,
                    foreground=COLOR_TEXTO,
                    font=('Arial', 10))
    
    # Estilo para los botones
    estilo.configure("TButton",
                    background=COLOR_SECUNDARIO,
                    foreground="white",
                    font=('Arial', 10, 'bold'))
    
    estilo.map("TButton",
               background=[('active', COLOR_PRINCIPAL),
                          ('pressed', COLOR_PRINCIPAL)])
    
    # Estilo para los combobox
    estilo.configure("TCombobox",
                    fieldbackground="white",
                    background="white",
                    foreground=COLOR_TEXTO,
                    selectbackground=COLOR_SECUNDARIO,
                    selectforeground="white")
    
    # Estilo para los entry
    estilo.configure("TEntry",
                    fieldbackground="white",
                    foreground=COLOR_TEXTO)
    
    # Estilo para el treeview
    estilo.configure("Treeview",
                    background="white",
                    foreground=COLOR_TEXTO,
                    fieldbackground="white")
    
    estilo.map("Treeview",
               background=[('selected', COLOR_SECUNDARIO)],
               foreground=[('selected', 'white')])
    
    # Estilo para los labelframes
    estilo.configure("TLabelframe",
                    background=COLOR_FONDO)
    
    estilo.configure("TLabelframe.Label",
                    background=COLOR_FONDO,
                    foreground=COLOR_PRINCIPAL,
                    font=('Arial', 10, 'bold'))
    
    # Estilo para los mensajes de éxito y error
    estilo.configure("Exito.TLabel",
                    foreground=COLOR_EXITOSO,
                    font=('Arial', 10, 'bold'))
    
    estilo.configure("Alerta.TLabel",
                    foreground=COLOR_ALERTA,
                    font=('Arial', 10, 'bold'))
    
    # Estilo para el título de bienvenida
    estilo.configure("Bienvenida.TLabel",
                    background=COLOR_FONDO,
                    foreground=COLOR_PRINCIPAL,
                    font=('Arial', 24, 'bold'))
    
    # Estilo para el subtítulo de bienvenida
    estilo.configure("Subtitulo.TLabel",
                    background=COLOR_FONDO,
                    foreground=COLOR_PRINCIPAL,
                    font=('Arial', 14, 'bold'))
    
    # Estilo para el botón de bienvenida
    estilo.configure("Bienvenida.TButton",
                    background=COLOR_EXITOSO,
                    foreground="white",
                    font=('Arial', 12, 'bold'))
    
    estilo.map("Bienvenida.TButton",
               background=[('active', '#27ae60'),
                          ('pressed', '#27ae60')])
    
    # Configurar la raíz
    root.configure(background=COLOR_FONDO)
    
    return estilo
