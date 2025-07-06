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
    '--collect-data=tkinter',  # Incluir todos los datos de tkinter
    '--collect-data=ttkbootstrap',  # Incluir todos los datos de ttkbootstrap
    '--collect-data=matplotlib',  # Incluir todos los datos de matplotlib
    '--collect-data=pandas',  # Incluir todos los datos de pandas
    '--collect-data=numpy',  # Incluir todos los datos de numpy
    '--collect-data=openpyxl',  # Incluir todos los datos de openpyxl
    '--collect-data=python_dateutil',  # Incluir todos los datos de dateutil
    '--collect-data=tcl',  # Incluir todos los datos de tcl
    '--collect-data=tk',  # Incluir todos los datos de tk
    '--collect-data=tcl8',  # Incluir todos los datos de tcl8
    '--collect-data=tk8.6',  # Incluir todos los datos de tk8.6
    '--clean',
    '--distpath', output_dir,  # Especificar carpeta de salida
    '--noconfirm',  # No preguntar por confirmación
])
