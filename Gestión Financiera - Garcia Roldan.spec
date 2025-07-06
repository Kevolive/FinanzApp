# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app_finanzas.py'],
    pathex=[],
    binaries=[],
    datas=[('estilos.py', '.'), ('finanzas_hogar.xlsx', '.')],
    hiddenimports=['ttkbootstrap', 'ttkbootstrap.themes', 'ttkbootstrap.icons', 'matplotlib', 'matplotlib.backends.backend_tkagg', 'matplotlib.figure', 'matplotlib.axes', 'matplotlib.pyplot', 'matplotlib.ticker', 'matplotlib.dates', 'matplotlib.font_manager', 'matplotlib.style', 'pandas', 'numpy', 'openpyxl', 'python_dateutil', 'python_dateutil.tz', 'python_dateutil.parser', 'python_dateutil.relativedelta', 'python_dateutil.rrule', 'python_dateutil.easter', 'python_dateutil.tzwin', 'python_dateutil.zoneinfo'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', '_tkinter', 'tcl', 'tk'],
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
