import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    OAUTH_CREDENTIALS = {
        'vk': {
            'id': '51670256',
            'secret': 'dFxnlpVsOAxf46FNmgiV'
        }
    }
