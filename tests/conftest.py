"""Содержит тестовую конфигурацию, то что понадобится перед каждым тестом."""

import os
import tempfile

import pytest

from ..flasksite import create_app
from ..flasksite.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf-8')


# Фикстура app вызовет фабрику из __init__.py, которая создаст(сконфигурирует) приложение
# и тестовую БД, чтобы не обращаться к БД приложения.

@pytest.fixture
def app():
    # tempfile.mkstemp создает и открывает временный файл для создания БД и тестирования
    # по окончании тестовый файл будет закрыт и удален.
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        # TESTING - приложение в тестовом состоянии
        'TESTING': True,
        # Путь к временной базе, определенной выше
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


# Фикстура, чтобы формировать запросы к приложению без запуска сервера
@pytest.fixture
def client(app):
    return app.test_client()


# Фикстура, создает runner (бегуна) для тестирования CLI команд,
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

