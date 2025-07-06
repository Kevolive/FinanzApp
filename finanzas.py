import tkinter as tk
from tkinter import ttk, messagebox, font
import pandas as pd
import datetime
from pathlib import Path
import sys
import os
import estilos

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class AplicacionFinanzas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Financiera Hogar - Garcia Roldan")
        self.root.geometry("800x600")
        
        # Configurar estilos
        self.estilo = estilos.configurar_estilos(root)
        
        # Mostrar pantalla de bienvenida
        self.mostrar_bienvenida()
        
    def mostrar_bienvenida(self):
        """Mostrar pantalla de bienvenida"""
        # Crear frame principal con padding
        self.frame_bienvenida = ttk.Frame(self.root, padding="20")
        self.frame_bienvenida.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear frame interno para centrar contenido
        frame_central = ttk.Frame(self.frame_bienvenida)
        frame_central.grid(row=0, column=0)
        
        # Configurar fuente grande
        fuente_grande = font.Font(size=24, weight="bold")
        
        # Mensaje de bienvenida
        ttk.Label(frame_central, text="Bienvenidos", style="Bienvenida.TLabel").pack(pady=20)
        ttk.Label(frame_central, text="Garcia Roldan", style="Bienvenida.TLabel").pack(pady=20)
        
        # Mensaje de uso
        ttk.Label(frame_central, text="Aplicación de Gestión Financiera", style="Subtitulo.TLabel").pack(pady=10)
        ttk.Label(frame_central, text="Para registrar ingresos, gastos y ahorros del hogar").pack(pady=10)
        
        # Botón para continuar
        ttk.Button(frame_central, text="Comenzar", style="Bienvenida.TButton", command=self.crear_interfaz_principal).pack(pady=20)
        
        # Configurar el grid para que el contenido se centre
        self.frame_bienvenida.grid_columnconfigure(0, weight=1)
        self.frame_bienvenida.grid_rowconfigure(0, weight=1)
        
        # Configurar el root para que se expanda correctamente
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
        self.ahorro = tk.StringVar(value="0")
        self.balance = tk.StringVar(value="0")
        
        # Crear widgets
        self.crear_widgets()
        
        # Cargar balance inicial
        self.actualizar_balance()
        
    def crear_archivo_excel(self):
        """Crear el archivo Excel con las columnas necesarias"""
        columnas = ['Fecha', 'Tipo', 'Categoria', 'Monto', 'Descripción']
        df = pd.DataFrame(columns=columnas)
        df.to_excel(self.excel_path, index=False)
    
    def crear_widgets(self):
        """Crear todos los elementos de la interfaz"""
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="10")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame para entrada de datos
        frame_entrada = ttk.LabelFrame(frame_principal, text="Ingresar Transacción", padding="15", style="TLabelframe")
        frame_entrada.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Tipo de transacción
        ttk.Label(frame_entrada, text="Tipo:").grid(row=0, column=0, sticky=tk.W)
        self.combo_tipo = ttk.Combobox(frame_entrada, textvariable=self.tipo, values=["Ingreso", "Gasto", "Ahorro"])
        self.combo_tipo.grid(row=0, column=1, padx=5, pady=5)
        
        # Categoría
        ttk.Label(frame_entrada, text="Categoría:").grid(row=1, column=0, sticky=tk.W)
        self.combo_categoria = ttk.Combobox(frame_entrada, textvariable=self.categoria, values=["Alimentos", "Transporte", "Vivienda", "Educación", "Salud", "Entretenimiento", "Otros", "Ahorro"])
        self.combo_categoria.grid(row=1, column=1, padx=5, pady=5)
        
        # Monto
        ttk.Label(frame_entrada, text="Monto:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(frame_entrada, textvariable=self.monto).grid(row=2, column=1, padx=5, pady=5)
        
        # Descripción
        ttk.Label(frame_entrada, text="Descripción:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(frame_entrada, textvariable=self.descripcion).grid(row=3, column=1, padx=5, pady=5)
        
        # Botón Agregar
        ttk.Button(frame_entrada, text="Agregar Transacción", command=self.agregar_transaccion).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Frame para mostrar resumen
        frame_resumen = ttk.LabelFrame(frame_principal, text="Resumen Mensual", padding="15", style="TLabelframe")
        frame_resumen.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Frame para mostrar balance
        frame_balance = ttk.LabelFrame(frame_resumen, text="Balance Actual", padding="10", style="TLabelframe")
        frame_balance.grid(row=0, column=0, padx=5, pady=10, sticky=(tk.W, tk.E))
        
        # Mostrar balance
        ttk.Label(frame_balance, text="Balance Total:", style="TLabel").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(frame_balance, textvariable=self.balance, style="Exito.TLabel").grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame_balance, text="Ahorro:", style="TLabel").grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(frame_balance, textvariable=self.ahorro, style="Exito.TLabel").grid(row=1, column=1, padx=10, pady=5)
        
        # Treeview para mostrar datos
        self.tree = ttk.Treeview(frame_resumen, columns=('Fecha', 'Tipo', 'Categoria', 'Monto', 'Descripción'), show='headings')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Categoria', text='Categoría')
        self.tree.heading('Monto', text='Monto')
        self.tree.heading('Descripción', text='Descripción')
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_resumen, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Botón para actualizar vista
        ttk.Button(frame_resumen, text="Actualizar Vista", style="TButton").grid(row=2, column=0, pady=10)
        
        # Cargar datos iniciales
        self.cargar_datos()
    
    def agregar_transaccion(self):
        """Agregar una nueva transacción al Excel"""
        try:
            monto = float(self.monto.get())
            if not self.tipo.get() or not self.categoria.get() or not self.descripcion.get():
                raise ValueError("Todos los campos son requeridos")
                
            # Leer el archivo existente
            df = pd.read_excel(self.excel_path)
            
            # Crear nueva fila como DataFrame
            nueva_fila = pd.DataFrame({
                'Fecha': [datetime.datetime.now().strftime('%Y-%m-%d')],
                'Tipo': [self.tipo.get()],
                'Categoria': [self.categoria.get()],
                'Monto': [monto],
                'Descripción': [self.descripcion.get()]
            })
            
            # Concatenar los DataFrames
            df = pd.concat([df, nueva_fila], ignore_index=True)
            
            # Guardar cambios
            df.to_excel(self.excel_path, index=False)
            
            # Limpiar campos
            self.tipo.set("")
            self.categoria.set("")
            self.monto.set("")
            self.descripcion.set("")
            
            # Actualizar vista y balance
            self.cargar_datos()
            self.actualizar_balance()
            
            messagebox.showinfo("Éxito", "Transacción agregada correctamente")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def actualizar_balance(self):
        """Actualizar el balance total y el ahorro"""
        try:
            df = pd.read_excel(self.excel_path)
            
            # Calcular ingresos
            ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
            
            # Calcular gastos
            gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
            
            # Calcular ahorro
            ahorro = df[df['Tipo'] == 'Ahorro']['Monto'].sum()
            
            # Calcular balance total
            balance = ingresos - gastos
            
            # Actualizar variables
            self.balance.set(f"${balance:.2f}")
            self.ahorro.set(f"${ahorro:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el balance: {str(e)}")
    
    def cargar_datos(self):
        """Cargar datos del Excel y mostrarlos en la tabla"""
        try:
            df = pd.read_excel(self.excel_path)
            
            # Limpiar la tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar datos
            for index, row in df.iterrows():
                self.tree.insert("", "end", values=(row['Fecha'], row['Tipo'], row['Categoria'], f"{row['Monto']:.2f}", row['Descripción']))
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los datos: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionFinanzas(root)
    root.mainloop()
