# -*- coding: utf-8 -*-

import sys
import time
import hashlib
from PyQt4 import QtGui, QtCore
from grab import Grab
from keygen_ui import Ui_Dialog
try:
    from PyQt4.phonon import Phonon
except Exception, e:
    pass

class KeyGen(QtGui.QDialog, Ui_Dialog):

    """ Генератор ключей активации """

    def __init__(self, parent=None):
        super(KeyGen, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('appicon.ico'))

    def prepare(self):
        """ Play Sound """

        self.mediaObject = Phonon.MediaObject(self)
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.mediaObject, self.audioOutput)
        self.mediaObject.setCurrentSource(Phonon.MediaSource('http://sysadmin.1cps.ru/alisa/keygen.mp3'))
        self.mediaObject.play()
        # loop
        self.mediaObject.aboutToFinish.connect(self.enqueFile)
        self.mediaObject.setPrefinishMark(0)
        self.mediaObject.setTransitionTime(0)

    def enqueFile(self):
        self.mediaObject.enqueue(Phonon.MediaSource('http://sysadmin.1cps.ru/alisa/keygen.mp3'))

    def genKey(self):
        # try:
        self.login = self.lineEdit_login.text()
        self.login = str(self.login)
        self.login = self.login.strip()
        self.login = QtCore.QString(self.login)

        self.hash_key = hashlib.md5(self.login).hexdigest()
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        grab = Grab(timeout=50, connect_timeout=25,
                    url='http://sysadmin.1cps.ru/alisa/activate.php')
        grab.setup(post={
                   'user': self.login, 'key': self.hash_key, 'datetime': datetime, 'KeyGen': True})
        grab.request()
        self.lineEdit_key.setText(self.hash_key)
        # Вставить в буфер обмена
        cb = QtGui.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.hash_key, mode=cb.Clipboard)

    def main(self):
        try:
            w.prepare()
        except Exception:
            pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = KeyGen()
    w.setWindowTitle('Alisa KeyGen')
    w.show()
    w.main()
    sys.exit(app.exec_())
