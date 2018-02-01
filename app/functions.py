import json
from urllib import request, parse


def add_user(username, password, api_key, domain):
    header = {'PddToken': api_key}
    data = parse.urlencode({'domain': domain,
                            'login': username,
                            'password': password}).encode()
    req = request.Request(url='https://pddimp.yandex.ru/api2/admin/email/add',
                          data=data, method='POST', headers=header)
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
    users.extend(tuple(map(lambda account: (account['uid'],
                                            account['login'],
                                            account['iname'],
                                            account['fname'],
                                            account['enabled']), user_accounts)))
    return users


def delete_user(uid, api_key, domain):
    header = {'PddToken': api_key}
    data = parse.urlencode({'domain': domain, 'uid': uid,}).encode()
    req = request.Request(url='https://pddimp.yandex.ru/api2/admin/email/del',
                          data=data, method='POST', headers=header)
    resp = request.urlopen(req).read()
    return resp


def edit_user(uid, name, sname, enabled, api_key, domain):
    header = {'PddToken': api_key}
    data = parse.urlencode({'domain': domain, 'uid': uid, }).encode()


def response_parse(response):
    response_dict = json.loads((response.decode()))
    return response_dict
