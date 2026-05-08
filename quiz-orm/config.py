import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DATABASE = os.path.join(basedir, 'quiz.sqlite')
    SECRET_KEY = 'bradzosekretnawartosc'
    SITE_NAME = 'Quiz Python'