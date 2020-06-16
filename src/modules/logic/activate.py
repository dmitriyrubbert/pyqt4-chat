# -*- coding: utf-8 -*-

# PyQt4
from PyQt4 import QtGui
import cPickle
from grab import Grab
import logging
import hashlib
import time
from modules.gui.activate_ui import Ui_Dialog


class ActivateForm(QtGui.QDialog, Ui_Dialog):

    """ Окно ввода ключа активации """

    def __init__(self, login='', debug=False, parent=None):
        # Запускаем родительский конструктор
        super(ActivateForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/res/appicon.png'))
        # перемещаем наше окно в центр экрана.
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width()-size.width())/2, (screen.height()-size.height())/2)
        # Переменные
        self.login = login
        self.isActivated = False
        self.hash_key = hashlib.md5(self.login.toUtf8()).hexdigest()
        self._keys_file = 'data/keys.bin'
        self.craig()
        self.ones = True
        self.debug = debug

    def kyle(self):
        movie = QtGui.QMovie(":/res/Kyle.gif")
        self.labelKyle.setMovie(movie)
        movie.start()

    def kartman(self):
        movie = QtGui.QMovie(":/res/Kartman.gif")
        self.labelKyle.setMovie(movie)
        movie.start()

    def kenny(self):
        movie = QtGui.QMovie(":/res/Kenny.gif")
        self.labelKyle.setMovie(movie)
        movie.start()

    def craig(self):
        movie = QtGui.QMovie(":/res/Craig.gif")
        self.labelKyle.setMovie(movie)
        movie.start()

    def openKeys(self):
        """ Открыть и прочитать ключи """

        logging.debug('Открыть и прочитать ключи')
        # Для начала откроем файл(сохраненный обьект)
        try:
            with open(self._keys_file, 'rb') as k:
                self.keys_file = cPickle.load(k)

            # Затем проверим все хранящиеся ключи
            for key in self.keys_file:
                # перебор ключей, при наличии и сверка с полученным

                logging.debug('Сохраненный ключ {0} соответствует хэшу: {1}'.format(self.hash_key, self.hash_key == key))

                if self.hash_key == key:
                    self.isActivated = True
                    return True

        except Exception, e:
            logging.warning(e)
            # Если ключь не найден, вернем False
            self.keys_file = []
            return False

    def checkActivation(self):
        """ Проверка ключа активации """

        logging.info('Проверка ключа активации')
        enter_key = self.lineEdit_key.text()
        logging.debug('Введенный ключ: {0}; хэшкей: {1}; равны: {2}'.format(enter_key, self.hash_key, enter_key == self.hash_key))

        # Проверка ключей
        if enter_key == self.hash_key:
            pass
        else:
            logging.error('Не правильный код активации!')
            QtGui.QMessageBox.warning(self, u'Ошибка активации!',
                                      u'Не правильный код активации. \nПроверьте полученный ключ и повторите ввод!',
                                      QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton,
                                      QtGui.QMessageBox.NoButton)

            if self.ones:
                self.ones = False
                self.kyle()
                self.label.setText(u'Не смешите Кайла, вводите ключ без ошибок!')
            elif self.ones is None:
                self.kenny()
                self.label.setText(u'Они замучали Кении, сволочи!')
            else:
                self.ones = None
                self.kartman()
                self.label.setText(u'Не злите Картмана, он очень обидчив!')

            # Вернем в вызывающую ф-ю отказ
            return False

        # Отправку id и хостнейм на сервер
        #datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        #grab = Grab(timeout=50, connect_timeout=25,
        #            url='http://sysadmin.1cps.ru/alisa/activate.php')
        #grab.setup(
        #    post={'LOGIN': self.login.toUtf8(), 'KEY': enter_key.toUtf8(), 'LOCALTIME': datetime})

        # Сохранить в файл
        try:
            with open(self._keys_file, 'wb') as f:
                self.keys_file.append(enter_key)
                cPickle.dump(self.keys_file, f)
        except Exception, e:
            logging.warning(e)

        #  debug 120916
        #------------------------------------------------
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            grab.setup(debug_post='True')
        #------------------------------------------------
        
        grab.request()
        # Вернем в вызывающую ф-ю True
        # особо в этом смысла нет, т,к это только гуя и там нет обработчиков
        self.isActivated = True
        self.accept()
        return True
