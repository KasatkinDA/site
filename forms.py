from flask_wtf import FlaskForm
from typing_extensions import ReadOnly
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    TelField,
    TextAreaField,
    BooleanField,
    SelectField
)
from wtforms.validators import DataRequired, Email, EqualTo, Disabled, Optional, ValidationError, Length
from classes import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Войти")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    login = StringField("Login", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    password_again = StringField("<PASSWORD>", validators=[DataRequired(), EqualTo("password", message="Пароли не совпадают")])
    role = StringField("Role", validators=[DataRequired()])
    submit = SubmitField("Зарегистрировать")

class AddOrganization(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    city = StringField("Город", validators=[DataRequired()])
    adress = StringField("Адрес", validators=[DataRequired()])
    phone1 = TelField("Телефон", validators=[DataRequired()])
    phone2 = TelField("Телефон")
    phone3 = TelField("Телефон")
    koment = TextAreaField("Комментарий")
    submit = SubmitField("Создать")

class FilterOrg(FlaskForm):
    name = StringField("name")
    city = StringField("city")
    adress = StringField("adress")
    phone = TelField("phone1")
    submit = SubmitField("Найти")


class CreateTicket(FlaskForm):
    organization = StringField("Выберите организацию", validators=[DataRequired()])
    city = StringField("Город")
    phone1 = TelField("Телефон")
    phone2 = TelField("Телефон")
    phone3 = TelField("Телефон")
    adress = StringField("Адрес")
    komment = TextAreaField("Коментарий")
    new_komment = TextAreaField("Новый комментарий")
    submit = SubmitField("Создать")


class EditUserForm(FlaskForm):
    username = StringField('ФИО', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    role = SelectField(
        'Роль',
        choices=[
            ('user', 'Пользователь'),
            ('admin', 'Администратор'),
            ('technician', 'Техник'),
            ('responsible', 'Ответственный')
        ],
        validators=[DataRequired()]
    )
    team_id = SelectField(  # Если есть список бригад
        'Бригада',
        coerce=int,
        choices=[],
        validators=[Optional()]
    )
    phone1 = StringField('Телефон 1', validators=[Optional(), Length(max=15)])
    phone2 = StringField('Телефон 2', validators=[Optional(), Length(max=15)])
    new_password = PasswordField('Новый пароль', validators=[Optional()])
    confirm_password = PasswordField('Повторите пароль', validators=[
        EqualTo('new_password', message='Пароли должны совпадать')
    ])
    is_banned = BooleanField('Заблокировать пользователя')
    submit = SubmitField('Сохранить')


from wtforms.validators import Optional, Length

class EditOrganizationForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    adress = StringField('Адрес', validators=[DataRequired()])
    phone1 = StringField('Телефон 1', validators=[Optional(), Length(max=15)])
    phone2 = StringField('Телефон 2', validators=[Optional(), Length(max=15)])
    phone3 = StringField('Телефон 3', validators=[Optional(), Length(max=15)])
    komment = TextAreaField('Комментарий', validators=[Optional()])
    submit = SubmitField('Сохранить изменения')