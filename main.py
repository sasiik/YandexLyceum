import json

from flask import Flask, url_for, request, render_template, redirect

from loginform import LoginForm

app = Flask(__name__)


@app.route('/<string:title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof):
    images = [url_for('static', filename="img/mars.png"), url_for('static', filename="img/riana.jpeg")]
    return render_template('training.html', title=prof, prof=prof, images=images)


@app.route('/list_prof/<list>')
def list_prof(list):
    profs = ['Инженер', "Строитель", "Врач", "Механик", "Пилот"]
    return render_template('list_prof.html', title='Job list', list_type=list, profs=profs)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    form_data = {'title': 'Form',
                 "surname": 'Wanty',
                 "name": 'Mark',
                 "education": 'School',
                 "profession": 'Doctor',
                 "sex": 'Male',
                 "motivation": "Want to live on Mars",
                 "ready": "Yes!"}
    return render_template('answer.html', title=form_data['title'], form_data=form_data)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form, title='Авторизация')


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.run(port=8080, host='127.0.0.1')
