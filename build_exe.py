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
    '--hidden-import=ttkbootstrap',  # Incluir ttkbootstrap
    '--clean',
    '--distpath', output_dir,  # Especificar carpeta de salida
    '--noconfirm'  # No preguntar por confirmación
])
