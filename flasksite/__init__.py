"""
Создает приложение, инициализирует Базу Данных, регистрирует Blueprints, содержащие views
"""
import os

from flask import Flask

from . import db, blog
from . import auth


# Фабричная функция по созданию приложений и базы данных к нему.
def create_app(test_config=None):
    # Создаем экземпляр фласка с именем из директории
    app = Flask(__name__, instance_relative_config=True)
    # Конфигурация, которую приложение будет использовать по умолчанию, если не передать других настроек.
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasksite.sqlite'),
    )

    # Проверка переданы ли конфиги через 'config.py' или нет.
    if test_config is None:
        # Если есть конфигурация в файле 'config.py' взять настройки оттуда.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Если нет, то использовать настройки по умолчанию.
        app.config.from_mapping(test_config)

    # Проверка, что папка приложения существует. Проверка пути к теущей директории.
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

    # Зарегистрировать чертеж под названием blog
    app.register_blueprint(blog.bp)
    # Blueprint blog не имеет префикса, поэтому index view будет на '/'
    app.add_url_rule('/', endpoint='index')

    return app


