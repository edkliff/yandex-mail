import json
from urllib import request, parse
from flask import flash
import config
from datetime import datetime

def add_user(username, password, api_key, domain):
    """
    Yandex API POST request for user creation

    :param username: username for new user
    :param password: password for new user
    :param api_key: Yandex API Key
    :param domain: domain in Yandex PDD
    :return: HTTP response
    """
    header = {'PddToken': api_key}
    data = parse.urlencode({'domain': domain,
                            'login': username,
                            'password': password}).encode()
    req = request.Request(url='https://pddimp.yandex.ru/api2/admin/email/add',
                          data=data, method='POST', headers=header)
    resp = request.urlopen(req).read()
    return resp


def get_birthday(date):
    if date:
        return datetime.strptime(date, '%Y-%m-%d')
    return ''

def get_users(api_key, domain):
    """
    Get users list by domain with Yandex API

    :param api_key: Yandex API Key
    :param domain: domain in Yandex PDD
    :return: list of users
    0 - uid, 1 - login, 2 - name, 3 - second name, 4- enabled, 5 - login,
    6 - birthday, 7 - sex, 8 - hintq, 9 - ready, 10 - fio,
    12 - aliases(in future)
    """
    header = {'PddToken': api_key}
    url = 'https://pddimp.yandex.ru/api2/admin/email/list?domain={}&page=1&on_page=150'.format(domain)
    req = request.Request(url=url, method='GET', headers=header)
    resp = request.urlopen(req).read()
    user_accounts = json.loads(resp.decode())['accounts']
    users = []
    ## !!!!NEED REWRITE FOR DICT!!!!
    users.extend(tuple(map(lambda account: (account['uid'],
                                            account['login'],
                                            account['iname'],
                                            account['fname'],
                                            user_enabled_parser(account['enabled']),
                                            domain_from_login(account['login']),
                                            get_birthday(account['birth_date']),
                                            account['sex'], account['hintq'],
                                            account['ready'], account['fio']),
                           user_accounts)))
    return users


def delete_user(uid, api_key, domain):
    """
    Yandex API POST request for user deletion

    :param uid: user id in Yandex
    :param api_key: Yandex API Key
    :param domain: domain in Yandex PDD
    :return: HTTP response
    """
    header = {'PddToken': api_key}
    data = parse.urlencode({'domain': domain, 'uid': uid}).encode()
    req = request.Request(url='https://pddimp.yandex.ru/api2/admin/email/del',
                          data=data, method='POST', headers=header)
    resp = request.urlopen(req).read()
    return resp


def edit_user(uid, name, sname, enabled, api_key, domain, birthday, gender, hintq, hinta):
    """
    User editing with Yandex API, you can change name, last name, enable or disable user

    :param uid: user id in Yandex
    :param name: real name for user
    :param sname: Last name for user
    :param enabled: enabled in bool
    :param api_key: Yandex API Key
    :param domain: domain in Yandex PDD
    :return: HTTP Response
    """
    enabled = user_enabled_changer(enabled)
    header = {'PddToken': api_key}
    data_dict = {'domain': domain, 'uid': uid,
                 'iname': name, 'fname': sname,
                 'enabled': enabled, 'birth_date': str(birthday),
                 'sex': gender, 'hintq': hintq}
    if hinta != 'no' and hinta != 'yes':
        data_dict.update({'hinta': hinta})
    print(hinta)

    data = parse.urlencode(data_dict).encode()
    req = request.Request(url='https://pddimp.yandex.ru/api2/admin/email/edit',
                          data=data, method='POST', headers=header)
    resp = request.urlopen(req).read()
    return resp


def domain_from_login(address):
    """
    Get domain with user login with split magick

    :param address: user e-mail address
    :return: domain name without zone

    Split by '@', then second element split by '.', then get first element
    """
    return address.split('@')[1].split('.')[0]


def user_enabled_parser(enabled):
    """
    :param enabled: enabled in Yandex-style
    :return: enabled in bool
    """
    if enabled == 'yes':
        return True
    return False


def user_enabled_changer(enabled):
    """
    :param enabled: enabled in bool
    :return: enabled in Yandex-style
    """
    if enabled:
        return 'yes'
    return 'no'


def console_output(response, process):
    """
    HTTP Response parsing.
    :param response: HTTP response
    :param process: process(creation, deletion, editing, etc), string
    :return: 0
    """
    resp = json.loads((response.decode()))
    if resp['success'] == 'ok':
        flash('{} was finished with status {}, User: {}, UID: {}'
              .format(process, resp['success'], resp['login'],
                      resp['uid'] if resp.get('uid') else 'Not defined'))
    else:
        flash('{} was finished with status {}, Error decription: {}'
              .format(process, resp['success'], resp['error']))
    return 0


def find_user_in_lists(user_id, users_list):
    """
    Find user in list of all users
    :param user_id: user_id, int. We find user with this id
    :param users_list: List of all users
    :return: user account data, his domain and domain APIKey/domain name
    """
    for user in users_list:
        if user[0] == user_id:
            account = user
            domain = domain_from_login(user[1])
            domain_data = config.DOMAIN_KEY[domain]
            return account, domain, domain_data
