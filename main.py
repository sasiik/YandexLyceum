import datetime

from flask import Flask, render_template, redirect, make_response, request, abort
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.news import News
from forms.job import JobsForm
from forms.loginform import LoginForm
from forms.news import NewsForm
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).all()
    print(news)
    return render_template("index.html", news=news)


@app.route("/jobs")
def jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("jobs.html", jobs=jobs)


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
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data

        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/addjob', methods=['GET', "POST"])
@login_required
def addjob():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        current_user.jobs.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/jobs')
    return render_template('addjob.html', title='Добавление работы',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


# scott = ['Scott', 'Ridley', 21, 'captain', 'research engineer', 'module_1', 'scott_chief@mars.org']
# mark = ['Scott', 'Mark', 20, 'colonist', 'doctor', 'module_2', 'mark_doctor@mars.org']
# drake = ['White', 'Drake', 27, 'colonist', 'scientist', 'module_3', 'drake21@mars.org']
# mike = ['Trump', 'Mike', 18, 'colonist', 'intern', 'module_4', 'mikesavage@mars.org']
#
# team = [scott, mark, drake, mike]


def main():
    db_session.global_init("db/jobs.db")
    # if not db_sess.query(User).first():
    #     for member in team:
    #         user = User()
    #         user.surname = member[0]
    #         user.name = member[1]
    #         user.age = member[2]
    #         user.position = member[3]
    #         user.speciality = member[4]
    #         user.address = member[5]
    #         user.email = member[6]
    #         db_sess.add(user)
    #     db_sess.commit()
    # if not db_sess.query(Jobs).first():
    #     job = Jobs()
    #     job.team_leader = 1
    #     job.job = 'deployment of residential modules 1 and 2'
    #     job.work_size = 15
    #     job.collaborators = '2, 3'
    #     job.start_date = datetime.datetime.now()
    #     job.is_finished = False
    #     db_sess.add(job)
    #     db_sess.commit()
    #
    # for user in db_sess.query(User).all():
    #     print(user)
    #
    # for job in db_sess.query(Jobs).all():
    #     print(job)


if __name__ == '__main__':
    main()
    app.run()
