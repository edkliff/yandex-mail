Small web-tool for yandex-pdd managment. 

1) Get yor yandex-pdd token/ tokens

2) create config.py in directory with yandex-mail

3) configure it like in template

**config.py structure:**
    
DOMAIN_KEY = {'domain_name_inside1': ('domain_name_in_yandex', 'yandex_pdd_api_key'),
              'domain_name_inside2': ('domain_name_in_yandex', 'yandex_pdd_api_key'),
              ...
              'domain_name_insideN': ('domain_name_in_yandex', 'yandex_pdd_api_key')}


class Config(object):
    SECRET_KEY = 'your-secret-key'
    
4) run app

5) enjoy simple creation with web-interface on http://your-server/ !