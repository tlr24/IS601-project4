from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user
from werkzeug.security import generate_password_hash
from app.db import db
from app.db.models import User
from app.auth.forms import register_form

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
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
        else:
            flash('Already Registered')
    return render_template('register.html', form=form)
