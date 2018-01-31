from urllib import request, parse
from app import config
import json

def add_user(username, password, api_key, domain):
    header = {'PddToken': api_key}
    data = parse.urlencode({'domain': domain, 'login': username, 'password': password}).encode()
    # data = 'domain={}&login={}&password={}'.format(domain, username, password)
    req = request.Request(url='https://pddimp.yandex.ru/api2/admin/email/add', data=data, method='POST', headers=header)
    resp = request.urlopen(req).read()
    return resp


def get_users(api_key, domain):
    header = {'PddToken': api_key}
    url = 'https://pddimp.yandex.ru/api2/admin/email/list?domain={}&page=1&on_page=150'.format(domain)
    req = request.Request(url=url, method='GET', headers=header)
    resp = request.urlopen(req).read()
    return resp


def get_user_info(users_raw):
    user_accounts = json.loads(users_raw.decode())['accounts']
    users = []
    for i in range(0, len(user_accounts)):
        user_raw = user_accounts[i]
        user = (user_raw['uid'], user_raw['login'], user_raw['iname'], user_raw['fname'])
        users.append(user)
    return users

def del_user(uid, api_key, domain):
    header = {'PddToken': api_key}
    data = parse.urlencode({'domain': domain, 'uid': uid,}).encode()
    req = request.Request(url='https://pddimp.yandex.ru/api2/admin/email/del', data=data, method='POST', headers=header)
    resp = request.urlopen(req).read()
    return resp

# add_user('test', 'test1234', config.KEY, config.DOMAIN)
#
users_response = get_users(config.KEY, config.DOMAIN)
print(get_user_info(users_response))

#
# del_user(1130000026629310, config.KEY, config.DOMAIN)
