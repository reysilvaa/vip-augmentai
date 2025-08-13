# PyInstaller spec file for Augment VIP MVC GUI
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Add src to Python path
src_path = Path('src')
sys.path.insert(0, str(src_path))

block_cipher = None

a = Analysis(
    ['main_mvc.py'],
    pathex=['.', 'src'],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'src.core.application',
        'src.views.main_window',
        'src.views.style_manager',
        'src.controllers.main_controller',
        'src.models.vscode_model',
        'src.models.database_model',
        'src.models.telemetry_model',
        'src.services.vscode_service',
        'src.services.file_service',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'augment_vip',  # Exclude old package
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AugmentVIP_MVC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for windowed app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
