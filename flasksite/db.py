"""
Соединение с Базой Данных
"""
import sqlite3
import click
from flask import current_app, g


# Установить соединение с БД
def get_db():
    # Если соединение не установлено - установить.
    if 'db' not in g:
        # g - спец. объект, содержит все данные, которые могут быть использованы
        # функциями в ходе одного соединения с базой данных.
        g.db = sqlite3.connect(
            # current_app - еще один спец.объект, указывает Flask поддерживать соединение.
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row - возвращать Row, которые ведут себя как словари
        g.db.row_factory = sqlite3.Row

    return g.db


# Закрыть соединение с БД.
def close_db(e=None):
    # Есть ли в спец.объекте g значение по ключу 'db'? если нет, то верни None.
    db = g.pop('db', None)

    # Если соединение не закрыто - закрой.
    if db is not None:
        db.close()


# Инициализировать Базу данных
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Очистить существующие данные и создать новые таблицы."""
    init_db()
    click.echo('Initialized the database.')


# Регистрирует приложения. Принимает в качестве аргумента приложение.
def init_app(app):
    # Вызвать функцию во время очистки после получения ответа.
    app.teardown_appcontext(close_db)
    # Добавить новую комнаду.
    app.cli.add_command(init_db_command)




