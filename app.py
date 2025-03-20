from config import app, render_template, db
from classes import *
from flask_login import   login_required, login_user, current_user, logout_user
from forms import LoginForm, RegisterForm, AddOrganization, FilterOrg, CreateTicket
from flask import  render_template, request, redirect, url_for,  flash, session, jsonify



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
        username = form.username.data
        login = form.login.data
        password = form.password.data
        role = form.role.data
        password = generate_password_hash(password=password)
        # user_model = db.session.query(Temp_user).filter_by(name=username).first()
        user = User(username=username, role=role, login=login, password_hash=password)
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

@app.route('/searchOrg')
@login_required
def search_org():
    return render_template('search-org.html')


@app.route('/data')
@login_required
def data():
    form = FilterOrg()
    organizations = Organizations.query.all()
    # org_list = [org.to_dict() for org in organizations]

    return jsonify([org.to_dict() for org in organizations])

@app.route('/filter', methods=['GET', 'POST'])
@login_required
def filter():
    form = FilterOrg()
    if form.validate_on_submit():
        name = form.name.data
        city = form.city.data
        adress = form.adress.data
        phone = form.phone.data
        organization = Organizations.query.filter_by(name=name, city=city, adress=adress, phone1=phone).all()
        return render_template('table_body.html', users=users)

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






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)