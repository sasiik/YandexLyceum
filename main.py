import datetime

from flask import Flask, render_template, redirect
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.news import News
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    for item in jobs:
        print(item.work_size)
    return render_template("index.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


scott = ['Scott', 'Ridley', 21, 'captain', 'research engineer', 'module_1', 'scott_chief@mars.org']
mark = ['Scott', 'Mark', 20, 'colonist', 'doctor', 'module_1', 'mark_doctor@mars.org']
drake = ['White', 'Drake', 27, 'colonist', 'scientist', 'module_2', 'drake21@mars.org']
mike = ['Trump', 'Mike', 18, 'colonist', 'intern', 'module_2', 'mikesavage@mars.org']

team = [scott, mark, drake, mike]


def main(db_path):
    db_session.global_init(db_path)
    db_sess = db_session.create_session()
    if not db_sess.query(User).first():
        for member in team:
            user = User()
            user.surname = member[0]
            user.name = member[1]
            user.age = member[2]
            user.position = member[3]
            user.speciality = member[4]
            user.address = member[5]
            user.email = member[6]
            db_sess.add(user)
        db_sess.commit()
    if not db_sess.query(Jobs).first():
        job = Jobs()
        job.team_leader = 1
        job.job = 'deployment of residential modules 1 and 2'
        job.work_size = 15
        job.collaborators = '2, 3'
        job.start_date = datetime.datetime.now()
        job.is_finished = False
        db_sess.add(job)
        db_sess.commit()

    for user in db_sess.query(User).filter(User.address == 'module_1', User.speciality.notlike('%engineer%'),
                                           User.position.notlike('%engineer%')):
        print(user.id)


if __name__ == '__main__':
    main('db/jobs.db')
    app.run()
