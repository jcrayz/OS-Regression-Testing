# -*- mode: python -*-
"""regrOS freezing script.
Execute from repossitory root."""

import os
import flask_migrate
import flask_admin

flask_migrate_package = os.path.dirname(flask_migrate.__file__)
flask_admin_package = os.path.dirname(flask_admin.__file__)

block_cipher = None

webapp_path = os.path.join('allamericanregress','webapp')

templates_path = os.path.join(webapp_path,'templates')
statics_path = os.path.join(webapp_path,'static')
datas  = [
  (flask_migrate_package,'flask_migrate'),
  (flask_admin_package,'flask_admin'),
  (templates_path,'templates'),
  (statics_path,'static'),
]
a = Analysis([os.path.join('allamericanregress','__main__.py')],
             pathex=[os.getcwd()],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='regros',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='regros')
