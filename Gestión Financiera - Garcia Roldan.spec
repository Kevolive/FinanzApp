# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('estilos.py', '.'), ('finanzas_hogar.xlsx', '.')]
datas += collect_data_files('tkinter')
datas += collect_data_files('ttkbootstrap')
datas += collect_data_files('matplotlib')
datas += collect_data_files('pandas')
datas += collect_data_files('numpy')
datas += collect_data_files('openpyxl')
datas += collect_data_files('python_dateutil')
datas += collect_data_files('tcl')
datas += collect_data_files('tk')
datas += collect_data_files('tcl8')
datas += collect_data_files('tk8.6')


a = Analysis(
    ['app_finanzas.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Gestión Financiera - Garcia Roldan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
