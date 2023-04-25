from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Работа', validators=[DataRequired()])
    team_leader = IntegerField('Тим-лидер (id)', validators=[DataRequired()])
    work_size = StringField("Размер работы (часов)", validators=[DataRequired()])
    collaborators = StringField('ID Участников (через запятую)', validators=[DataRequired()])
    is_finished = BooleanField('Завершена ли работа?')
    submit = SubmitField('Применить')
