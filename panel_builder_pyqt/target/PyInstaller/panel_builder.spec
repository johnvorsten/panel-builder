# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\z003vrzk\\.spyder-py3\\Scripts\\Work\\PanelBuilder\\panel_builder_pyqt\\src\\main\\python\\main.py'],
             pathex=['C:\\Users\\z003vrzk\\.spyder-py3\\Scripts\\Work\\PanelBuilder\\panel_builder_pyqt\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['c:\\programdata\\anaconda3\\envs\\pyqt\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['C:\\Users\\z003vrzk\\.spyder-py3\\Scripts\\Work\\PanelBuilder\\panel_builder_pyqt\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='panel_builder',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='C:\\Users\\z003vrzk\\.spyder-py3\\Scripts\\Work\\PanelBuilder\\panel_builder_pyqt\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='panel_builder')
