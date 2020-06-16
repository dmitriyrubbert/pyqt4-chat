from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Alisa.py', base=base)
]

setup(name='Alisa',
      version = '2.0',
      description = 'Simple chat bot',
      options = dict(build_exe = buildOptions),
      executables = executables)
