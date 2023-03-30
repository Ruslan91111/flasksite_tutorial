# Не относится к приложение - просто hello world на Flask
from flask import Flask, url_for

# Создаем экземпляра класса Flask с именем myapp
app = Flask(__name__)


# @app.route - декоратор маршрут для view
# methods=[перечень видов запросов, которые могут использоваться]
@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Index Page'


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return 'Hello World'


if __name__ == '__main__':
    # Режим отладки
    app.debug = True
    app.run()

