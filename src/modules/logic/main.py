# -*- coding: utf-8 -*-
import sys
import os
from PyQt4 import QtGui, QtCore
import logging
from logging.handlers import TimedRotatingFileHandler
from modules.logic.base import MainWindow
from modules.logic.login import LoginForm
from modules.logic.activate import ActivateForm

__version__ = '2'
DEBUG = False
LOGLEVEL = logging.DEBUG
 # CRITICAL
 # ERROR
 # WARNING

def main():

    if not os.path.exists('./log'):
        os.makedirs('./log')

    logger = logging.getLogger()
    logger.setLevel(LOGLEVEL)

    handler = TimedRotatingFileHandler('./log/alisa.log', when='d', interval=1, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Alisa-Sender')
    app.setApplicationVersion(__version__)
    app.addLibraryPath('imageformats')
    app.addLibraryPath(os.path.join(os.path.dirname(QtCore.__file__), "imageformats"))

    login_window = LoginForm(debug=DEBUG)
    if login_window.exec_() == QtGui.QDialog.Accepted and login_window.isAuthorized:
        print('Accepted & isAuthorized')
        activate_window = ActivateForm(login_window.login, debug=DEBUG)
        if activate_window.openKeys() and activate_window.isActivated:
            window = MainWindow(login_window.login, login_window.password,
                                login_window.pics, debug=DEBUG)
            window.show()
            sys.exit(app.exec_())
        else:
            sys.exit(activate_window.exec_())
    else:
        print('NOT Accepted & isAuthorized')

    ###################################3
    # window = MainWindow('elona1205@gmail.com', 'aO0nY3',
    #                             [], debug=DEBUG)
    # window.show()
    # sys.exit(app.exec_())

# 23/10/17 ---------------------------------------------

    # window = MainWindow(debug=DEBUG)
    # window.show()
    # sys.exit(app.exec_())
