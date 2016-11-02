# -*- coding: utf-8 -*-


"""
tests.settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Contains the settings to be used when running the test suite.
"""


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django_localflavor_br',
]

SECRET_KEY = '_e1f4wee)*kq5(!c_%xc35_wak1f7uxk6ae=^)tf&4_8q%pj3m'
