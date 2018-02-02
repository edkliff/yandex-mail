# Small web-tool for yandex-pdd managment
Small and simple tool for managment of yandex-pdd mails. 
It can create new mail acoount, delete it, show you list of mail accounts. 
So, you can connect 1 and more domains to this tool.


## Features
1) List your domains accounts
2) Create, remove or edit accounts on your domain
3) Several domains in one tool

## Installation
1) Get your yandex-pdd token/tokens
2) Сreate config.py in directory with yandex-mail
3) Сonfigure it like in template
### config.py structure:
```
DOMAIN_KEY = {'domain_name_inside1': ('domain_name_in_yandex', 'yandex_pdd_api_key'),
              'domain_name_inside2': ('domain_name_in_yandex', 'yandex_pdd_api_key'),
              ...
              'domain_name_insideN': ('domain_name_in_yandex', 'yandex_pdd_api_key')}


class Config(object):
    SECRET_KEY = 'your-secret-key'
```
4) Run app
5) Enjoy simple creation with web-interface on http://your-server:5000/

### WARNING!
It's not secure tool, and i don't use authorization
