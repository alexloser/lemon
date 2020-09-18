# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(['rename2.py'],
             pathex=['D:\\_CVProto'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=["tkinter", "lib2to3", "xml", "bz2", "lzma", "unicodedata", "ctypes", "select", 
                       "socket", "decimal", "overlapped", "testcapi", "asyncio", "ssl", "Include",],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='rename2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
