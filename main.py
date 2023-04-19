import json

from flask import Flask, url_for, request, render_template, redirect

from loginform import LoginForm

app = Flask(__name__)


@app.route('/<string:title>')
def index(title):
    return render_template('base.html', title=title)

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(port=8080, host='127.0.0.1')

