from flask import Flask, url_for

# Создаем экземпляра класса Flask с именем myapp
app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    # Режим отладки
    app.debug = True
    app.run()

