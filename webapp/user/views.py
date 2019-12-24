from flask import Blueprint, flash, current_app, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user
from webapp.db import db

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.utils import get_redirect_target

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(get_redirect_target())
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)

@blueprint.route('/process_login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно залогинились на сайте')
            return redirect(get_redirect_target())
    flash('Неверно введен логин или пароль')
    return redirect(url_for('user.login')) 

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('news.index'))

@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Регистрация'
    form = RegistrationForm()
    return render_template('user/registration.html', page_title=title, form=form)

@blueprint.route('/process_reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        news_user = User(username=form.username.data, email=form.email.data, role='user')
        news_user.set_password(form.password.data)
        db.session.add(news_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form, field).label.text}: {error}')
        return redirect(url_for('user.register'))

    flash('Исправьте ошибки и попробуйте снова')
    return redirect(url_for('user.register'))