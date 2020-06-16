# -*- coding: utf-8 -
import time
import logging
from PyQt4 import QtGui, QtCore
from PyQt4.QtWebKit import QWebSettings, QWebView, QWebPage
from modules.gui.mainwindow_ui import Ui_MainWindow
from modules.config.config import Config
from modules.script.threads import TimerThread
from modules.script.threads import ChatThread
from modules.script.threads import AdmirerThread
# from browser import CookieJar
from grab import Grab


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    """ Главное окно программы """

    def __init__(self, _id='', password='', pics={}, debug=False, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        """ переменные """
        self.running = False
        self.debug = debug
        self.id = _id
        self.password = password
        self.pics = pics
        self.cookie_file = './data/cookie-{0}.bin'.format(self.id)
        self.active_thread = QtCore.QThread()
        self.saved_counter = 0
        self.total = 0
        self.send = 0
        self.error_count = 0
        self.isLoadFinished = False
        self.isConfigured = False
        self.isVisible = True
        self.activeMode = 'chat'
        """ ui """
        self.setupUi(self)
        self.prepare()

    def createWiev(self):

        def _jsEvaluate():

            jsString = self.lineEdit_Js.text()
            jsReturn = self.webView.page().currentFrame().evaluateJavaScript(jsString)
            self.lineEdit_Js.setText(jsReturn.toString())
            print 'DEBUG:', jsReturn.toString()

        def jsEvaluate(string):
            ''' Принимает строку и выполняет ее в браузере '''

            jsString = QtCore.QString(string)
            jsReturn = self.webView.page().currentFrame().evaluateJavaScript(jsString)
            return jsReturn.toString()

        def jsFix():
            """ Правка стилей страницы чата """

            logging.debug('jsFix')
            # убрать зеленый хеадер
            # jsEvaluate("document.getElementsByClassName('b-header')[0].style.display='none';")
            # jsEvaluate("document.getElementsByClassName('b-content')[0].style.position='static';")
            # убрать кнопку рассылки
            jsEvaluate("document.getElementsByClassName('item modal-link')[0].style.display='none';")
            jsEvaluate("var div = document.createElement('div');document.body.appendChild(div);")
            jsEvaluate("""playSound = function( param ){ \
                div.innerHTML='<object type="application/x-shockwave-flash" \
                data="http://flash-mp3-player.net/medias/player_mp3_mini.swf" \
                width="0" height="0"><param name="FlashVars" \
                value="mp3='+param+'&autoplay=1" /></object>';};\
                """)
            if self.debug:
                jsEvaluate("playSound('http://sysadmin.1cps.ru/alisa/init.mp3')")

            jsEvaluate("cht.playSound = playSound")

        def openInBrowser(url):
            QtGui.QDesktopServices.openUrl(url)

        # self.webView = QWebView(self.frame)
        self.webView.page().settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.webView.page().settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        self.webView.page().settings().setAttribute(QWebSettings.AutoLoadImages, True)
        self.webView.page().settings().setAttribute(QWebSettings.LocalStorageEnabled, True)
        self.webView.page().settings().setAttribute(QWebSettings.OfflineWebApplicationCacheEnabled, True)
        self.webView.page().settings().enablePersistentStorage(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.TempLocation))
        # self.frame.addWidget(self.webView)
        # Потуги кэширования
        # QtNetwork.QNetworkRequest.CacheLoadControl(QtNetwork.QNetworkRequest.PreferCache)

        # debug 110816
        #-----------------------------------------------
        # Обработка кукисов
        # self.cookieJar = CookieJar(self.cookie_file)
        # self.webView.page().networkAccessManager().setCookieJar(self.cookieJar)
        #--------------------------
        url = 'https://www.bridge-of-love.com/index.php?app=chat&user_id=0&send_invite=1#'
        self.webView.load(QtCore.QUrl(url))
        self.webView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

        # debug 110816
        #------------------------------------------------
        def fillLoginForm():
            """ Заполнить поля формы """

            current_url = unicode(self.webView.url().toString())
            logging.debug('current_url:{0}'.format(current_url))
            if "app=chat" in current_url:
                doc = self.webView.page().mainFrame().documentElement()
                user = doc.findFirst('input[id=firstname]')
                passwd = doc.findFirst('input[id=password]')
                user.setAttribute("value", self.id)
                passwd.setAttribute("value", self.password)
                button = doc.findFirst('input[type=submit]')
                button.evaluateJavaScript('this.click()')

        # После загрузки страници поправить стили и прочее
        self.webView.loadFinished.connect(fillLoginForm)

        self.webView.loadFinished.connect(jsFix)
        # self.webView.loadFinished.connect(jsGrep)
        self.webView.linkClicked.connect(openInBrowser)
        self.isLoadFinished = True

    def prepare(self):
        """ Подготовка основного окна """

        logging.info('Подготовка основного окна')
        """ потоки и обьекты """
        self.config = Config(pics=self.pics, id=self.id, debug=self.debug)
        self.timer = TimerThread(self.config)
        # Делаем окно модальным
        self.config.setWindowModality(QtCore.Qt.ApplicationModal)
        # debug 110816
        #------------------------------------------------
        self.chat_thread = ChatThread(
            self.timer, self.config, self.cookie_file, self.password)
        self.admirer_thread = AdmirerThread(
            self.timer, self.config, self.cookie_file, self.password)
        #------------------------------------------------
        self.setWindowIcon(QtGui.QIcon(':/res/appicon.png'))
        QtGui.QApplication.setStyle(self.config.style)
        self.setWindowTitle('Alisa {0} www.bridge-of-love.com'.format(QtGui.QApplication.applicationVersion()))
        # перемещаем наше окно в центр экрана.
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width()-size.width())/2, (screen.height()-size.height())/2)

        # fullscreen
        self.resize(screen.width(), screen.height())

        # Сделать менюшки и действия к ним
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            self.createWiev()
        self.createActions()
        self.createMenus()
        self.pushButtonStop.setDisabled(True)
        self.lcdNumber_last.display('00:00:00')
        # прогресбар
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setMaximumSize(QtCore.QSize(300, 16777215))
        self.progressBar.hide()
        self.statusbar.addPermanentWidget(self.progressBar)
        # панель
        self.tool.move(self.tool.parent().geometry().x(), 
            self.tool.parent().geometry().y())
        self.on_hide()

        # Статистика работы граба
        self.connect(self.timer, QtCore.SIGNAL(
            "status (int, int, QString)"), self.on_change, QtCore.Qt.QueuedConnection)

        # Ошибки в работе граба
        self.connect(self.timer, QtCore.SIGNAL(
            "spider_error (bool, QString)"), self.on_error, QtCore.Qt.QueuedConnection)

        # Когда граб спит (режим 2, интервал)
        self.connect(self.timer, QtCore.SIGNAL(
            "sleep"), self.on_sleep, QtCore.Qt.QueuedConnection)

        # Успешное выполнение части задания граба
        self.connect(self.chat_thread, QtCore.SIGNAL(
            "iter_done (PyQt_PyObject)"), self.on_iter_done, QtCore.Qt.QueuedConnection)
        self.connect(self.admirer_thread, QtCore.SIGNAL(
            "iter_done (PyQt_PyObject)"), self.on_iter_done, QtCore.Qt.QueuedConnection)

        # Успешное выполнение граба
        self.connect(self.chat_thread, QtCore.SIGNAL(
            "task_done (bool, bool)"), self.on_task_done, QtCore.Qt.QueuedConnection)
        self.connect(self.admirer_thread, QtCore.SIGNAL(
            "task_done (bool, bool)"), self.on_task_done, QtCore.Qt.QueuedConnection)

    def show_pause(self, msg, last):
        ''' Проверка и отрисовка таймера ожидания
        следущей итерации после интервала '''

        self.lcdNumber_speed.display(msg)
        if last > 0:
            last = time.strftime('%H:%M:%S', time.gmtime(last))
            self.lcdNumber_last.display(last)

    def on_start(self):
        ''' Главный обработчик '''

        self.pushButtonStop.setDisabled(False)
        self.running = True
        self.start_time = time.clock()
        # установить счетчик отсчета сна как в настройках
        self.sleep_counter = self.config.interval*60
        self.error_count = 0

        if self.activeMode == 'chat':
            logging.info('Режим рассылка в чат')
            self.active_thread = self.chat_thread
        elif self.activeMode == 'admirers':
            logging.info('Режим рассылка по поклонникам')
            self.active_thread = self.admirer_thread

        """ Запуск потока """
        if not self.active_thread.isRunning():
            self.active_thread.start()
        else:
            self.active_thread.terminate()
            self.active_thread.start()

        self.progressBar.show()
        self.pushButtonStart.setDisabled(True)

    def on_stop(self):
        """ остановка потоков и выход """

        self.pushButtonStart.setDisabled(False)
        self.running = False

        # ждем завершения
        if self.active_thread.isRunning():
            # остановка спайдера
            self.active_thread.stop()
            self.active_thread.wait(300)
            self.active_thread.terminate()

        # остановка таймера
        if self.timer.isRunning():
            self.timer.running = False
            self.timer.wait(300)

        self.clear()
        self.pushButtonStop.setDisabled(True)

    def on_error(self, count, status):
        """ Вызываем при ошибочном ответе сервера  """

        self.lcdNumber_speed.display('error')
        self.statusbar.showMessage(status)
        self.error_count += 1

    """def closeEvent(self, event):

        quit_msg = u'Вы действительно хотите выйти из программы?'
        reply = QtGui.QMessageBox.question(self, u'Выход',
                                           quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.hide()
            self.active_thread.running = False
            self.timer.running = False
            if self.active_thread.isRunning():
                self.active_thread.stop()
                self.active_thread.wait(5000)
                self.active_thread.terminate()
            if self.timer.isRunning():
                self.timer.wait(5000)
            event.accept()
        else:
            event.ignore()"""

    def clear(self):
        """ Очистка счетчиков """

        # lcdNumber_sent
        # self.lcdNumber_sent.display(0)
        # lcdNumber_speed
        self.lcdNumber_speed.display(0)
        # lcdNumber_last
        self.lcdNumber_last.display('00:00:00')
        # statusbar
        self.statusbar.clearMessage()
        # progressBar
        self.progressBar.reset()
        self.progressBar.hide()
        # счетчик отправки
        self.saved_counter = 0

    def on_change(self, count, total, status):
        """ отрисовка процесса """

        # скорость равна таймауту
        # для правильного подсчета поставим 1
        speed = self.config.timeaut
        if not speed:
            speed = 1
        # отправка = счетчику спайдера
        self.send = count
        logging.debug('on_change :: показание счетчика Spider: {0}'.format(self.send))
        # всего мужиков
        self.total = total
        # если режим 1-3 то время_работы=всего*скорость
        run = self.total*speed
        # изменим счетчики если режим 2
        if self.config.mode == 2:
            if self.radioButtonChat.isChecked():
                # если чат = всего_мужиков*число_сообщ
                # если начинаем не с первого сообщения, то уменьшим число отправляемых
                self.total = total*len(self.config.msg_body)-self.config.one_msg_index
                # всего сообщений
                msg_count = len(self.config.msg_body)
            if self.radioButtonFav.isChecked():
                # если поклонники = всего_мужиков*число_писем
                # если начинаем не с первого письма, то уменьшим число отправляемых
                self.total = total*len(self.config.letter_body)-self.config.one_letter_index
                # всего писем
                msg_count = len(self.config.letter_body)
            # отправка = счетчик_спайдера+отправлено_ранее
            self.send = self.saved_counter + count
            logging.debug('on_change :: показание счетчика: {0} (2-й режим)'.format(self.send))
            # время_работы=(всего_мужиков*скорость)+(всего_сообщ*интервал_простоя)
            run = (self.total*speed)+(msg_count*self.config.interval)

        """ ОСТАЛОСЬ ВРЕМЕНИ """
        # время_конца=время_начала+время_работы
        end = self.start_time + run
        last = end - time.clock()
        # Чтобы не было 23:59:59
        if last > 0:
            last = time.strftime('%H:%M:%S', time.gmtime(last))
            self.lcdNumber_last.display(last)

        """ ОТПРАВЛЕНО """
        self.lcdNumber_sent.display(self.send)
        logging.debug('on_change :: показание счетчика: {0}'.format(self.send))

        """ ПРОГРЕСС БАР """
        # если режим 1-3, просто показываем не измененный счетчик
        self.progressBar.setMaximum(self.total)
        # текущее значение = всего-остаток
        # чтоб не было обратного отсчета
        value = self.total-(self.total-self.send)
        if value <= self.total:
            self.progressBar.setValue(value)

        """ СКОРОСТЬ """
        self.lcdNumber_speed.display(speed)

        """ СТРОКА СООСТОЯНИЯ """
        # просто проброс сообщ из спайдера
        self.statusbar.showMessage(status)

    def on_sleep(self):
        """  Когда граб спит (режим 2, интервал)  """

        self.sleep_counter -= self.config.timeaut
        self.show_pause('pause', self.sleep_counter)

    def on_iter_done(self, blacklist):
        ''' конец итерации '''

        # Сохранить блэклист
        if blacklist:
            if self.active_thread is self.admirer_thread:
                self.config.addToAdmirerBlacklist(blacklist)
                logging.debug('В блэклист занесено {0} поклонников'.format(len(blacklist)))
            elif self.active_thread is self.chat_thread:
                self.config.addToChatBlacklist(blacklist)
                logging.debug('В блэклист занесено {0} пользователей чата'.format(len(blacklist)))
        # Сохранить число отправленных для след итерации
        self.saved_counter = self.saved_counter + self.send
        # установить счетчик отсчета сна как в настройках
        self.sleep_counter = self.config.interval*60

    def on_task_done(self, running, terminated):
        """  когда цикл отправки завершен  """

        # выход если никто не нажал кнопки стоп
        if not running and not terminated:
            self.on_stop()

    def configWindow(self):
        '''  Окно настроек'''
        self.config.show()

    def toolbarModeSelected(self, mode):

        if mode:
            logging.debug('Тулбар: выбор режима')
            if self.radioButtonChat.isChecked():
                logging.debug('Тулбар: выбран режим чата')
                self.chatAct.setChecked(True)
                self.activeMode = 'chat'
            elif self.radioButtonFav.isChecked():
                logging.debug('Тулбар: выбран режим поклонников')
                self.admAct.setChecked(True)
                self.activeMode = 'admirers'

    def menuModeSelected(self, mode):

        if mode:
            logging.debug('Меню: выбор режима')
            if self.chatAct.isChecked():
                logging.debug('Меню: выбран режим чата')
                self.radioButtonChat.setChecked(True)
                self.activeMode = 'chat'
            elif self.admAct.isChecked():
                logging.debug('Меню: выбран режим поклонников')
                self.radioButtonFav.setChecked(True)
                self.activeMode = 'admirers'

    def createActions(self):
        ''' Создание действий к кнопкам '''

        self.setingsAct = QtGui.QAction(u"&Настройки", self,
                                        shortcut="Ctrl+P",
                                        statusTip=u"Настройки приложения",
                                        triggered=self.configWindow)

        self.exitAct = QtGui.QAction(u"&Выход", self,
                                     shortcut="Ctrl+Q",
                                     statusTip=u"Выход из приложения",
                                     triggered=self.close)

        self.aboutAct = QtGui.QAction(u"&О программе", self,
                                      shortcut="F1",
                                      statusTip=u"Показать информацию о программе",
                                      triggered=self.about)

        self.aboutQtAct = QtGui.QAction(u"О &PyQt4", self,
                                        statusTip=u"Показать информацию о библиотеке Qt4",
                                        triggered=QtGui.qApp.aboutQt)

        self.chatAct = QtGui.QAction(u"Рассылка в &чат", self, checkable=True,
                                     shortcut="Ctrl+1",
                                     statusTip=u"Запуск рассылки в чат",
                                     triggered=self.menuModeSelected)

        self.admAct = QtGui.QAction(u"Рассылка &поклонникам", self, checkable=True,
                                    shortcut="Ctrl+2",
                                    statusTip=u"Запуск рассылки поклонникам",
                                    triggered=self.menuModeSelected)

        self.runAct = QtGui.QAction(u"&Старт", self,
                                    shortcut="Ctrl+Enter",
                                    statusTip=u"Запуск рассылки",
                                    triggered=self.on_start)

        self.stopAct = QtGui.QAction(u"&Стоп", self,
                                     shortcut="Escape",
                                     statusTip=u"Остановка рассылки",
                                     triggered=self.on_stop)

        self.actionGroup = QtGui.QActionGroup(self)
        self.actionGroup.addAction(self.chatAct)
        self.actionGroup.addAction(self.admAct)
        self.admAct.setChecked(True)

    def createMenus(self):
        ''' Создание меню'''

        fileMenu = self.menuBar().addMenu(u"&Файл")
        fileMenu.addAction(self.setingsAct)
        fileMenu.addAction(self.exitAct)

        serviceMenu = self.menuBar().addMenu(u"&Сервис")
        serviceMenu.addAction(self.chatAct)
        serviceMenu.addAction(self.admAct)
        serviceMenu.addSeparator().setText("Управление")
        serviceMenu.addAction(self.runAct)
        serviceMenu.addAction(self.stopAct)

        helpMenu = self.menuBar().addMenu(u"&Справка")
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

    def about(self):
        QtGui.QMessageBox.about(self, u'О программе Alisa-Sender {0}'.format(QtGui.QApplication.applicationVersion()),
                                u'''Программа <b>Alisa-Sender</b>, это рассылка для сайта <a href="www.bridge-of-love.com.">www.bridge-of-love.com.</a> \
                                Написана на языке <a href="https://www.python.org/downloads/release/python-2710/">Python 2.7.12</a>,\
                                с использованием библиотеки парсинга вебсайтов для языка Python <a href="http://grablib.org">Grab 0.6.30</a> \
                                и графической библиотеки <a href="https://www.riverbankcomputing.com">PyQt4.8.7</a>
                                <p>Разработка и сопровождение: <a href="https://t.me/goldlinux">Goldlinux</a></p>''')

    def on_hide(self):

        if self.isVisible:
            self.toolBox.hide()
            self.isVisible = False
            self.toolButton.setArrowType(QtCore.Qt.RightArrow)
            self.tool.setGeometry(QtCore.QRect(self.tool.parent().geometry().x(), 
                self.tool.parent().geometry().y(), 40, 40))
            self.tool.setAutoFillBackground(False)

        else:
            self.toolBox.show()
            self.isVisible = True
            self.toolButton.setArrowType(QtCore.Qt.LeftArrow)
            self.tool.setGeometry(QtCore.QRect(self.tool.parent().geometry().x(), 
                self.tool.parent().geometry().y(), 245, 280))
            self.tool.setAutoFillBackground(True)
