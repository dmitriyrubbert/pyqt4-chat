# -*- coding: utf-8 -*-
from grab import Grab
import logging
import os


def checkAuthorization(login, password):
    '''Проверка авторизации'''

    print('Проверка авторизации')
    key = '4109294306'

    # Для начала нужно создать обьект граб
    grab = Grab(
        timeout=50, 
        connect_timeout=25, 
        url='https://www.bridge-of-love.com/login.html',
        debug_post='True',
        log_dir='log'
        )

    # Затемзалогинится на сайте
    #  debug 120916
    #------------------------------------------------
    # grab.setup(post={'user_name': login.toUtf8(), 'password': password.toUtf8(), 'remember': 'on', 'ret_url': ''})
    grab.setup(post={'key': key, 'user_name': login, 'password': password, 'remember': 'on', 'ret_url': ''})
    #------------------------------------------------

    # Отправка формы
    grab.request()

    print(dir(grab.doc))

    # Проверка авторизации
    if not grab.doc.text_search(unicode(login)):
        print('Ошибка авторизации!')
        msg = u'Неправильный логин или пароль. Проверьте все еще раз и повторите ввод!'
        #  debug 120916
        #------------------------------------------------
        print(grab.doc.select('//title').text())
        #------------------------------------------------

    else:
        print('Успешно')
        print(grab.doc.select('//title').text())
    

if not os.path.exists('./log'):
    os.makedirs('./log')

login='demo@mail.ru'
password = 'demo'
checkAuthorization(login, password)

