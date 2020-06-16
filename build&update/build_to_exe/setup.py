# -*- coding: utf-8 -*-
# Создание исполняемого файла
# http://cx-freeze.readthedocs.org/en/latest/distutils.html#distutils-commands

import sys
from cx_Freeze import setup, Executable
from modules.logic.main import __version__

DEBUG = False

packages = ["modules.config", "modules.gui", "modules.logic", "modules.script"]

includes = ["atexit", "os", "weblib", "selection", "curl", "grab", "grab.transport",
            "grab.transport.curl", "grab.spider", "grab.spider.queue_backend",
            "grab.spider.queue_backend.memory", "csv", "cookielib",
            "lxml.etree", "lxml._elementpath", "logging.handlers", "SocketServer", "SimpleHTTPServer"]

# zip_includes = [("C:\\Python27\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\", "imageformats")]
# bin_includes = ["os"]

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
                     "packages": packages,
                     "optimize": 2,
                     "include_msvcr": True,
                     "includes": includes,
                     "excludes": ["Tkinter", "Tk","Tcl", "PyQt4.QtSql", "sqlite3", 
                                  "scipy.lib.lapack.flapack",
                                  "PyQt4.QtNetwork",
                                  "PyQt4.QtScript",
                                  "numpy.core._dotblas", 
                                  "PyQt5"],
                     # "zip_includes": zip_includes,
                     # "bin_includes": bin_includes
                     }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if not DEBUG:
    if sys.platform == "win32":
        base = "Win32GUI"

setup(
    name="Alisa-Sender",
    version=__version__,
    description=u"Чат бот для сайта www.bridge-of-love.com",
    options={"build_exe": build_exe_options},
    executables=[Executable("Alisa-Sender.py", base=base, icon="res/appicon.ico")]
)
