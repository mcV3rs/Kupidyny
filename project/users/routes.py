import datetime
import os

import sqlalchemy as sa
from flask import (current_app, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import update

from project import db
from project.models import User, UserWedding, Wedding
from . import users_blueprint
from .forms import LoginForm, RegisterForm


# Routes
@users_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Zmiana danych wesela
    if request.method == "POST":
        user_wedding = UserWedding.query.filter_by(user_id=current_user.id).first()
        wedding = user_wedding.wedding
        wedding.wife = request.form["wife"]
        wedding.husband = request.form["husband"]
        wedding.city = request.form["city"]
        wedding.date = datetime.datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        db.session.commit()

    user_wedding = UserWedding.query.filter_by(user_id=current_user.id).first()
    engine = sa.create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)

    return render_template('users/profile.html',
                           flask_env=current_app.config['FLASK_ENV'],
                           debug=current_app.config['DEBUG'],
                           testing=current_app.config['TESTING'],
                           upload_path=current_app.config['UPLOAD_PATH'],
                           sqlalchemy_database_uri=current_app.config['SQLALCHEMY_DATABASE_URI'],
                           log_to_stdout=os.getenv('LOG_TO_STDOUT'),
                           database_initialized=inspector.has_table("users"),
                           wedding=user_wedding.wedding
                           )


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # If the User is already logged in, don't allow them to try to register
    if current_user.is_authenticated:
        flash('Jesteś już zalogowany!')
        return redirect(url_for('users.profile'))

    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user = User(form.email.data, form.password.data)

        current_app.logger.info(f"DEBUG001... DATABASE_URL environment variable: {os.getenv('DATABASE_URL')}")
        current_app.logger.info(f"DEBUG002... CONFIG_TYPE environment variable: {os.getenv('CONFIG_TYPE')}")
        current_app.logger.info(f"DEBUG003... SQLALCHEMY_DATABASE_URI: {current_app.config['SQLALCHEMY_DATABASE_URI']}")
        current_app.logger.info(f"DEBUG004... LOG_TO_STDOUT environment variable: {os.getenv('LOG_TO_STDOUT')}")

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Dziękujemy za zarejestrowanie, {}!'.format(new_user.email))
        return redirect(url_for('users.profile'))
    return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # If the User is already logged in, don't allow them to try to log in again
    if current_user.is_authenticated:
        flash('Jesteś już zalogowany!')
        return redirect(url_for('users.profile'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.is_password_correct(form.password.data):
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)
                flash('Dziękujemy za zalogowanie, {}!'.format(current_user.email))
                return redirect(url_for('users.profile'))

        flash('Niepoprawne dane logowania')
    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Do zobaczenia!')
    return redirect(url_for('recipes.index'))
