# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import platform

# 收集所有必要的依赖
datas = []
binaries = []
hiddenimports = []

# 收集keyboard模块的所有依赖
tmp_ret = collect_all('keyboard')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# 收集PyQt6的所有依赖
pyqt6_modules = ['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets']
for module in pyqt6_modules:
    try:
        tmp_ret = collect_all(module)
        datas += tmp_ret[0]
        binaries += tmp_ret[1]
        hiddenimports += tmp_ret[2]
    except:
        pass

# 添加隐藏导入（Mac版本，移除Windows特定的）
hiddenimports += [
    'mouse_trail',
    'control_panel',
    'keyboard',
    'keyboard._nixcommon',
    'keyboard._darwinmouse',  # Mac特定的
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# 创建可执行文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='轨迹精灵',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Mac上通常不使用UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Mac上创建.app bundle
app = BUNDLE(
    exe,
    name='轨迹精灵.app',
    icon=None,
    bundle_identifier='com.trailsprite.app',
    version='1.0.0',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'NSRequiresAquaSystemAppearance': 'False',
        'LSMinimumSystemVersion': '10.13',
        'NSHumanReadableCopyright': 'Copyright © 2024',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
    },
)
