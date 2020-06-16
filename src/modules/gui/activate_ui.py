# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'activate.ui'
#
# Created: Sat Jan 23 13:26:06 2016
#      by: PyQt4 UI code generator 4.10.4
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
        Dialog.resize(268, 450)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelKyle = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.labelKyle.sizePolicy().hasHeightForWidth())
        self.labelKyle.setSizePolicy(sizePolicy)
        self.labelKyle.setMinimumSize(QtCore.QSize(250, 303))
        self.labelKyle.setMaximumSize(QtCore.QSize(250, 303))
        self.labelKyle.setText(_fromUtf8(""))
        self.labelKyle.setPixmap(QtGui.QPixmap(_fromUtf8(":/res/Craig.gif")))
        self.labelKyle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelKyle.setObjectName(_fromUtf8("labelKyle"))
        self.verticalLayout.addWidget(self.labelKyle)
        self.label = QtGui.QLabel(Dialog)
        self.label.setWordWrap(True)
        self.label.setMargin(10)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.lineEdit_key = QtGui.QLineEdit(Dialog)
        self.lineEdit_key.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit_key.setObjectName(_fromUtf8("lineEdit_key"))
        self.verticalLayout.addWidget(self.lineEdit_key)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.lineEdit_key)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.checkActivation)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Ввод ключа активации", None))
        self.label.setText(_translate("Dialog", "Кенни говорит Вам ПРИВЕТ! Будь внимательней при вводе ключа активации!", None))

import resource_rc
