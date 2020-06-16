# -*- coding: utf-8 -*-

from grab.spider import Spider, Task
import sys
import re
from random import choice
import logging
from urlparse import parse_qs
from PyQt4 import QtCore


class Admirers(Spider):

    """ SearchInvite будет искать мужиков по заданному патерну и слать им спам """

    initial_urls = ['https://www.bridge-of-love.com/login.html']

    def __init__(self, cookie_file, letter_subject, letter_body,
                 letter_photos, current_messege=0, sleep=1, sleep_interval_enabled=False,
                 sleep_interval=60, random=False, blacklist=[], id='', password='',
                 debug=False, thread_number=0):

        super(Admirers, self).__init__()
        # Переменная отвечает разрешена ли работа в текущий момент
        self.running = True
        # Включить отладку?
        self.debug = debug
        # Откуда брать кукис
        self.cookie_file = cookie_file
        # Отдавать сообщение о работе
        self.status_message = ''
        # id
        self.id = id
        # debug 110816
        self.password = password
        #---------------------------
        # Храним отчет тут
        # self.result_file = './result/result-{0}.txt'.format(self.id)
        # Этот счётчик будем использовать для отправленных инвайтов
        self.result_counter = 0
        # Хранит общее число мужиков
        self.menTotal = 0
        # Хранит общее число мужиков на странице
        self.menForPage = 12
        # Задержка м/у отправкойы
        self.delay = 1
        # Заголовок сообщения
        self.letter_subject = letter_subject
        # Тело сообщения
        self.letter_body = letter_body
        # Одно письмо
        self.current_messege = current_messege
        # Фото
        self.letter_photos = letter_photos
        # sleep
        self.sleep = sleep
        # random
        self.random = random
        # blacklist
        self.blacklist = blacklist
        self.count = 3
        self.error_count = 0
        # Засыпать при ошибке
        self.sleep_interval_enabled = sleep_interval_enabled
        self.sleep_interval = sleep_interval
        # Добавляем id с ошибкой "вы бот"
        self.sesion_blacklist = []
        self.names = {}
        # Счетчик входов в task_invite
        self.truCount = 0

        # Проверить существование папок
        # if not os.path.exists('./result'):
        #     os.makedirs('./result')

        #  debug 120916
        #------------------------------------------------
        self.key = '4109294306'
        self.site = 'https://www.bridge-of-love.com/'
        #------------------------------------------------

    def create_grab_instance(self, **kwargs):
        """ Настройки граба """

        grab = super(Admirers, self).create_grab_instance(**kwargs)
        grab.setup(timeout=50, connect_timeout=25)
        try:
            # debug 110816
            #------------------------------------------------
            # grab.cookies.load_from_file(self.cookie_file)
            # Затемзалогинится на сайте
            
            #  debug 120916
            #------------------------------------------------
            grab.setup(post={'key': self.key, 'user_name': self.id, 'password': self.password, 'remember': 'on', 'ret_url': ''})
            #---------------------------------------------
            
            self.running = True
        except Exception, e:
            logging.critical(e)
            self.running = False

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            grab.setup(debug_post='True', debug='True')
        return grab

    def prepare(self):
        """ Подготовка данных, проверка валидностим """

        logging.info('Запуск рассылки поклонникам')
        logging.debug('Проверка полученных данных')
        # Если нам ничего не передали (QStringList or not QStringList)
        if not len(self.letter_subject) or not len(self.letter_body):
            logging.error("Передан пустой заголовок или сообщение!")
            self.quit()
        for x in self.letter_body:
            if x == '' or len(x) < 200:
                logging.error("Передано собщение меньше 200 символов!")
                self.quit()
        for x in self.letter_subject:
            if x.isEmpty() or x.contains(QtCore.QRegExp("^\s+")):
                logging.error("Передан пустой заголовок сообщения!")
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
            # debug 110816
            #------------------------------------------------
            message = [u'System message - Login already!- Powered by Dating co.',
                       u'Системное сообщение - Вы уже в системе!- Powered by Dating co.',
                       u'System message - Login successful!- Powered by Dating co.']
            #------------------------------------------------
            # Если ответ содержит один из ответов, продолжаем работу
            contains = False
            for x in message:
                if grab.doc.text_search(x):
                    logging.info(x)
                    contains = True
            if not contains:
                # debug 110816
                #------------------------------------------------
                logging.critical(grab.doc.select('//title').text())
                #-------------------------------------------------

                self.status_message = u'ОШИБКА [НЕ АВТОРИЗОВАН]'
                logging.critical(self.status_message)
                # debug 110816
                sys.exit()

            # Поехали, запуск двигателей ...
            self.url = 'https://www.bridge-of-love.com/index.php?app=my_favorite'
            grab.setup(url=self.url)
            yield Task('search', grab=grab)

    def task_search(self, grab, task):
        """ Поиск числа страниц """

        logging.info("Поиск числа страниц")
        max = 0
        for link in grab.doc.select('//div[contains(@class, "page_nav")]//a/@href'):
            t = link.html()
            if '&page=' in t:
                m = int(re.search('&page=(\d*)', t).group(1))
                if m > max:
                    max = m
        # Перейдем по ней и выясним, действительно ли она последняя
        url = self.url + '&page=' + str(max)
        grab.setup(url=url)
        # Для этого запустим новый таск
        yield Task('get_last_page', grab=grab)

    def task_get_last_page(self, grab, task):
        '''Выяснить, действительно ли она последняя'''

        logging.info('Проверка последней страницы')
        max_pages = 0
        for link in grab.doc.select('//div[contains(@class, "page_nav")]//a/@href'):
            t = link.html()
            if '&page=' in t:
                m = int(re.search('&page=(\d*)', t).group(1))
                if m > max_pages:
                    max_pages = m

        # Счетчик (общее число мужиков = число страниц * мужиков на странице)
        self.menTotal = max_pages * self.menForPage
        logging.info('Всего найдено {0} страниц, всего {1} мужчин'.format(max_pages, self.menTotal))

        '''Генерация абсолютных ссылок страниц'''
        self.status_message = u'Запускаю поиск поклонников'
        logging.info(self.status_message)
        for x in range(1, max_pages+1):
            # Готовим ссылку1
            url = self.url + '&page=' + str(x)
            grab.setup(url=url)

            '''Переход на страницу для выборки данных'''
            yield Task('parse', grab=grab, page=x)

    def task_parse(self, grab, task):
        '''Переход на одну страницу для выборки данных,
        для каждого найденного запустить отправку письма'''

        self.status_message = u'Собираю информацию о поклонниках ...'
        logging.debug('TASK URL: {0}'.format(task.url))

        """ Проверка последней страници """
        if grab.doc.text_search(u'Нет данных!') or grab.doc.text_search(u'No members!'):
            self.status_message = u'Всего {0} страниц мужчин онлайн'.format(task.page)
            logging.info(self.status_message)

        men_for_page = 0

        """ Выбор name _id на  странице """
        for node in grab.doc.select("""//ul[contains(@class, "matrix_list1")]
            //div[contains(@class, "user_info_right f_l")]
            //a[@class='name']"""):

            name = unicode(node.attr('title'))
            _id = unicode(parse_qs(node.attr('href'))['id'][0])

            item = {}
            item[_id] = name

            """ Сборка url для post """
            url = '{0}index.php?app=message&act=send&to_user_id={1}'.format(self.site,_id)

            '''Запуск обработчика для одного мужика'''
            grab.setup(url=url)

            '''тайминги'''
            self.count += 1
            delay = self.sleep * self.count
            yield Task('send', grab=grab, item=item, delay=delay)

            men_for_page += 1
        logging.debug('Всего мужчин на странице по {0} штук.'.format(men_for_page))

    def task_send(self, grab, task):
        """ Переход на страницу отправки письма одному мужику """

        pos = 0
        post = {}
        item = task.item.popitem()

        '''Проверка, случайно или по порядку'''
        if self.random:
            pos = choice(range(len(self.letter_body)))
            message = self.letter_body[pos]
        else:
            message = self.letter_body[self.current_messege]
            pos = self.current_messege

        '''Проверка если число заголовков != числу писем, то заголовок выбирается произвольно'''
        if len(self.letter_subject) != len(self.letter_body):
            subject = self.letter_subject[choice(range(len(self.letter_subject)))]
        else:
            subject = self.letter_subject[pos]

        '''Проверка, если в черном списке, то pass'''
        if item[0] in self.blacklist:
            try:
                self.status_message = u'Сообщение для {0}:{1} [ОТМЕНЕНО]'.format(
                    item[1].encode('utf8'), item[0].encode('utf8'))
                logging.debug(self.status_message)
            except Exception, e:
                logging.error(e)
        else:
            '''Вставим вместо макроса имя'''
            if message.contains('%name%'):
                message = message.replace('%name%', item[1])
            if subject.contains('%name%'):
                subject = subject.replace('%name%', item[1])

            # Конвертируем в HTML
            message = message.replace(QtCore.QRegExp("\t|\n|\v|\f|\r"), "<br>")

            '''Добавим фото к письму'''
            pic = ''
            for image in self.letter_photos:

                pic = pic + '<p class="thumb" style="text-align: center;">\
                <a href="{0}" rel="group"><img src="{1}" border="0" alt="My Photo"\
                width="300" data-thumb="{1}" /></a></p>'.format(image, image)

            '''Сборка письма'''
            message.prepend('<p>')
            message.append('</p>')
            message.append(pic)

            '''Подготовка POST запроса'''
            for node in grab.doc.select('//form[@id="send_message_form"]//input[@type="hidden"]'):
                post[node.attr('name')] = node.attr('value')

            post['msg_subject'] = subject.toUtf8()
            post['msg_content'] = message.toUtf8()
            post['phone_id'] = ''

            grab.setup(post=post)

            # # Счетчик (общее число мужиков = число тасков
            # self.menTotal += 1

            '''Отправка и сохранение результатов'''
            yield Task('invite', grab=grab, item=item, pos=pos)

    def task_invite(self, grab, task):
        """ Созраняем результаты """

        # Сброс ошибки
        self.error_count = 0
        responce = grab.doc.select('//title').text()
        sucess = u'Системное сообщение - Сообщение отправлено успешно!- Powered by Dating co.'
        # errors = u'Системное сообщение - Вы не можете так часто отправлять сообщения! Вы бот?- Powered by Dating co.'
        task.pos = unicode(task.pos)
        self.status_message = u'Письмо № {0} {1} (id {2}): {3}'.format(task.pos, task.item[1], task.item[0], responce)

        '''если сервер сообщил об успешной отправке'''
        if responce in sucess:
            self.result_counter += 1
            # self.result.writerow([task.item[0].encode('utf8'), task.item[1].encode('utf8')])
            self.sesion_blacklist.append(task.item[0])
        else:
            '''если ошибка'''
            self.error_count += 1
            self.status_message = u'Ошибка при ответе сервера: {0};'.format(responce)

        '''сохранить результат'''
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
        """ Завершение потоков и выход из рассылки """

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

    def task_search_fallback(self, task):
        """ Отловить ошибочные задания """
        self.status_message = u'ОШИБКА ОПРЕДЕЛЕНИЯ ЧИСЛА ПОКЛОННИКОВ '
        logging.error(self.status_message)
        self.quit()

    def task_get_last_page_fallback(self, task):
        """ Отловить ошибочные задания """
        self.status_message = u'ОШИБКА ПОИСКА ПОСЛЕДНЕЙ СТРАНИЦИ'
        logging.error(self.status_message)
        self.quit()

    def task_parse_fallback(self, task):
        """ Отловить ошибочные задания """
        self.status_message = u'ОШИБКА РАЗБОРА СТРАНИЦ'
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
