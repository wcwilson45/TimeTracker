# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app\\MainPage.py'],
    pathex=[],
    binaries=[],
    datas=[('app/ui', 'app/ui'), ('app/ui/Databases', 'app/ui/Databases'), ('app/image.png', 'app/')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.font', 'sqlite3', 'datetime', 'pathlib', 'csv', 'threading', 're', 'shutil', 'matplotlib', 'matplotlib.figure', 'matplotlib.backends.backend_tkagg', 'typing'],
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
    [],
    exclude_binaries=True,
    name='TimeTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\elamb\\OneDrive\\Desktop\\Software Engineering Project\\TimeTracker\\app\\image.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TimeTracker',
)
