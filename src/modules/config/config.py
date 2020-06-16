# -*- coding: utf-8 -*-

import os
import cPickle
import urllib
import time
from random import choice
from PyQt4 import QtGui, QtCore
from modules.gui.config_ui import Ui_Dialog
import logging
from grab import Grab


class Config(QtGui.QDialog, Ui_Dialog):

    """ Описание настроек программы """

    def __init__(self, pics={}, id='', debug=False, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/res/appicon.png'))
        # Инициальизация переменных
        self.id = id
        # Интервал между рассылками (мин.)
        self.interval = 1
        # Таймаут между сообщениями (сек.)
        self.timeaut = 3
        # Черный список
        self.blacklist = True
        # Повтор рассылки
        self.repeat = False
        # Выбор режима работы
        self.mode = 1
        # рандом
        self.random = False
        # Одно сообщение
        self.one_msg = QtCore.QString()
        # Одно письмо
        self.one_letter = QtCore.QString()
        # хранит текущий индекс одного письма
        self.one_letter_index = 0
        # -- сообщения
        self.one_msg_index = 0
        # список хранит имена выбранных фото
        self.current_photo = []
        # тема письма
        self.letter_subject = QtCore.QString()
        # тело письма
        self.letter_body = QtCore.QString()
        # тело ообщения
        self.msg_body = QtCore.QString()
        # тело blacklist
        self.chat_blacklist_body = QtCore.QString()
        self.admirer_blacklist_body = QtCore.QString()
        # Проверка корректности ввода
        self.correct = True
        # Отладка
        self.debug = debug
        # style
        self.style = ''
        # style_index
        self.style_index = 0
        # Загрузка превью фото
        self.pics = pics
        # Где хранить конфиг
        self.config_path = './data/config-{0}.bin'.format(self.id)
        # Засыпать при ошибке "вы что бот?" (мин)
        self.sleep_interval_enabled = False
        self.sleep_interval = 5
        # Проверить существование папок
        if not os.path.exists('./data'):
            os.makedirs('./data')
        # Загрузим натройки
        self.populate()
        self.load_config()

    def on_interval_changed(self, value):
        self.interval = value
        logging.debug('Изменен interval {0}'.format(self.interval))

    def on_timeaut_changed(self, value):

        if value < 3 and not self.debug:
            msg = u'''<b>Не рекомендуется ставить таймаут меньше трех секунд!</b>
            <br><br>Сервер может посчитать что вы бот и отбрасывать ваши сообщения.'''
            QtGui.QMessageBox.information(self, u'Внимание!', msg, QtGui.QMessageBox.Ok)

            self.horizontalSlider_timeaut.setProperty("value", 3)
            self.horizontalSlider_timeaut.setSliderPosition(3)
            value = 3

        value+choice(range(-2, 3))
        self.timeaut = value

        logging.debug('Изменен timeaut {0}'.format(self.timeaut))

    def on_blacklist_state_changed(self, state):
        if state == 2:
            self.blacklist = True
        else:
            self.blacklist = False
        logging.debug('Изменен blacklist {0}'.format(self.blacklist))

    def on_repeat_state_changed(self, state):
        if state == 2:
            self.repeat = True
        else:
            self.repeat = False

        logging.debug('Изменен repeat {0}'.format(self.repeat))

    def on_mode1_changed(self, togle):
        # случайно
        if togle:
            self.mode = 1
            self.random = True
        logging.debug('Изменен mode {0}; random {1}'.format(self.mode, self.random))

    def on_mode2_changed(self, togle):
        # по порядку
        if togle:
            self.mode = 2
            self.random = False
        logging.debug('Изменен mode {0}; random {1}'.format(self.mode, self.random))

    def on_mode3_changed(self, togle):
        # одно письмо
        if togle:
            self.mode = 3
            self.random = False
        logging.debug('Изменен mode {0}; random {1}'.format(self.mode, self.random))

    def on_one_letter_index_changed(self, string):
        self.one_letter = string
        logging.debug('Текущее "одно" письмо: {0}'.format(self.one_letter.toUtf8()))

    def on_one_letter_index_changed_int(self, index):
        self.one_letter_index = index
        logging.debug('Текущее "одно" письмо: {0}'.format(self.one_letter_index))

    def on_one_msg_index_changed(self, string):
        self.one_msg = string
        logging.debug('Текущее "одно" сообщение: {0}'.format(self.one_msg.toUtf8()))

    def on_one_msg_index_changed_int(self, index):
        self.one_msg_index = index
        logging.debug('Текущее "одно" сообщение: {0}'.format(self.one_msg_index))

    def on_photo_changed(self, item):
        """ Установить - снять видимость иконки """

        logging.debug('item.text(): {0}; in self.pics.keys(): {1}'.format(item.text().toUtf8(), item.text() in self.pics.keys()))

        # Проверка есть ли картинка в словаре
        if item.text() in self.pics.keys():
            url = self.pics[str(item.text())]

            if item.flags() & QtCore.Qt.ItemIsEnabled:
                # Выкл.
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEnabled)
                self.listWidgetPic.setItemSelected(item, False)
                self.current_photo.remove(url)
            else:
                # Вкл.
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.listWidgetPic.setItemSelected(item, True)
                self.current_photo.append(url)

        if item.text() == 'no photo':
            # Удалим все отметки
            del self.current_photo
            self.current_photo = []
            # Снимем выделение
            for i in range(self.listWidgetPic.count()):
                item = self.listWidgetPic.item(i)
                item.setFlags(item.flags() & ~ QtCore.Qt.ItemIsEnabled)
                self.listWidgetPic.setItemSelected(item, False)

        logging.debug('Изменены отметки фото: item.text() {0}; current_photo {1};'.format(unicode(item.text().toUtf8()), self.current_photo))

    def on_style_changed(self, index):
        self.style_index = index
        self.style = self.comboBox_style.currentText()

        logging.debug('Изменен style_index {0}; self.style {1};'.format(self.style_index, self.style))

    def on_letter_subject_changed(self):
        """ При изменении заголовка письма """

        # Прочитаем содержимое, получим PyQt4.QtCore.QString
        self.letter_subject_raw = self.plainTextEdit_letter_subject.toPlainText()
        # Разобьем полученную строку по символу = на список типа PyQt4.QtCore.QStringList
        self.letter_subject = self.letter_subject_raw.split(
            "=", QtCore.QString.SkipEmptyParts)
        # Почистим строки от дубликатов и пройдем регэкспом
        self.letter_subject.replaceInStrings(QtCore.QRegExp("^\s+|\s+$"), "")
        self.letter_subject.removeDuplicates()
        # Удаление пустых строк
        self.letter_subject.removeAll("")

        if self.debug:
            logging.debug('Изменен letter_subject;')
            i = 0
            for x in self.letter_subject:
                logging.debug('[START №{0}]{1}[END]'.format(i, x.toUtf8()))
                i += 1

    def on_letter_body_changed(self):
        """ При изменении тела письма """

        # Сохраним текущий индекс
        index = self.comboBox_one_letter.currentIndex()

        # Прочитаем содержимое, получим PyQt4.QtCore.QString
        self.letter_body_raw = self.plainTextEdit_letter_body.toPlainText()
        # Разобьем полученную строку по символу = на список типа PyQt4.QtCore.QStringList
        self.letter_body = self.letter_body_raw.split("=", QtCore.QString.SkipEmptyParts)
        # Почистим строки от дубликатов и пройдем регэкспом
        self.letter_body.replaceInStrings(QtCore.QRegExp("^\s+|\s+$"), "")
        self.letter_body.removeDuplicates()
        # Удаление пустых строк
        self.letter_body.removeAll("")
        # Вставим в QCombobox
        comboText = self.letter_body_raw.simplified().split("=", QtCore.QString.SkipEmptyParts)
        # Почистим строки от дубликатов и пройдем регэкспом
        comboText.removeDuplicates()
        comboText.replaceInStrings(QtCore.QRegExp("^\s+|\s+$"), "")
        self.comboBox_one_letter.clear()
        self.comboBox_one_letter.addItems(comboText)
        # Вернем предыдущий индекс
        if index != -1:
            self.comboBox_one_letter.setCurrentIndex(index)

        if self.debug:
            logging.debug('Изменен letter_body;')
            i = 0
            for x in self.letter_body:
                logging.debug('[START №{0}]{1}[END]'.format(i, x.toUtf8()))
                i += 1

    def on_msg_body_changed(self):
        """ При изменении тела сообщений """

        # Сохраним текущий индекс
        index = self.comboBox_one_msg.currentIndex()
        # Прочитаем содержимое, получим PyQt4.QtCore.QString
        self.msg_body_raw = self.plainTextEdit_msg.toPlainText()
        # Разобьем полученную строку по символу = на список типа
        # PyQt4.QtCore.QStringList
        self.msg_body = self.msg_body_raw.split(
            "=", QtCore.QString.SkipEmptyParts)
        # Почистим строки от дубликатов и пройдем регэкспом
        self.msg_body.replaceInStrings(QtCore.QRegExp("^\s+|\s+$"), "")
        self.msg_body.removeDuplicates()
        # Удаление пустых строк
        self.msg_body.removeAll("")
        # Вставим в QCombobox
        comboText = self.msg_body_raw.simplified().split("=", QtCore.QString.SkipEmptyParts)
        # Почистим строки от дубликатов и пройдем регэкспом
        comboText.removeDuplicates()
        comboText.replaceInStrings(QtCore.QRegExp("^\s+|\s+$"), "")
        self.comboBox_one_msg.clear()
        self.comboBox_one_msg.addItems(comboText)
        # Вернем предыдущий индекс
        if index != -1:
            self.comboBox_one_msg.setCurrentIndex(index)

        if self.debug:
            logging.debug('Изменен msg_body;')
            i = 0
            for x in self.msg_body:
                logging.debug('[START №{0}]{1}[END]'.format(i, x.toUtf8()))
                i += 1

    def on_chat_blacklist_body_changed(self):
        """ При изменении тела blacklist """

        # Прочитаем содержимое, получим PyQt4.QtCore.QString
        self.chat_blacklist_body_raw = self.plainTextEdit_chat_blacklist.toPlainText()
        # Обрезать лишние пробелы с концов и в середине строк
        # Разобьем полученную строку по символу ; на список типа
        # PyQt4.QtCore.QStringList
        self.chat_blacklist_body = self.chat_blacklist_body_raw.simplified().split(
            ",", QtCore.QString.SkipEmptyParts)
        # Почистим строки от дубликатов и пройдем регэкспом
        self.chat_blacklist_body.replaceInStrings(QtCore.QRegExp("\D"), "")
        # Удаление пустых строк
        self.chat_blacklist_body.removeAll("")
        self.chat_blacklist_body.removeDuplicates()

        if self.debug:
            logging.debug('Изменен chat_blacklist_body;')
            i = 0
            for x in self.chat_blacklist_body:
                logging.debug('[START №{0}]{1}[END]'.format(i, x.toUtf8()))
                i += 1

    def on_admirer_blacklist_body_changed(self):
        """ При изменении тела blacklist """

        # Прочитаем содержимое, получим PyQt4.QtCore.QString
        self.admirer_blacklist_body_raw = self.plainTextEdit_admirer_blacklist.toPlainText()
        # Обрезать лишние пробелы с концов и в середине строк
        # Разобьем полученную строку по символу ; на список типа
        # PyQt4.QtCore.QStringList
        self.admirer_blacklist_body = self.admirer_blacklist_body_raw.simplified().split(
            ",", QtCore.QString.SkipEmptyParts)
        # Почистим строки от дубликатов и пройдем регэкспом
        self.admirer_blacklist_body.replaceInStrings(QtCore.QRegExp("\D"), "")
        # Удаление пустых строк
        self.admirer_blacklist_body.removeAll("")
        self.admirer_blacklist_body.removeDuplicates()

        if self.debug:
            logging.debug('Изменен admirer_blacklist_body;')
            i = 0
            for x in self.admirer_blacklist_body:
                logging.debug('[START №{0}]{1}[END]'.format(i, x.toUtf8()))
                i += 1

    def on_sleep_interval_changed(self, value):
        '''Засыпать при ошибке "вы что бот?" (мин)'''

        self.sleep_interval = value

        logging.debug('Изменен sleep_interval {0}'.format(self.sleep_interval))

    def changePage(self, current, previous):
        if not current:
            current = previous
        self.stackedWidget.setCurrentIndex(self.listWidget.row(current))

    def load_config(self):
        """ Загрузить сохраненные параметры """

        logging.info("Загрузим сохраненные параметры")
        try:
            with open(self.config_path, 'rb') as f:
                self.interval = cPickle.load(f)
                self.timeaut = cPickle.load(f)
                self.blacklist = cPickle.load(f)
                self.repeat = cPickle.load(f)
                self.mode = cPickle.load(f)
                one_letter_index = cPickle.load(f)
                one_msg_index = cPickle.load(f)
                self.current_photo = cPickle.load(f)
                self.letter_subject_raw = cPickle.load(f)
                self.letter_body_raw = cPickle.load(f)
                self.msg_body_raw = cPickle.load(f)
                self.chat_blacklist_body_raw = cPickle.load(f)
                self.admirer_blacklist_body_raw = cPickle.load(f)
                self.style_index = cPickle.load(f)

            logging.debug("Восстановление сохраненных параметров")
            # Интервал
            self.horizontalSlider_interval.setProperty("value", self.interval)
            # Таймаут
            self.horizontalSlider_timeaut.setProperty("value", self.timeaut)
            # Блэклист
            self.checkBox_Blacklist.setChecked(self.blacklist)
            # Повтор
            self.checkBox_repeat.setChecked(self.repeat)
            # Режим работы
            if self.mode == 1:
                self.on_mode1_changed(True)
                self.radioButton_ramdom.setChecked(True)
            elif self.mode == 2:
                self.on_mode2_changed(True)
                self.radioButton_order.setChecked(True)
            elif self.mode == 3:
                self.on_mode3_changed(True)
                self.radioButton_one.setChecked(True)
            logging.debug("Вспоминаем фото в превью")
            logging.debug('Sawed photos:{0}'.format(self.current_photo))
            # очистка сохраненных фото
            # если у девушки в галерее такого фото нет
            # мы его удалим из списка
            if len(self.current_photo):
                for x in self.current_photo:
                    if x not in self.pics.values():
                        self.current_photo.remove(x)
            # пометка фото как активное в настройках
            for i in range(self.listWidgetPic.count()):
                item = self.listWidgetPic.item(i)
                if item.text() in self.pics.keys():
                    url = self.pics[str(item.text())]
                    if url in self.current_photo:
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.listWidgetPic.setItemSelected(item, True)

            logging.debug('Restored photos:{0}'.format(self.current_photo))
            logging.debug("Вспоминаем тело письма")
            # Вспоминаем letter_subject
            self.plainTextEdit_letter_subject.setPlainText(
                self.letter_subject_raw)
            # Вспоминаем self.letter_body
            self.plainTextEdit_letter_body.setPlainText(self.letter_body_raw)
            # Вспоминаем self.letter_body
            self.plainTextEdit_msg.setPlainText(self.msg_body_raw)
            # Вспоминаем self.chat_blacklist_body
            self.plainTextEdit_chat_blacklist.setPlainText(self.chat_blacklist_body_raw)
            self.plainTextEdit_admirer_blacklist.setPlainText(self.admirer_blacklist_body_raw)
            logging.debug("Вспоминаем положение текушего письма")
            self.comboBox_one_letter.setCurrentIndex(one_letter_index)
            self.comboBox_one_msg.setCurrentIndex(one_msg_index)
            self.comboBox_style.setCurrentIndex(self.style_index)
            logging.debug('Восстановление индексов: one_letter_index {0}; one_msg_index {1};'.format(one_letter_index, one_msg_index))

        except Exception, e:
            logging.warning(e)

        logging.debug('Загрузка стандартных значений')
        self.on_letter_body_changed()
        self.on_msg_body_changed()
        self.on_chat_blacklist_body_changed()
        self.on_admirer_blacklist_body_changed()

    def save_config(self):
        """ Сохраним конфиг в файл """

        logging.info('Сохраним конфиг в файл')
        logging.debug('Сохраним one_letter_index {0}; one_msg_index {1};'.format(self.one_letter_index, self.one_msg_index))

        with open(self.config_path, 'wb') as f:
            cPickle.dump(self.interval, f)
            cPickle.dump(self.timeaut, f)
            cPickle.dump(self.blacklist, f)
            cPickle.dump(self.repeat, f)
            cPickle.dump(self.mode, f)
            cPickle.dump(self.one_letter_index, f)
            cPickle.dump(self.one_msg_index, f)
            cPickle.dump(self.current_photo, f)
            cPickle.dump(self.letter_subject_raw, f)
            cPickle.dump(self.letter_body_raw, f)
            cPickle.dump(self.msg_body_raw, f)
            cPickle.dump(self.chat_blacklist_body_raw, f)
            cPickle.dump(self.admirer_blacklist_body_raw, f)
            cPickle.dump(self.style_index, f)

    def applySettings(self):
        """ Проверить правильность заполнения """

        logging.info('Проверить правильность заполнения')
        index = 0
        self.correct = True
        # self.on_letter_subject_changed()
        # self.on_letter_body_changed()
        # self.on_msg_body_changed()

        logging.debug('Проверка длинны тела письма')
        if len(self.letter_body):
            for string in self.letter_body:
                if string.length() < 200 and not string.isEmpty():
                    msg = u'Длинна письма № {0} меньше 200 символов'.format(self.letter_body.indexOf(string)+1)
                    self.correct = False
                    index = 2
        logging.debug('Проверка если тело пусто')
        if self.letter_body_raw.contains(QtCore.QRegExp("^\s+")) or self.letter_body_raw.toUtf8() == '':
            msg = u'Вы не заполнили тело письма!'
            self.correct = False
            index = 2
        logging.debug('Проверка если тема пуста')
        if not len(self.letter_subject) or self.letter_subject_raw.contains(QtCore.QRegExp("^\s+")) or self.letter_subject_raw.toUtf8() == '':
            msg = u'Укажите тему письма!'
            self.correct = False
            index = 2
        logging.debug('Проверка если сообщения пусты')
        if not len(self.msg_body) or self.msg_body_raw.contains(QtCore.QRegExp("^\s+")) or self.msg_body_raw.toUtf8() == '':
            msg = u'Заполните текст сообщеий!'
            self.correct = False
            index = 3

        if self.correct:
            logging.info('Все данные введены корректно')
            self.save_config()
            self.accept()
        else:
            logging.warning(msg)
            self.listWidget.setCurrentRow(index)
            QtGui.QMessageBox.warning(self, u'Ошибка', msg, QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.NoButton, QtGui.QMessageBox.NoButton)

            # Если все коррект сохраним буферизированные параметры

    def addToChatBlacklist(self, id):
        ''' Занести в черный список '''

        logging.info('Занесем ID в черный список чата')
        raw = self.plainTextEdit_chat_blacklist.toPlainText()
        raw.append('\n,----------\n')
        for x in id:
            raw.append('{0},\n'.format(x))
        self.plainTextEdit_chat_blacklist.setPlainText(raw)

    def addToAdmirerBlacklist(self, id):
        ''' Занести в черный список '''

        logging.info('Занесем ID в черный список поклонников')
        raw = self.plainTextEdit_admirer_blacklist.toPlainText()
        raw.append('\n,----------\n')
        for x in id:
            raw.append('{0},\n'.format(x))
        self.plainTextEdit_admirer_blacklist.setPlainText(raw)

    def populate(self):
        """ Отобразить фото пользователя """

        try:
            start_time = time.clock()
            for pic in self.pics:
                # Взять из кэша или скачать превью
                image = QtGui.QImage()
                image.loadFromData(self.cache(self.pics[pic]))
                # Вставка в виджет
                item = QtGui.QListWidgetItem()
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(image), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(icon)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable)
                item.setText(pic)
                self.listWidgetPic.addItem(item)
            logging.debug('Время выполнения запроса:{0}'.format(time.clock() - start_time))
        except Exception, e:
            logging.error(e)
            return False
        else:
            return True

    def cache(self, url):
        ''' Взять из кэша или скачать превью'''

        id = url.split('/')[-2]
        mypath = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.TempLocation)+'/Alisa-Sender/'+id+'/'
        mypath = str(mypath.toUtf8())
        # Проверить существование
        if not os.path.exists(mypath):
            os.makedirs(mypath)
        # Просмотреть кэш
        cache = []
        for (dirpath, dirnames, filenames) in os.walk(mypath):
            cache.extend(filenames)
            break
        # Формирование превью
        if 'https://www.bridge-of-love.com/' in url:
            list = url.split('/')
            img = list.pop()
            thumb = 'small_'+img
            list.append(thumb)
        # Загрузка превью
        path = mypath+thumb
        if thumb not in cache:
            # скачать
            url = '/'.join(list)
            g = Grab()
            g.go(url)
            g.doc.save(path)
            logging.debug('Из сети:{0}'.format(url))
        else:
            logging.debug('Из кэша:{0}'.format(path))

        with open(path, 'rb') as file:
            data = file.read()
            file.close()

        return data
