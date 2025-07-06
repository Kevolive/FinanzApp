import PyInstaller.__main__
import os

# Asegurarse de que la carpeta de salida existe
output_dir = 'dist'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

PyInstaller.__main__.run([
    'app_finanzas.py',  # Archivo principal actualizado
    '--onefile',
    '--windowed',
    '--name=Gestión Financiera - Garcia Roldan',
    '--add-data=estilos.py;.',  # Incluir archivo de estilos
    '--add-data=finanzas_hogar.xlsx;.',  # Incluir archivo Excel
    '--hidden-import=ttkbootstrap',  # Incluir ttkbootstrap
    '--hidden-import=ttkbootstrap.themes',  # Incluir temas de ttkbootstrap
    '--hidden-import=ttkbootstrap.icons',  # Incluir íconos de ttkbootstrap
    '--hidden-import=matplotlib',  # Incluir matplotlib
    '--hidden-import=matplotlib.backends.backend_tkagg',  # Backend de TkAgg
    '--hidden-import=matplotlib.figure',  # Módulo de figure
    '--hidden-import=matplotlib.axes',  # Módulo de axes
    '--hidden-import=matplotlib.pyplot',  # Módulo pyplot
    '--hidden-import=matplotlib.ticker',  # Módulo ticker
    '--hidden-import=matplotlib.dates',  # Módulo dates
    '--hidden-import=matplotlib.font_manager',  # Módulo font_manager
    '--hidden-import=matplotlib.style',  # Módulo style
    '--hidden-import=pandas',  # Incluir pandas
    '--hidden-import=numpy',  # Incluir numpy
    '--hidden-import=openpyxl',  # Incluir openpyxl
    '--hidden-import=python_dateutil',  # Incluir dateutil
    '--hidden-import=python_dateutil.tz',  # Incluir dateutil.tz
    '--hidden-import=python_dateutil.parser',  # Incluir dateutil.parser
    '--hidden-import=python_dateutil.relativedelta',  # Incluir dateutil.relativedelta
    '--hidden-import=python_dateutil.rrule',  # Incluir dateutil.rrule
    '--hidden-import=python_dateutil.easter',  # Incluir dateutil.easter
    '--hidden-import=python_dateutil.tzwin',  # Incluir dateutil.tzwin
    '--hidden-import=python_dateutil.zoneinfo',  # Incluir dateutil.zoneinfo
    '--clean',
    '--distpath', output_dir,  # Especificar carpeta de salida
    '--noconfirm',  # No preguntar por confirmación
    '--exclude-module=tkinter',  # Excluir tkinter ya que viene con Python
    '--exclude-module=_tkinter',  # Excluir _tkinter ya que viene con Python
    '--exclude-module=tcl',  # Excluir tcl ya que viene con Python
    '--exclude-module=tk',  # Excluir tk ya que viene con Python
])
