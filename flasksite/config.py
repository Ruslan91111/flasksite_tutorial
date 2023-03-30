import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# Конфигурация
DATABASE = '/tmp/flasksite.db'
DEBUG = True
SECRET_KEY = 'supersecretkey'
USERNAME = 'admin'
PASSWORD = '12345'


app = Flask(__name__)
app.config.from_object(__name__)

# Загружаем конфиг по умолчанию и переопределяем в конфигурации часть
# значений через переменную окружения
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flasksite.db'),
    DEBUG=True,
    SECRET_KEY='supersecretkey',
    USERNAME='admin',
    PASSWORD='12345'
))
app.config.from_envvar('FLASKSITE_SETTINGS', silent=True)
