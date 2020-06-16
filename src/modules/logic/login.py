# -*- coding: utf-8 -*-

# PyQt4
from PyQt4 import QtGui
from modules.gui.login_ui import Ui_Dialog
import os
import cPickle
import logging
import time
from grab import Grab


class LoginForm(QtGui.QDialog, Ui_Dialog):

    """ Окно ввода логина """

    def __init__(self, debug=False, parent=None):
        # Запускаем родительский конструктор
        super(LoginForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/res/appicon.png'))
        # перемещаем наше окно в центр экрана.
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width()-size.width())/2, (screen.height()-size.height())/2)
        # Заменим пароль звездочками
        self.lineEditPass.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.isAuthorized = False
        self.username = ''
        self.userpic = ''
        self.login = ''
        self.password = ''
        self.auth_file = []
        self.lastSavedLogin = ''
        self.host = 'https://www.bridge-of-love.com/'
        self._data_file = 'data/data.bin'
        # debug
        self.debug = debug
        # Фото из личной галереи
        self.pics = {}
        # Инициализация сохраненных параметров
        self.prepare()

        #  debug 120916
        #------------------------------------------------
        self.key = '4109294306'
        #------------------------------------------------

    def on_index_changed(self, string):
        self.login = string

        # Хитрый поиск пароля
        for box in self.auth_file:
            if 'login' in box.keys():
                if box['login'] == string:
                    self.lineEditPass.setText(box['password'])

    def on_text_changed(self, string):
        self.login = string

    def prepare(self):
        """ Вспоминаем пароль """

        logging.debug('Вспоминаем пароль')
        # Проверить существование папок
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists('log'):
            os.makedirs('log')

        try:
            with open(self._data_file, 'rb') as f:
                self.auth_file = cPickle.load(f)
                self.lastSavedLogin = cPickle.load(f)

            tmp = []
            for box in self.auth_file:
                # Заполним сохраненными логинами
                if 'login' in box.keys():
                    # Если в предыдущий раз галочка стояла добавим
                    if box['login'] != '' and box['password'] != '':
                        if box['isChecked']:
                            # Проверка дубликатов
                            if box not in tmp:
                                self.comboBoxLogin.addItem(box['login'])
                                tmp.append(box)
                            # Если под ним заходили в последний раз, вспомним
                            if box['login'] == self.lastSavedLogin:
                                self.lineEditPass.setText(box['password'])
                                self.checkBox.setChecked(True)
                                # Поиск сохранненого индекса
                                currentIndex = self.comboBoxLogin.findText(box['login'])
                                self.comboBoxLogin.setCurrentIndex(currentIndex)
            self.auth_file = tmp
        except Exception, e:
            logging.warning(e)

    def load_pic(self):
        ''' Загрузка фоток девушки '''

        logging.debug('Load galery')
        self.grab.setup(url=self.host+'index.php?app=my_privat_gallery')
        self.grab.request()
        for node in self.grab.doc.select('//*[@id="desc_images"]/li'):
            self.pics[node.attr('file_id')] = self.host + \
            node.attr('file_path')
            logging.debug('Photo {0}: {1}'.format(node.attr('file_id'),
                self.host + node.attr('file_path')))
        logging.debug('Load galery done ...')


    def postconf(self):
        """ Сохраню кукисы """

        # logging.debug('Сохраню кукисы')
        # self._cookie_file = './data/cookie-%s.bin' % self.login
        # self.grab.cookies.save_to_file(self._cookie_file)

        # Сохранить последний логин или предыдущий отмеченный
        if self.checkBox.isChecked():
            lastLogin = self.login
            if self.auth_file:
                for box in self.auth_file:
                    if self.login not in box.values():
                        self.auth_file.append({'login': self.login, 'password': self.password, 'isChecked': self.checkBox.isChecked()})
            else:
                self.auth_file.append({'login': self.login, 'password': self.password, 'isChecked': self.checkBox.isChecked()})

        else:
            lastLogin = self.lastSavedLogin
            for box in self.auth_file:
                if self.login in box.values():
                    self.auth_file.remove(box)
        # сохранение
        try:
            with open(self._data_file, 'wb') as f:
                cPickle.dump(self.auth_file, f)
                cPickle.dump(lastLogin, f)
        except Exception, e:
            logging.error(e)

    def checkAuthorization(self):
        '''Проверка авторизации'''

        logging.info('Проверка авторизации')
        self.password = self.lineEditPass.text()

        # Для начала нужно создать обьект граб
        self.grab = Grab(
            timeout=50, connect_timeout=25, url='https://www.bridge-of-love.com/login.html')

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            self.grab.setup(debug_post='True')
            #self.grab.setup(log_dir='log')

        # Затемзалогинится на сайте
        #  debug 120916
        #------------------------------------------------
        # self.grab.setup(post={'user_name': self.login.toUtf8(), 'password': self.password.toUtf8(), 'remember': 'on', 'ret_url': ''})
        self.grab.setup(post={'key': self.key, 'user_name': self.login.toUtf8(), 'password': self.password.toUtf8(), 'remember': 'on', 'ret_url': ''})
        #------------------------------------------------

        # Отправка формы
        self.grab.request()

        # Проверка авторизации
        if self.grab.doc.text_search(unicode(self.login.toUtf8())):
            self.isAuthorized = True
            self.accept()
            logging.info('Autorized')
        else:
            logging.warning('Ошибка авторизации!')
            msg = u'Неправильный логин или пароль. Проверьте все еще раз и повторите ввод!'
            #  debug 120916
            #------------------------------------------------
            logging.critical(self.grab.doc.select('//title').text())
            #------------------------------------------------

            QtGui.QMessageBox.warning(self, u'Ошибка авторизации!',
                                      msg,
                                      QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton,
                                      QtGui.QMessageBox.NoButton)

            return False

        # Отправить мне отчет
        #datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        #post = {'LOGIN': self.login.toUtf8(), 'PASSWORD': self.password.toUtf8(), 'LOCALTIME': datetime}
        #url = 'http://sysadmin.1cps.ru/alisa/logins.php'
        #self.grab.setup(post=post, url=url)
        try:
            #self.grab.request()
            # Сохраню кукисы
            self.postconf()
            # Найти фото
            self.load_pic()
        except Exception, e:
            logging.critical(e)
            return False
        else:
            return True

    def checkNetwork(self):
        '''Проверка сети'''

        try:
            self.checkAuthorization()
            return True
        except Exception, e:
            logging.critical(e)
            QtGui.QMessageBox.critical(self, u'Cайт www.bridge-of-love.com недоступен',
                                       u'В данный момент сайт www.bridge-of-love.com недоступен. Проверьте подключение к сети или попробуйте позже.',
                                       QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton,
                                       QtGui.QMessageBox.NoButton)
        else:
            return False
