from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin

from config import db, app, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) #id пользователя в базе
    user_id = db.Column(db.String(50), unique=True) #Telegram chat_id пользователя
    username = db.Column(db.String(50)) #Имя и фамилия
    role = db.Column(db.String(15)) #Роль в программе
    team_id = db.Column(db.Integer) #Id бригады если он техник
    phone1 = db.Column(db.String(15)) #Телефон юзера номер 1
    phone2 = db.Column(db.String(15)) #Телефон юзера номер 2. Необязателен
    login = db.Column(db.String(15)) #Логин юзера
    password_hash = db.Column(db.String(300)) #Пароль в хэше юзера
    ban = db.Column(db.String(50))

    def __repr__(self):
        return f"User(id={self.id}, user_id={self.user_id}, username={self.username}, role={self.role})"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Organizations(db.Model):
    org_id = db.Column(db.Integer, primary_key=True) #Id организации в базе
    name = db.Column(db.String(50)) #Имя организации
    city = db.Column(db.String(50)) #Город в котором находится организация
    adress = db.Column(db.String(50))  # Адрес организации
    phone1 = db.Column(db.String(15)) #Телефон организации. Доп номера будут браться из профиля ответственных
    phone2 = db.Column(db.String(15))  # Телефон организации. Доп номера будут браться из профиля ответственных
    phone3 = db.Column(db.String(15))  # Телефон организации. Доп номера будут браться из профиля ответственных
    komment = db.Column(db.String(500)) #Коментарии к организации. Доступны только для техников

    def to_dict(self):  # Преобразование объекта в словарь
        return {
            'id': self.org_id,
            'name': self.name,
            'city': self.city,
            'adress': self.adress,
            'phone1': self.phone1,
            'komment': self.komment
        }

    def __repr__(self):
        return f"<organizations {self.org_id}>"


class Teams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True) #ID бригады в базе
    name = db.Column(db.String(15)) #Имя для бригады

    def __repr__(self):
        return f"<teams {self.team_id}>"


class Contact_person(db.Model):
    org_id = db.Column(db.Integer, primary_key=True) #ID огранизации из таблицы "Organizations"
    contact_person = db.Column(db.Integer) #ID пользователя из таблицы "Users"

    def __repr__(self):
        return f"<contact_person {self.org_id}>"


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True) #ID заявки в базе. Генерируется строго по порядку
    description = db.Column(db.String(500)) #Описание заявки отправленное ответственным
    status = db.Column(db.String(20)) #Статус отработки заявки
    created_at = db.Column(db.DateTime, default=datetime.now) #Дата создания заявки
    update_at = db.Column(db.DateTime) #Дата обновления заявки. Обновляется каждый раз как изменить заявку.
    org_id = db.Column(db.Integer) #ID организации для которой поступила заявка
    team_id = db.Column(db.Integer) #ID бригады на которую назначили заявку
    komments = db.Column(db.String(500)) #Коментарий к заявке. Указывается техником.
    author = db.Column(db.Integer) #Создатель заявки, ID юзера в таблице Users. По возможности надо чтобы отображалась вся инфа.

    def __repr__(self):
        return f"<task {self.task_id}>"

class Temp_user(db.Model):
    __tablename__ = 'temp_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    name = db.Column(db.String(50))
    def __repr__(self):
        return f"<temp user {self.user_id}>"

class Cities(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    def __repr__(self):
        return f"<city {self.name}"

