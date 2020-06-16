# -*- coding: utf-8 -

from PyQt4 import QtCore
from modules.script.admirers import Admirers
from modules.script.chat import Chat
import logging


class AbstractThread(QtCore.QThread):

    """ Поток на QThread для grab """

    def __init__(self, timer_obj, config_obj, cookie_file, password='', debug=True):
        super(QtCore.QThread, self).__init__()
        self.running = False
        self.debug = debug
        self.isTerminated = False
        """ obj  """
        self.timer = timer_obj
        self.config = config_obj
        self.cookie_file = cookie_file
        # debug 110816
        #------------------------------------------------
        self.password = password

    def prepare(self):
        print u'Вы должны сначала должны переопределить метод prepare() и setup()'
        self.quit()
        # self.index = self.config.one_msg_index
        # self.body = self.config.letter_body

    def setup(self, index=0):
        """ создание обьекта """
        pass
        # self.spider = Admirers(self.cookie_file, self.config.letter_subject,
        #                        self.body, self.config.current_photo,
        #                        index, self.config.timeaut, self.config.sleep_interval_enabled,
        #                        self.config.sleep_interval, self.config.random,
        #                        self.config.admirer_blacklist_body, self.config.id,
        #                        self.config.debug)

        # self.timer.setup(self.spider)
        # self.timer.start()

    def run(self):
        """ Запуск потока """

        self.running = True
        self.isTerminated = False
        self.prepare()

        while self.running:

            """ Если 1-3 режим, отработали и все  """
            if self.config.mode == 1 or self.config.mode == 3:
                self.setup(self.index)
                self.spider.run()

                # Закончили, расскажем всем кто был злодей
                blacklist = self.spider.getBlacklist()
                self.emit(QtCore.SIGNAL("iter_done (PyQt_PyObject)"), blacklist)

            """ Если 2-й режим, уходим в цикл  """
            if self.config.mode == 2:
                for x in range(len(self.body)):
                    # Оборвать в случае нажатия СТОП
                    if self.running:

                        # ВЫДЕРЖАТЬ ИНТЕРВАЛ М/У РАССЫЛКОЙ ВСЕМ ОЧЕРЕДНОГО ПИСЬМА
                        # Начинаем засыпать после 1-й итерации
                        interval = self.config.interval*60
                        if x:
                            self.timer.show_sleep = True
                            self.sleep(interval)
                            self.timer.show_sleep = False

                        # НАЧАТЬ С ЭТОГО ПИСЬМА
                        msg = x
                        # если выбрано письмо в one_letter_index, начать с него
                        if self.index != 0:
                            msg = x + self.index
                        # Чтоб не выйти за предел списка
                        if msg == len(self.body):
                            break
                        # Запуск
                        # передать в граб текущее письмо
                        self.setup(msg)
                        self.spider.run()
                        # Закончили, расскажем всем кто был злодей
                        blacklist = self.spider.getBlacklist()
                        self.emit(QtCore.SIGNAL("iter_done (PyQt_PyObject)"), blacklist)
                    else:
                        # Оборвать в случае нажатия СТОП
                        break

            # ПРОВЕРКА НА ПОВТОР РАССЫЛКИ
            if not self.config.repeat:
                self.running = False

            # выход
            self.emit(QtCore.SIGNAL("task_done (bool, bool)"), self.running, self.isTerminated)

    def stop(self):
        self.running = False
        self.isTerminated = True
        self.spider.quit()


class AdmirerThread(AbstractThread):

    """ Отправка писем поклонникам """

    def prepare(self):
        self.index = self.config.one_letter_index
        self.body = self.config.letter_body

    def setup(self, index=0):
        """ создание обьекта """
        # debug 110816
        #---------------------------------------------
        self.spider = Admirers(self.cookie_file, self.config.letter_subject,
                               self.body, self.config.current_photo,
                               index, self.config.timeaut, self.config.sleep_interval_enabled,
                               self.config.sleep_interval, self.config.random,
                               self.config.admirer_blacklist_body, self.config.id,
                               self.password, self.config.debug)
        #---------------------------------------------
        self.timer.setup(self.spider)
        self.timer.start()


class ChatThread(AbstractThread):

    """ Отправка сообщений в чат  """

    def setup(self, index=0):
        """ создание обьекта """
        # debug 110816
        #------------------------------------------------
        self.spider = Chat(self.cookie_file, self.body, index,
                           self.config.timeaut, self.config.random,
                           self.config.chat_blacklist_body, self.config.id,
                           self.password, self.config.debug)
        #------------------------------------------------
        self.timer.setup(self.spider)
        self.timer.start()

    def prepare(self):
        self.index = self.config.one_msg_index
        self.body = self.config.msg_body


class TimerThread(QtCore.QThread):

    """Обработка работы спайдера, вывод статистики"""

    def __init__(self, config):
        super(QtCore.QThread, self).__init__()
        self.running = False
        self.count = 0
        self.config = config
        self.show_sleep = False

    def setup(self, spider):
        self.spider = spider

    def run(self):
        """ Запуск потока """
        self.running = True
        self.show_sleep = False

        while self.running:
            # если не режим сна показывать статичтику
            if not self.show_sleep:
                # счеткики спайдера
                self.count = self.spider.getCount()
                self.total = self.spider.getTotal()
                self.status = self.spider.getStatus()
                logging.debug('TimerThread :: счеткик отправленных:{0}'.format(self.count))
                logging.debug('TimerThread :: всего мужчин:{0}'.format(self.total))

                # если в спайдере возникла ошибка
                if self.spider.error_count:
                    self.error_count = self.spider.error_count
                    logging.debug('TimerThread :: число ошибок:{0}'.format(self.error_count))
                    self.emit(QtCore.SIGNAL("spider_error (bool, QString)"),
                              self.error_count, self.status)

                else:
                    # если спайдер работает и все заебись
                    self.emit(QtCore.SIGNAL("status (int, int, QString)"),
                              self.count, self.total, self.status)

            else:
                # если спайдер спит показывать обратный отсчет сна
                self.emit(QtCore.SIGNAL("sleep"))

            # обновлять счетчики одновременно с интервалом расылки
            self.sleep(self.config.timeaut)
