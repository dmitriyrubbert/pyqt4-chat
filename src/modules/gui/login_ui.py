# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Sat Jan 23 13:26:07 2016
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
        Dialog.resize(337, 101)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEditPass = QtGui.QLineEdit(Dialog)
        self.lineEditPass.setObjectName(_fromUtf8("lineEditPass"))
        self.gridLayout.addWidget(self.lineEditPass, 1, 1, 1, 1)
        self.comboBoxLogin = QtGui.QComboBox(Dialog)
        self.comboBoxLogin.setEditable(True)
        self.comboBoxLogin.setObjectName(_fromUtf8("comboBoxLogin"))
        self.gridLayout.addWidget(self.comboBoxLogin, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(84, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.label.setBuddy(self.comboBoxLogin)
        self.label_2.setBuddy(self.lineEditPass)

        self.retranslateUi(Dialog)
        self.comboBoxLogin.setCurrentIndex(-1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.checkNetwork)
        QtCore.QObject.connect(self.comboBoxLogin, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), Dialog.on_index_changed)
        QtCore.QObject.connect(self.comboBoxLogin, QtCore.SIGNAL(_fromUtf8("editTextChanged(QString)")), Dialog.on_text_changed)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.comboBoxLogin, self.lineEditPass)
        Dialog.setTabOrder(self.lineEditPass, self.checkBox)
        Dialog.setTabOrder(self.checkBox, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Авторизация www.bridge-of-love.com", None))
        self.label.setText(_translate("Dialog", "&Логин:", None))
        self.checkBox.setToolTip(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Запомнить учетные данные</span></p></body></html>", None))
        self.checkBox.setText(_translate("Dialog", "&Запомнить", None))
        self.label_2.setText(_translate("Dialog", "&Пароль:", None))
        self.lineEditPass.setToolTip(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Пароль</span></p></body></html>", None))
        self.comboBoxLogin.setToolTip(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Ваш логин от сайта www.bridge-of-love.com</span></p></body></html>", None))

import resource_rc
