# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'keygen.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(317, 101)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_login = QtGui.QLineEdit(Dialog)
        self.lineEdit_login.setText(_fromUtf8(""))
        self.lineEdit_login.setObjectName(_fromUtf8("lineEdit_login"))
        self.gridLayout.addWidget(self.lineEdit_login, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_key = QtGui.QLineEdit(Dialog)
        self.lineEdit_key.setText(_fromUtf8(""))
        self.lineEdit_key.setObjectName(_fromUtf8("lineEdit_key"))
        self.gridLayout.addWidget(self.lineEdit_key, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(84, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_2.addWidget(self.pushButton, 1, 2, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setDefault(True)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.label.setBuddy(self.lineEdit_login)
        self.label_2.setBuddy(self.lineEdit_key)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.reject)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.genKey)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEdit_login, self.lineEdit_key)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "&Логин:", None))
        self.label_2.setText(_translate("Dialog", "&Ключ:", None))
        self.pushButton.setText(_translate("Dialog", "QUIT", None))
        self.pushButton_2.setText(_translate("Dialog", "GENERATE", None))

