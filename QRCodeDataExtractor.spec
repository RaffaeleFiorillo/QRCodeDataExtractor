# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all submodules and data files for scipy and other dependencies
hidden_imports = collect_submodules('scipy')
datas = collect_data_files('scipy')

hidden_imports += collect_submodules('numpy')
datas += collect_data_files('numpy')

hidden_imports += collect_submodules('pyzbar')
datas += collect_data_files('pyzbar')

# Add additional necessary hidden imports
hidden_imports += ['scipy._lib.array_api_compat.numpy.fft', 'scipy.ndimage._filters', 'scipy._lib._util', 'scipy._lib._array_api']

block_cipher = None

a = Analysis(
    ['QRCodeDataExtractor.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='QRCodeDataExtractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='report.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QRCodeDataExtractor',
    icon='report.ico'  
)
