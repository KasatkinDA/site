from flask_wtf import FlaskForm
from typing_extensions import ReadOnly
from wtforms import StringField, SubmitField, TextAreaField,  BooleanField, PasswordField, TelField
from wtforms.validators import DataRequired, Email, EqualTo, Disabled


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Войти")
    regist = SubmitField("Регистрация")

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
