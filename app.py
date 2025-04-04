from config import app, render_template, db
from classes import *
from flask_login import   login_required, login_user, current_user, logout_user
from forms import (LoginForm, RegisterForm, AddOrganization, FilterOrg, CreateTicket,
                   RegistrationForm, EditUserForm, EditOrganizationForm)
from flask import  render_template, request, redirect, url_for,  flash, session, jsonify, abort



with app.app_context():
    db.create_all()


@app.route('/')
@login_required
def index():  # put application's code here
    return render_template('index.html')


"""Модуль пользователей"""
@app.route('/registration', methods=['GET', 'POST'])
@login_required
def registration():
    """Тут должна быть форма по которой мы выдаем юзеру логин и пароль"""
    form = RegisterForm()
    if form.validate_on_submit():

        # user_model = db.session.query(Temp_user).filter_by(name=username).first()
        user = User(
            username=form.username.data,
            role=form.role.data,
            login=form.login.data)
        user.set_password(form.password.data)

        db.session.add(user)
        # db.session.delete(user_model)
        db.session.commit()
        # db.insert(User).values(name=username, login=login, password=password, role=role)

        # print(username, login, password, role)
        return render_template('index.html', sms=f'Пользователь {username} успешно добавлен.')


    users = db.session.query(Temp_user).all()
    return render_template("registration.html", form=form, users=users)

@app.route('/searchUser')
@login_required
def searchUser():
    return render_template("index.html")




@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template("admin.html")





"""Модуль заявок"""
@app.route('/newCreateOrder', methods=("POST", "GET"))
@login_required
def newCreateOrder():
    brigades = Teams.query.all()
    organization = Organizations.query.all()
    form = CreateTicket()
    # if form.validate_on_submit():

    return render_template('create-order.html', organization=organization, brigades=brigades, form=form)


@app.route('/get_organization_details', methods=['GET'])
@login_required
def get_organization_details():
    organization_name = request.args.get('organization_name')
    organization = Organizations.query.filter_by(name=organization_name).first()
    if organization:
        return jsonify({'city': organization.city,'phone1': organization.phone1, 'phone2': organization.phone2, 'phone3': organization.phone3,
                        'address': organization.adress, 'comment': organization.komment})
    return jsonify({'error': 'Организация не найдена'})


@app.route('/searchOrder')
@login_required
def searchOrder():
    return render_template("index.html")

@app.route('/orders')
@login_required
def orders():
    return render_template("index.html")










"""Модуль бригад"""
@app.route('/newCreateBrigade')
@login_required
def newCreateBrigade():
    return render_template("index.html")

@app.route('/editBrigade')
@login_required
def editBrigade():
    return render_template("index.html")









"""Модуль организации"""


@app.route('/search_org', methods=['GET'])
@login_required
def search_org():
    # Параметры фильтрации
    name = request.args.get('name', '').strip()
    city = request.args.get('city', '').strip()
    address = request.args.get('address', '').strip()
    phone = request.args.get('phone', '').strip()

    # Базовый запрос
    query = Organizations.query

    # Фильтры
    if name:
        query = query.filter(Organizations.name.ilike(f'%{name}%'))
    if city:
        query = query.filter(Organizations.city.ilike(f'%{city}%'))
    if address:
        query = query.filter(Organizations.adress.ilike(f'%{address}%'))  # Исправьте на 'address' если нужно
    if phone:
        query = query.filter(
            (Organizations.phone1.ilike(f'%{phone}%')) |
            (Organizations.phone2.ilike(f'%{phone}%')) |
            (Organizations.phone3.ilike(f'%{phone}%'))
        )

    organizations = query.all()
    return render_template('search-org.html', organizations=organizations)


@app.route('/data')
@login_required
def data():
    form = FilterOrg()
    organizations = Organizations.query.all()
    # org_list = [org.to_dict() for org in organizations]

    return jsonify([org.to_dict() for org in organizations])



@app.route('/createOrg', methods=("POST", "GET"))
@login_required
def createOrg():
    form = AddOrganization()
    cities = db.session.query(Cities).all()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            city = form.city.data
            adress = form.adress.data
            phone1 = form.phone1.data
            phone2 = form.phone2.data
            phone3 = form.phone3.data
            komment = f"{session['name']}({session['role']}):\n---\n{form.koment.data}\n---"

            organization = Organizations(name=name, city=city, adress=adress, phone1=phone1, phone2=phone2, phone3=phone3, komment=komment)
            db.session.add(organization)
            db.session.commit()
        else:
            flash('Исправьте ошибки в форме', 'error')
        return render_template('index.html', sms=f"Организация - {name} добавлена")

    return render_template("create_org.html", form=form, cities=cities)










@app.route('/logout/')
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))

@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.login == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            session['name'] = user.username
            session['role'] = user.role


            return redirect(url_for('index'))

        flash("Invalid username/password", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()  # Убедитесь в скобках!

    if form.validate_on_submit():
        try:
            # Проверка уникальности логина
            existing_user = User.query.filter_by(login=form.username.data).first()
            if existing_user:
                flash('Логин уже занят', 'error')
                return render_template('register.html', form=form)

            user = User(
                login=form.login.data,
                username=form.username.data,
                role='Пользователь'
            )
            user.set_password(form.password.data)


            db.session.add(user)
            db.session.commit()

            flash('Регистрация успешна! Теперь войдите', 'success')
            return redirect(url_for('login'))  # Редирект после успеха

        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Ошибка регистрации: {str(e)}')  # Логируем ошибку
            flash('Ошибка базы данных', 'error')

    # Добавляем вывод ошибок валидации
    for field, errors in form.errors.items():
        for error in errors:
            app.logger.warning(f'Ошибка в поле {field}: {error}')

    return render_template('register.html', form=form)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'Администратор':
        abort(403)

    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    form.team_id.choices = [(t.team_id, t.name) for t in Teams.query.all()]  # Заполняем список бригад
    form.user_id = user.id

    if form.validate_on_submit():
        try:
            user.username = form.username.data
            user.login = form.login.data
            user.role = form.role.data
            user.team_id = form.team_id.data or None
            user.phone1 = form.phone1.data
            user.phone2 = form.phone2.data
            user.ban = "banned" if form.is_banned.data else None  # Сохраняем статус блокировки

            if form.new_password.data:
                user.set_password(form.new_password.data)

            db.session.commit()
            flash('Данные обновлены!', 'success')
            return redirect(url_for('user_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка: {str(e)}', 'danger')

    # Для чекбокса блокировки
    form.is_banned.data = bool(user.ban)
    return render_template('edit_user.html', form=form, user=user)


@app.route('/users')
@login_required
def user_list():
    if current_user.role != 'Администратор':
        abort(403)
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/edit_org/<int:org_id>', methods=['GET', 'POST'])
@login_required
def edit_org(org_id):
    # Только администраторы и ответственные
    if current_user.role != 'Администратор':
        abort(403)

    org = Organizations.query.get_or_404(org_id)
    form = EditOrganizationForm(obj=org)

    if form.validate_on_submit():
        try:
            org.name = form.name.data
            org.city = form.city.data
            org.adress = form.adress.data
            org.phone1 = form.phone1.data
            org.phone2 = form.phone2.data
            org.phone3 = form.phone3.data
            org.komment = form.komment.data

            db.session.commit()
            flash('Организация обновлена!', 'success')
            return redirect(url_for('search_org'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка: {str(e)}', 'danger')

    return render_template('edit_org.html', form=form, org=org)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)