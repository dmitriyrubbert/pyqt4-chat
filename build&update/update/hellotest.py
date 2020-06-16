import requests


class BridgeAPI(object, requests):

    def __init__(self, login, password, *args, **kwargs):
        self.login = login
        self.password = password

        url='https://www.bridge-of-love.com/login.html'
        post={
            'key': '4109294306',
            'user_name': login,
            'password': password,
            'remember': 'on',
            'ret_url': ''
            }
        # return self.post(url, post).text
        # text,url, raw, requrest, status_code, url, links, json, headers, cookie, content

    def authCheck(self):
        if login in self.text:
            print('Authorized')
            return True

if __name__ == "__main__":
  login='demo@mail.ru'
  password = 'demo'
  BridgeAPI(login, password)
  # b.authCheck()
