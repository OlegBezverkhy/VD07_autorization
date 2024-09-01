from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import app, db
from app.forms import RegistrationForm, LoginForm, UpdateRegistrationForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация нового пользователя')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вы успешно вошли в систему')
            return redirect(url_for('home'))
            flash('Введены неверные данные', 'danger')
    return render_template('login.html', form=form, title='Вход пользователя в систему')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateRegistrationForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Ваши регистрационные данные обновлены!', 'success')
        return redirect(url_for('profile'))
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('profile.html', form=form)
