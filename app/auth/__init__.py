from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash
from app.db import db
from app.db.models import User
from app.auth.forms import register_form, login_form

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('simple_pages.index'))
    form = register_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data), is_admin=0)
            db.session.add(user)
            db.session.commit()
            if user.id == 1:
                user.is_admin = 1
                db.session.add(user)
                db.session.commit()

            flash('Congratulations, you are now a registered user!', "success")
            return redirect(url_for('auth.login'), 302)
        else:
            flash('Already Registered')
            return redirect(url_for('auth.login'), 302)
    return render_template('register.html', form=form)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = login_form()
    if current_user.is_authenticated:
        return redirect(url_for('simple_pages.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        else:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Welcome", 'success')
            return redirect(url_for('simple_pages.index'))
    return render_template('login.html', form=form)