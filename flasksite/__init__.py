"""
Данный файл выполняет 2 функции:
1) фабрика приложений;
2) сообщает Python, что с директорией flasksite следует обращаться как с пакетом.
"""
import os

from flask import Flask

from . import db
from . import auth

# Фабричная функция по созданию приложений.
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # Конфигурация, которую приложение будет использовать по умолчанию, если не передать других настроек.
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasksite.sqlite'),
    )

    if test_config is None:
        # Если есть конфигурация в файле config.py взять настройки оттуда.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Если нет, то использовать настройки по умолчанию.
        app.config.from_mapping(test_config)

    # Проверка, что папка приложения существует.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Простое представление.
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Инициализировать приложение.
    db.init_app(app)

    # Зарегистрировать чертеж под названием auth
    app.register_blueprint(auth.bp)

    return app


