# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:\\Users\\Administrator\\Desktop\\side_project\\路由重启\\python-version\\0_2\\route_rebootor0.2.py'],
             pathex=['C:\\Users\\Administrator\\Desktop\\side_project\\路由重启\\python-version\\0_2'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='route_rebootor0.2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='C:\\Users\\Administrator\\Desktop\\side_project\\路由重启\\resource\\20201217080538460_easyicon_net_128.ico')
