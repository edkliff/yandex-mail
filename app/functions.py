import json
from urllib import request, parse
from flask import flash


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
                                            user_enabled_parser(account['enabled']),
                                            domain_from_login(account['login'])),
                           user_accounts)))
    return users


def delete_user(uid, api_key, domain):
    header = {'PddToken': api_key}
    data = parse.urlencode({'domain': domain, 'uid': uid}).encode()
    req = request.Request(url='https://pddimp.yandex.ru/api2/admin/email/del',
                          data=data, method='POST', headers=header)
    resp = request.urlopen(req).read()
    return resp


def edit_user(uid, name, sname, enabled, api_key, domain):
    enabled = user_enabled_changer(enabled)
    header = {'PddToken': api_key}
    data = parse.urlencode({'domain': domain, 'uid': uid,
                            'iname': name, 'fname': sname,
                            'enabled': enabled}).encode()
    print(data)
    req = request.Request(url='https://pddimp.yandex.ru/api2/admin/email/edit',
                          data=data, method='POST', headers=header)
    resp = request.urlopen(req).read()
    return resp


def response_parse(response):
    response_dict = json.loads((response.decode()))
    return response_dict


def domain_from_login(login):
    return login.split('@')[1].split('.')[0]


def user_enabled_parser(enabled):
    if enabled == 'yes':
        return True
    return False


def user_enabled_changer(enabled):
    if enabled:
        return 'yes'
    return 'no'


def console_output(response, process):
    resp = response_parse(response)
    if resp['success'] == 'ok':
        flash('{} was finished with status {}, User: {}, UID: {}'
              .format(process, resp['success'], resp['login'],
                      resp['uid'] if resp.get('uid') else 'Not defined'))
    else:
        flash('{} was finished with status {}, Error decription: {}'
              .format(process, resp['success'], resp['error']))