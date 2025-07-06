import tkinter as tk
from tkinter import ttk, messagebox, font
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import pandas as pd
import datetime
from pathlib import Path
import sys
import os
import matplotlib
matplotlib.use('TkAgg')  # Usar el backend de Tkinter para matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates

class AplicacionFinanzas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Financiera - Olivella")
        self.root.geometry("1200x800")
        
        # Configurar tema y estilos
        try:
            self.style = ttkb.Style("superhero")  # Tema más robusto
        except Exception as e:
            print(f"Error al cargar el tema: {e}")
            self.style = ttkb.Style("default")
        
        try:
            self.style.configure("TLabel", font=('Segoe UI', 10))
        except Exception as e:
            print(f"Error al configurar el estilo: {e}")
            self.style.configure("TLabel", font=('Arial', 10))
        
        # Variables para el período y tipo de gráfico
        self.periodo_grafico = tk.StringVar(value="Mes")  # Valores: 'Día', 'Semana', 'Mes'
        self.periodo_valores = {
            'Día': 'dia',
            'Semana': 'semana',
            'Mes': 'mes'
        }
        
        # Variable para el tipo de gráfico
        self.tipo_grafico = tk.StringVar(value="linea")  # Valores: 'linea', 'barras', 'area'
        
        # Variable para el tema
        self.tema_oscuro = False  # Tema claro por defecto
        
        # Mostrar pantalla de bienvenida
        self.mostrar_bienvenida()
    
    def mostrar_bienvenida(self):
        """Mostrar pantalla de bienvenida"""
        self.frame_bienvenida = ttkb.Frame(self.root, padding=40)
        self.frame_bienvenida.place(relx=0.5, rely=0.5, anchor='center')
        
        # Contenedor principal
        container = ttkb.Frame(self.frame_bienvenida, bootstyle="light")
        container.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Logo y título
        ttkb.Label(
            container, 
            text="💰", 
            font=('Segoe UI', 64),
            bootstyle="inverse-light"
        ).pack(pady=(0, 20))
        
        ttkb.Label(
            container,
            text="Bienvenidos a",
            font=('Segoe UI', 14),
            bootstyle="secondary"
        ).pack()
        
        ttkb.Label(
            container,
            text="Olivella",
            font=('Segoe UI', 32, 'bold'),
            bootstyle="primary"
        ).pack(pady=(0, 30))
        
        ttkb.Label(
            container,
            text="Sistema de Gestión Financiera",
            font=('Segoe UI', 12),
            bootstyle="secondary"
        ).pack(pady=(0, 40))
        
        # Botón de inicio
        ttkb.Button(
            container,
            text="Comenzar",
            bootstyle="success",
            padding=10,
            command=self.crear_interfaz_principal
        ).pack(pady=10, ipadx=20)
        
        # Configurar el grid para que el contenido se centre
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
    
    def crear_interfaz_principal(self):
        """Crear la interfaz principal después de la bienvenida"""
        self.frame_bienvenida.destroy()
        
        # Crear archivo Excel si no existe
        self.excel_path = Path("finanzas_hogar.xlsx")
        if not self.excel_path.exists():
            self.crear_archivo_excel()
        
        # Variables
        self.tipo = tk.StringVar()
        self.categoria = tk.StringVar()
        self.monto = tk.StringVar()
        self.descripcion = tk.StringVar()
        self.ahorro = tk.StringVar(value="$0.00")
        self.balance = tk.StringVar(value="$0.00")
        
        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Frame principal
        self.main_frame = ttkb.Frame(self.root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Configurar grid del frame principal
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Barra superior
        self.crear_barra_superior()
        
        # Contenido principal
        self.crear_contenido_principal()
        
        # Cargar datos iniciales
        self.cargar_datos()
        self.actualizar_grafica()
    
    def crear_barra_superior(self):
        """Crear la barra superior con el título y botones"""
        top_bar = ttkb.Frame(self.main_frame, bootstyle="light")
        top_bar.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        
        ttkb.Label(
            top_bar,
            text="Gestión Financiera",
            font=('Segoe UI', 14, 'bold'),
            bootstyle="inverse-light"
        ).pack(side='left', padx=10)
        
        ttkb.Button(
            top_bar,
            text="Actualizar",
            bootstyle="outline",
            command=self.cargar_datos
        ).pack(side='right', padx=5)
    
    def crear_contenido_principal(self):
        """Crear el contenido principal con formulario, resumen y gráfica"""
        # Contenedor principal
        content_frame = ttkb.Frame(self.main_frame)
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo - Formulario y resumen
        left_panel = ttkb.Frame(content_frame, padding=10)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Panel derecho - Gráfica
        right_panel = ttkb.Frame(content_frame, padding=10)
        right_panel.grid(row=0, column=1, sticky='nsew')
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        
        # Crear formulario
        self.crear_formulario(left_panel)
        
        # Crear resumen
        self.crear_resumen(left_panel)
        
        # Crear gráfica
        self.crear_grafica(right_panel)
    
    def crear_formulario(self, parent):
        """Crear el formulario para agregar transacciones"""
        form_frame = ttkb.Labelframe(
            parent,
            text="Nueva Transacción",
            bootstyle="info",
            padding=15
        )
        form_frame.pack(fill='x', pady=(0, 20))
        
        # Tipo de transacción
        ttkb.Label(form_frame, text="Tipo:").grid(row=0, column=0, sticky='w', pady=5)
        tipo_combo = ttkb.Combobox(
            form_frame,
            textvariable=self.tipo,
            values=["Ingreso", "Gasto", "Ahorro"],
            bootstyle="info",
            width=20
        )
        tipo_combo.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Categoría
        ttkb.Label(form_frame, text="Categoría:").grid(row=1, column=0, sticky='w', pady=5)
        self.combo_categoria = ttkb.Combobox(
            form_frame,
            textvariable=self.categoria,
            values=["Alimentos", "Transporte", "Vivienda", "Educación", "Salud", "Entretenimiento", "Otros", "Ahorro"],
            bootstyle="info",
            width=20
        )
        self.combo_categoria.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Monto
        ttkb.Label(form_frame, text="Monto:").grid(row=2, column=0, sticky='w', pady=5)
        ttkb.Entry(
            form_frame,
            textvariable=self.monto,
            bootstyle="info",
            width=23
        ).grid(row=2, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Descripción
        ttkb.Label(form_frame, text="Descripción:").grid(row=3, column=0, sticky='nw', pady=5)
        ttkb.Entry(
            form_frame,
            textvariable=self.descripcion,
            bootstyle="info",
            width=23
        ).grid(row=3, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Botón para agregar
        ttkb.Button(
            form_frame,
            text="Agregar Transacción",
            bootstyle="success",
            command=self.agregar_transaccion,
            width=20
        ).grid(row=4, column=0, columnspan=2, pady=(15, 5))
        
        # Configurar grid
        form_frame.grid_columnconfigure(1, weight=1)
    
    def crear_resumen(self, parent):
        """Crear el panel de resumen financiero"""
        resumen_frame = ttkb.Labelframe(
            parent,
            text="Resumen Financiero",
            bootstyle="success",
            padding=15
        )
        resumen_frame.pack(fill='x')
        
        # Balance Total
        ttkb.Label(resumen_frame, text="Balance Total:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        ttkb.Label(
            resumen_frame,
            textvariable=self.balance,
            font=('Segoe UI', 14, 'bold'),
            bootstyle="success"
        ).grid(row=0, column=1, sticky='e', pady=5, padx=10)
        
        # Ahorro
        ttkb.Label(resumen_frame, text="Ahorro:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        ttkb.Label(
            resumen_frame,
            textvariable=self.ahorro,
            font=('Segoe UI', 14, 'bold'),
            bootstyle="success"
        ).grid(row=1, column=1, sticky='e', pady=5, padx=10)
    def crear_grafica(self, parent):
        """Crear el panel de la gráfica de evolución"""
        self.grafica_frame = ttkb.Labelframe(
            parent,
            text="Evolución Mensual",
            bootstyle="info",
            padding=15
        )
        grafica_frame = self.grafica_frame  # Mantener compatibilidad con el código existente
        grafica_frame.grid(row=0, column=0, sticky='nsew')
        grafica_frame.grid_columnconfigure(0, weight=1)
        grafica_frame.grid_rowconfigure(1, weight=1)  # Cambiado para dar espacio a los controles
        
        # Frame para los controles de la gráfica
        controles_frame = ttkb.Frame(grafica_frame)
        controles_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        
        # Frame para el botón de tema
        frame_tema = ttkb.Frame(controles_frame)
        frame_tema.pack(side='right', padx=10)
        
        # Botón para cambiar el tema
        self.btn_tema = ttkb.Checkbutton(
            frame_tema,
            bootstyle="info-round-toggle",
            text="Tema Oscuro",
            command=self.cambiar_tema
        )
        self.btn_tema.pack(side='right')
        
        # Frame para los controles principales
        controles_principales = ttkb.Frame(controles_frame)
        controles_principales.pack(side='left', fill='x', expand=True)
        
        # Frame para los controles de período
        frame_periodo = ttkb.Frame(controles_principales)
        frame_periodo.pack(side='left', padx=5)
        
        # Etiqueta para el selector de período
        ttkb.Label(frame_periodo, text="Período:").pack(side='left', padx=(0, 5))
        
        # Selector de período
        periodo_combo = ttkb.Combobox(
            frame_periodo,
            textvariable=self.periodo_grafico,
            values=['Día', 'Semana', 'Mes'],
            state='readonly',
            width=10
        )
        periodo_combo.pack(side='left')
        
        # Frame para los botones de tipo de gráfico
        frame_tipo_grafico = ttkb.Frame(controles_principales)
        frame_tipo_grafico.pack(side='left', padx=20)
        
        # Botones para cambiar el tipo de gráfico
        ttkb.Label(frame_tipo_grafico, text="Tipo:").pack(side='left', padx=(0, 5))
        
        # Botón para gráfico de líneas
        btn_linea = ttkb.Radiobutton(
            frame_tipo_grafico,
            text="Líneas",
            variable=self.tipo_grafico,
            value="linea",
            command=self.actualizar_grafica,
            bootstyle="info-toolbutton"
        )
        btn_linea.pack(side='left', padx=2)
        
        # Botón para gráfico de barras
        btn_barras = ttkb.Radiobutton(
            frame_tipo_grafico,
            text="Barras",
            variable=self.tipo_grafico,
            value="barras",
            command=self.actualizar_grafica,
            bootstyle="info-toolbutton"
        )
        btn_barras.pack(side='left', padx=2)
        
        # Botón para gráfico de área
        btn_area = ttkb.Radiobutton(
            frame_tipo_grafico,
            text="Área",
            variable=self.tipo_grafico,
            value="area",
            command=self.actualizar_grafica,
            bootstyle="info-toolbutton"
        )
        btn_area.pack(side='left', padx=2)
        
        # Vincular el evento de cambio del período
        periodo_combo.bind('<<ComboboxSelected>>', lambda e: self.actualizar_grafica())
        
        # Configurar el título inicial
        self.grafica_frame = grafica_frame
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Configurar estilo de la gráfica
        self.fig.patch.set_facecolor('#f8f9fa')
        self.ax.set_facecolor('#f8f9fa')
        
        # Configurar el grid
        self.ax.grid(True, linestyle='--', alpha=0.6)
        
        # Formatear el eje Y como moneda
        def formato_moneda(y, pos):
            return f'${y:,.0f}'
        
        self.ax.yaxis.set_major_formatter(FuncFormatter(formato_moneda))
        
        # Crear canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=grafica_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew')
        
        # Configurar el tooltip
        self.fig.tight_layout()
    
    def crear_panel_grafica(self):
        """Crear el panel de gráfica"""
        # Frame para la gráfica
        grafica_frame = ttkb.LabelFrame(
            self.frame_principal,
            text="Gráfica de Evolución",
            padding=10
        )
        grafica_frame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        grafica_frame.grid_columnconfigure(0, weight=1)
        grafica_frame.grid_rowconfigure(1, weight=1)
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Configurar estilo de la gráfica
        self.fig.patch.set_facecolor('#f8f9fa')
        self.ax.set_facecolor('#f8f9fa')
        
        # Configurar el grid
        self.ax.grid(True, linestyle='--', alpha=0.6)
        
        # Formatear el eje Y como moneda
        def formato_moneda(y, pos):
            return f'${y:,.0f}'
        
        self.ax.yaxis.set_major_formatter(FuncFormatter(formato_moneda))
        
        # Crear canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=grafica_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew')
        
        # Configurar el tooltip
        self.fig.tight_layout()

    def cambiar_tema(self):
        """Cambiar entre tema claro y oscuro"""
        self.tema_oscuro = not self.tema_oscuro
        
        if self.tema_oscuro:
            self.style.theme_use('darkly')
            self.btn_tema.config(text="Tema Claro")
        else:
            self.style.theme_use('minty')
            self.btn_tema.config(text="Tema Oscuro")
        
        # Actualizar la gráfica para reflejar el nuevo tema
        self.actualizar_grafica()

    def actualizar_grafica(self):
        """Actualizar la gráfica con los datos actuales según el período seleccionado"""
        try:
            # Leer el archivo Excel
            df = pd.read_excel(self.excel_path)
            
            if df.empty:
                return
            
            # Convertir fecha a datetime
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df = df.sort_values('Fecha')
            
            # Obtener el período seleccionado y actualizar título
            periodo_mostrar = self.periodo_grafico.get()
            periodo = self.periodo_valores.get(periodo_mostrar, 'mes')
            
            # Actualizar el título del frame del gráfico
            if hasattr(self, 'grafica_frame'):
                self.grafica_frame.config(text=f"Evolución {periodo_mostrar}")
            
            # Configurar colores según el tema
            color_fondo = '#2d2d2d' if self.tema_oscuro else '#f8f9fa'
            color_ejes = '#ffffff' if self.tema_oscuro else '#000000'
            color_grid = '#404040' if self.tema_oscuro else '#e0e0e0'
            colores = {
                'Ingreso': '#2ecc71',  # Verde
                'Gasto': '#e74c3c',     # Rojo
                'Ahorro': '#3498db'     # Azul
            }
            
            # Agrupar datos según el período seleccionado
            if periodo == 'dia':
                # Agrupar por día
                df_agrupado = df.groupby(['Fecha', 'Tipo'])['Monto'].sum().unstack(fill_value=0)
                formato_fecha = '%d/%m/%Y'
                titulo = f'Evolución Diaria - {periodo_mostrar}'
            elif periodo == 'semana':
                # Agrupar por semana
                df_semana = df.copy()
                df_semana['Semana'] = df_semana['Fecha'].dt.to_period('W').dt.start_time
                df_agrupado = df_semana.groupby(['Semana', 'Tipo'])['Monto'].sum().unstack(fill_value=0)
                formato_fecha = '%d/%m/%Y'
                titulo = f'Evolución Semanal - {periodo_mostrar}'
            else:  # mes por defecto
                # Agrupar por mes
                df_mes = df.copy()
                df_mes['Mes'] = df_mes['Fecha'].dt.to_period('M').dt.to_timestamp()
                df_agrupado = df_mes.groupby(['Mes', 'Tipo'])['Monto'].sum().unstack(fill_value=0)
                formato_fecha = '%b %Y'
                titulo = f'Evolución Mensual - {periodo_mostrar}'
            
            # Limpiar gráfica
            self.ax.clear()
            
            # Aplicar colores al gráfico
            self.fig.patch.set_facecolor(color_fondo)
            self.ax.set_facecolor(color_fondo)
            self.ax.tick_params(colors=color_ejes)
            self.ax.xaxis.label.set_color(color_ejes)
            self.ax.yaxis.label.set_color(color_ejes)
            self.ax.title.set_color(color_ejes)
            self.ax.spines['bottom'].set_color(color_ejes)
            self.ax.spines['top'].set_color(color_ejes)
            self.ax.spines['left'].set_color(color_ejes)
            self.ax.spines['right'].set_color(color_ejes)
            self.ax.grid(True, linestyle='--', alpha=0.6, color=color_grid)
            
            # Obtener el tipo de gráfico seleccionado
            tipo_grafico = self.tipo_grafico.get()
            
            # Dibujar según el tipo de gráfico seleccionado
            for tipo in ['Ingreso', 'Gasto', 'Ahorro']:
                if tipo in df_agrupado.columns:
                    color = colores.get(tipo, '#95a5a6')
                    
                    if tipo_grafico == 'barras':
                        # Gráfico de barras
                        self.ax.bar(
                            df_agrupado.index,
                            df_agrupado[tipo],
                            label=tipo,
                            color=color,
                            alpha=0.7,
                            width=0.25 if len(df_agrupado) > 1 else 0.4
                        )
                    elif tipo_grafico == 'area':
                        # Gráfico de área
                        self.ax.fill_between(
                            df_agrupado.index,
                            df_agrupado[tipo],
                            label=tipo,
                            color=color,
                            alpha=0.3,
                            linewidth=2
                        )
                    else:  # Gráfico de líneas (por defecto)
                        # Gráfico de líneas con marcadores
                        self.ax.plot(
                            df_agrupado.index,
                            df_agrupado[tipo],
                            label=tipo,
                            color=color,
                            marker='o',
                            linestyle='-',
                            linewidth=2,
                            markersize=6
                        )
            
            # Configurar etiquetas y formato
            self.ax.set_title(titulo, fontsize=12, fontweight='bold', pad=15, color=color_ejes)
            self.ax.set_xlabel('Fecha', fontsize=10, labelpad=10, color=color_ejes)
            self.ax.set_ylabel('Monto', fontsize=10, labelpad=10, color=color_ejes)
            
            # Formatear el eje X con fechas
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter(formato_fecha))
            self.ax.tick_params(axis='x', rotation=45, colors=color_ejes)
            self.ax.tick_params(axis='y', colors=color_ejes)
            
            # Formatear el eje Y como moneda
            def formato_moneda(y, pos):
                return f'${y:,.0f}'
            
            self.ax.yaxis.set_major_formatter(FuncFormatter(formato_moneda))
            
            # Configurar leyenda
            legend = self.ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
            
            # Ajustar márgenes
            self.fig.subplots_adjust(bottom=0.2)
            
            # Ajustar diseño
            self.fig.tight_layout()
            
            # Actualizar canvas
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error al actualizar gráfica: {e}")

    def cargar_datos(self):
        """Cargar datos del Excel y actualizar la vista"""
        try:
            # Leer datos del Excel
            df = pd.read_excel(self.excel_path)
            
            # Limpiar treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar datos en el treeview
            for _, row in df.iterrows():
                self.tree.insert('', 'end', values=(
                    row['Fecha'],
                    row['Tipo'],
                    row['Categoria'],
                    f"${row['Monto']:.2f}",
                    row['Descripción']
                ))
            
            # Actualizar balance
            self.actualizar_balance()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}")

if __name__ == "__main__":
    try:
        root = ttkb.Window(themename="superhero")  # Tema más robusto
        app = AplicacionFinanzas(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        print("Detalles del error:", traceback.format_exc())
