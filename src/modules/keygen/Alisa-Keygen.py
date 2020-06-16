# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui

if __name__ == "__main__":
    from keygen import KeyGen
    app = QtGui.QApplication(sys.argv)
    w = KeyGen()
    w.setWindowTitle('Alisa KeyGen')
    w.show()
    w.main()
    sys.exit(app.exec_())
