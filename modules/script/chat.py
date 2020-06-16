# -*- coding: utf-8 -*-

from grab.spider import Spider, Task
import os
import sys
from random import choice
import csv
import logging
from PyQt4 import QtCore

SEND = True


class Chat(Spider, object):

    """ ChatSpiderSearch отвечает за функции отправки и ведение статистики """

    initial_urls = ['https://www.bridge-of-love.com/login.html']

    def __init__(self, cookie_file, template=[], current_messege=0,
                 sleep=1, random=False, blacklist=[], id='', password='', debug=False, thread_number=1):

        super(Chat, self).__init__()
        # Задать какое письмо отправлять
        self.current_messege = current_messege
        # Задержка м/у письмами
        self.sleep = sleep
        # Задать "случайное письмо"
        self.random = random
        # Включить блэклист
        self.blacklist = blacklist
        # Отладка
        self.debug = debug
        # Кортеж для мужиков в сети
        self.online = {}
        # Шаблоны сообщений
        self.template = template
        # Отвечает за работу
        self.running = False
        # Отправлять ответ cколько мужиков в сети
        self.menTotal = 0
        # Отправлять ответ кому шлем в текущий момент
        self.status_message = ''
        # Этот счётчик будем использовать для отправленных инвайтов
        self.result_counter = 0
        # Откуда брать кукис
        self.cookie_file = cookie_file
        # id
        self.id = id
        # debug 110816
        self.password = password
        # Храним отчет тут
        # self.result_file = './result/result-{0}.txt'.format(self.id)
        self.error_count = 0
        # Добавляем id с ошибкой "вы бот"
        self.sesion_blacklist = []
        # Счетчик входов в task_invite
        self.truCount = 0
        # Проверить существование папок
        # if not os.path.exists('./result'):
        #     os.makedirs('./result')

        #  debug 120916
        #------------------------------------------------
        self.key = '4109294306'
        #------------------------------------------------

    def create_grab_instance(self, **kwargs):
        # Настройки граба
        grab = super(Chat, self).create_grab_instance(**kwargs)
        grab.setup(timeout=50, connect_timeout=25)
        try:
            # debug 110816
            #------------------------------------------------
            # grab.cookies.load_from_file(self.cookie_file)
            # Затемзалогинится на сайте

            #  debug 120916
            #------------------------------------------------
            grab.setup(post={'key': self.key, 'user_name': self.id, 'password': self.password, 'remember': 'on', 'ret_url': ''})
            #------------------------------------------------

            # Отправка формы
            # grab.go('https://www.bridge-of-love.com/login.html')

            #------------------------------------------------

            self.running = True
        except Exception, e:
            logging.critical(e)
            self.status_message = u'Критическая ошибка, не удалось загрузить куки'
            self.running = False

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            grab.setup(debug_post='True')
            #grab.setup(log_dir='log')
        return grab

    def prepare(self):
        """ Подготовка """

        logging.info(
             """ $$$$$$\  $$\                  $$\
                $$  __$$\ $$ |                 $$ |
                $$ /  \__|$$$$$$$\   $$$$$$\ $$$$$$\
                $$ |      $$  __$$\  \____$$\\_$$  _|
                $$ |      $$ |  $$ | $$$$$$$ | $$ |
                $$ |  $$\ $$ |  $$ |$$  __$$ | $$ |$$\
                \$$$$$$  |$$ |  $$ |\$$$$$$$ | \$$$$  |
                 \______/ \__|  \__| \_______|  \____/

                 """
                 )

        if not len(self.template):
            self.quit()
        for x in self.template:
            if x.isEmpty() or x.contains(QtCore.QRegExp("^\s+")):
                self.quit()

        # Этот файл будем использовать для логирования отправленных инвайтов
        # self.result = csv.writer(open(self.result_file, 'wb'))

        # http://docs.grablib.org/en/latest/spider/error_handling.html?highlight=network_try_limit
        logging.debug('NETWORK_TRY_LIMIT: {0} (def 10)'.format(self.network_try_limit))
        # self.network_try_limit = 1
        # logging.debug('Установлен NETWORK_TRY_LIMIT :{0}'.format(self.network_try_limit))

        logging.debug('TASK_TRY_LIMIT: {0} (def 3)'.format(self.task_try_limit))
        # self.task_try_limit = 1
        # logging.debug('Установлен TASK_TRY_LIMIT :{0}'.format(self.task_try_limit))

    def task_initial(self, grab, task):

        if self.running:
            logging.info("Проверка авторизации")
            # Проверка авторизации
            if grab.doc.text_search(u'Мужчины - Мой кабинет'):
                logging.info('Autorized')
            else:
                self.status_message = u'ОШИБКА [НЕ АВТОРИЗОВАН]'
                logging.critical(self.status_message)
                logging.critical(self.grab.doc.select('//title').text())
                sys.exit()

            # Запускаем подготовку к рассылке
            # Переход на страницу чата, для получения HASH, IDS
            grab.setup(
                url='https://www.bridge-of-love.com/index.php?app=chat&user_id=0&send_invite=1#')
            yield Task('getHash', grab=grab)

    def task_getHash(self, grab, task):
        """ Переход на страницу чата, для получения HASH, IDS """

        logging.debug('Переход на страницу чата, для получения HASH, IDS')
        # Найти HASH сэссии
        self._hash = grab.doc.rex_text("HASH: '(.*)',")
        logging.debug(self._hash)
        # Найти IDS сэссии
        self._ids = grab.doc.rex_text("IDS: '(.*)',")
        logging.debug(self._ids)

        # Соберем мужиков
        grab.setup(post={
                   'ids': self._ids}, url='https://www.bridge-of-love.com/apiv2/index.php?app=ajax&act=get_online_list')
        # URL для отправки запроса
        yield Task('getOnline', grab=grab)

    def task_getOnline(self, grab, task):

        # print(grab.doc.body)
        _list = grab.doc.json

        for x in _list:
            for i in x['data']:
                # print i['id'], ':', i['name']
                self.online[i['id']] = i['name']
        self.status_message = u'Найдено %s мужчин онлайн' % len(self.online)

        self.menTotal = len(self.online)
        logging.info('Длинна списка мужчин:'.format(self.menTotal))

        yield Task('send', grab=grab)

    def task_send(self, grab, task):
        # Тут пока переменная running истина, из словаря выбираются все мужики,
        # формируются задания и отдаются в очередь. Все.
        i = 0
        while len(self.online):
            # Нужно прочитать шаблон сообщения из словаря
            # Если активна кнопка "случайное письмо"
            pos = 0
            if self.random:
                pos = choice(range(len(self.template)))
                message = self.template[pos]
            else:
                message = self.template[self.current_messege]
                pos = self.current_messege

            # Извлечение пары ID:NAME
            if len(self.online):
                item = self.online.popitem()
            else:
                self.running = False

            # Проверка, еслив черном списке, то pass
            if item[0] in self.blacklist:
                try:
                    self.status_message = u'Отправка сообщения для {0} : {1}[ОТМЕНЕНА]'.format(
                        item[0].encode('utf8'), item[1].encode('utf8'))
                    logging.debug(self.status_message)
                except Exception, e:
                    logging.error(e)
            else:
                # Вставим вместо макроса имя
                if message.contains('%name%'):
                    message = message.replace('%name%', item[1])

                # !!! Подготовка POST запроса
                url = 'https://www.bridge-of-love.com/apiv2/index.php?app=ajax&act=send_message'
                post = {'chat_id': '', 'message': message.toUtf8(), 'user_id': item[
                    0], 'hash': self._hash, 'ids': self._ids}

                if SEND:
                    grab.setup(url=url, post=post)
                else:
                    grab.setup(url=url)

                i += 1
                delay = self.sleep * i
                # Запуск обработчика выполняющего рассылку
                yield Task('invite', grab=grab, item=item, pos=pos, delay=delay)

    def task_invite(self, grab, task):
        """ Отправка сохранение """

        # 20/10/2017 ERROR - 'ascii' codec can't decode byte 0xc3 in position 1: ordinal not in range(128)

        # Сброс ошибки
        self.error_count = 0

        '''если сервер сообщил об успешной отправке'''
        if grab.doc.text_search(task.item[0]):
            self.result_counter += 1
            responce = u'Сообщение отправлено успешно'
            '''сохранить результат'''
            # self.result.writerow([task.item[0].encode('utf8'), task.item[1].encode('utf8')])
            # self.sesion_blacklist.append(task.item[0])
        else:
            # если в ответе сервера не найден user_id, сгенерировать ошибку
            self.error_count += 1
            self.sesion_blacklist.append(task.item[0])
            responce = u'Error while sending the message (see debug log)'
            # logging.error(grab.doc.select('//title').text())
            logging.debug(grab.response.body)
        try:
            self.status_message = u'Message {0} to {1} {2}: {3}'.format(task.pos+1,
                task.item[1], task.item[0], responce)
        except Exception as e:
            logging.warning(e)

        self.truCount += 1
        log = 'Всего мужиков:{0}; Попыток:{1} / Отправлено:{2}; Ответ сервера:{3}'.format(
            self.menTotal, self.truCount, self.result_counter, self.status_message.encode('utf8'))
        logging.info(log)

    def getCount(self):
        return self.result_counter

    def getTotal(self):
        return self.menTotal

    def getStatus(self):
        return self.status_message

    def getBlacklist(self):
        return self.sesion_blacklist

    def quit(self):
        """ Завершение потоков и выход """

        self.status_message = u"Завершение потоков и выход из рассылки"
        logging.info(self.status_message)
        self.running = False
        self.work_allowed = False
        self.result_counter = 0
        logging.debug(self.render_stats())

    def task_initial_fallback(self, task):
        """ Отловить ошибочные задания """
        self.status_message = u'ОШИБКА НА ЭТАПЕ ИНИЦИАЛИЗАЦИИ'
        logging.error(self.status_message)
        self.quit()

    def task_getHash_page_fallback(self, task):
        """ Отловить ошибочные задания """
        self.status_message = u'ОШИБКА ПОЛУЧЕНИЯ ХЭШ'
        logging.error(self.status_message)
        self.quit()

    def task_getOnline_fallback(self, task):
        """ Отловить ошибочные задания """
        self.status_message = u'ОШИБКА ПОЛУЧЕНИЯ СПИСКА ОНЛАЙН'
        logging.error(self.status_message)
        self.quit()

    def task_send_fallback(self, task):
        """ Отловить ошибочные задания """
        self.status_message = u'ОШИБКА ФОРМАРОВАНИЯ ЗАПРОСА'
        logging.error(self.status_message)
        self.quit()

    def task_invite_fallback(self, task):
        """ Отловить ошибочные задания """
        self.status_message = u'ПРОБЛЕММЫ С СЕТЬЮ! ПРОВЕРЬТЕ ПОДКЛЮЧЕНИЕ!'
        logging.error(self.status_message)
        # self.quit()
